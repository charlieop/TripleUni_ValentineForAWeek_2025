from wechatpayv3 import WeChatPay, WeChatPayType
from uuid import uuid4
from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, AuthenticationFailed


from ..mixin import UtilMixin, Gone
from ..models import PaymentRecord

from django.conf import settings
import json

with open(settings.BASE_DIR / "SECRETS.json") as f:
    secrets = json.load(f)
    APPID = secrets["WECHAT_APP_ID"]
    CERT_SERIAL_NO = secrets["WECHAT_CERT_SERIAL_NO"]
    APIV3_KEY = secrets["WECHAT_APIV3_KEY"]
    MCHID = secrets["WECHAT_MCHID"]
with open(settings.BASE_DIR / "apiclient_key.pem") as f:
    PRIVATE_KEY = f.read()
    
PRICE = 70 * 100
EXPIRES_IN = 7 * 60
DESCRIPTION = "Triple Uni 一周CP 2025 活动押金"
NOTIFY_URL = "https://api.charlieop.com/api/v1/wechat/payment/"
CERT_DIR = str(settings.BASE_DIR / "cert")
PARTNER_MODE = False
TIMEOUT = (7, 20)

wxpay = WeChatPay(
    wechatpay_type=WeChatPayType.NATIVE,
    mchid=MCHID,
    private_key=PRIVATE_KEY,
    cert_serial_no=CERT_SERIAL_NO,
    apiv3_key=APIV3_KEY,
    appid=APPID,
    notify_url=NOTIFY_URL,
    cert_dir=CERT_DIR,
    partner_mode=PARTNER_MODE,
    timeout=TIMEOUT
)

class WeChatPaymentView(APIView, UtilMixin):
    def get(self, request):        
        openid = self.get_openid(request)
        match = self.get_latest_match_by_openid(openid)
        if not match:
            raise NotFound("找不到你的匹配结果")
        self.assert_match_results_released(match)
        self.assert_match_confirm_deadline(match)
        my_index, me, partner = self.get_match_participants(match, openid)
        if me.payment is not None:
            raise Gone("你已经支付过了")
        
        out_trade_no = str(uuid4()).replace('-', '')
        expire_time = datetime.now() + timedelta(seconds=EXPIRES_IN)
        expire_time_str = expire_time.strftime("%Y-%m-%dT%H:%M:%S+08:00")
        
        code, message = wxpay.pay(
            description=DESCRIPTION,
            out_trade_no=out_trade_no,
            amount={'total': PRICE},
            pay_type=WeChatPayType.JSAPI,
            payer={'openid': openid},
            time_expire=expire_time_str
        )
        result = json.loads(message)
        if code in range(200, 300):
            prepay_id = result.get('prepay_id')
            timestamp = str(int(datetime.now().timestamp()))
            noncestr = str(uuid4()).replace('-', '')
            package = 'prepay_id=' + prepay_id
            sign = wxpay.sign([APPID, timestamp, noncestr, package])
            signtype = 'RSA'
            data = {
                'appId': APPID,
                'timeStamp': timestamp,
                'nonceStr': noncestr,
                'package': 'prepay_id=%s' % prepay_id,
                'signType': signtype,
                'paySign': sign
            }
            return Response({"data": data}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "调起微信支付接口失败"}, status=code)
        
        
    def post(self, request):
        result = wxpay.callback(headers=request.META, body=request.body)
        if not (result and result.get('event_type') == 'TRANSACTION.SUCCESS'):
            raise AuthenticationFailed("支付失败")
        
        resource = result.get('resource')
        out_trade_no = resource.get('out_trade_no')
        transaction_id = resource.get('transaction_id')
        payer = resource.get('payer')
        openid = payer.get('openid')
        
        payment = PaymentRecord.objects.create(
            out_trade_no=out_trade_no,
            transaction_id=transaction_id
        )
        payment.save()
        
        applicant = self.get_applicant_by_openid(openid)
        if applicant is None:
            return Response({"detail": "找不到对应的报名信息"}, status=status.HTTP_200_OK)
        applicant.payment = payment
        applicant.save()
        self.refresh_applicant_cache(applicant)
        return Response({"msg": "支付成功"}, status=status.HTTP_200_OK)