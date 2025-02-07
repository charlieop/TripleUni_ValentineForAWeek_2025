from datetime import timedelta
from rest_framework.exceptions import APIException, NotFound, PermissionDenied, ParseError
import uuid
import pickle
from django.core.cache import cache
from django.db.models import Q

from .models import Applicant, Match
from .AppConfig import AppConfig


class Gone(APIException):
    status_code = 410
    default_detail = "The requested resource is no longer available."
    default_code = "gone"


class Conflict(APIException):
    status_code = 409
    default_detail = "A conflict occurred."
    default_code = "conflict"


class PaymentRequired(APIException):
    status_code = 402
    default_detail = "Payment is required to proceed."
    default_code = "payment_required"


class UtilMixin:
    def _get_applicant_key(self, pk):
        return f"applicants:{pk}"
    def _get_match_key(self, pk):
        return f"matches:{pk}"
    def _get_task_key(self, match, day):
        return f"tasks:{match.id}:day{day}"
    
    
    def get_openid(self, request):
        openid = request.headers.get('Authorization')
        if openid is None:
            raise ParseError("Authorization header with user \"openid\" is required")
        return openid
    
    def get_applicant_by_openid(self, openid):
        applicant = Applicant.objects.filter(wechat_info=openid).first()
        return applicant

    def get_applicant(self, pk, openid):
        try:
            uuid.UUID(pk)
        except ValueError:
            raise ParseError("输入的申请人ID格式不正确")
        
        KEY = self._get_applicant_key(pk)
        cached_applicant = cache.get(KEY)
        
        if cached_applicant:
            applicant = pickle.loads(cached_applicant)
        else:
            applicant = Applicant.objects.filter(id=pk).first()
            if not applicant:
                raise PermissionDenied("你无权访问此申请者")
            pickled = pickle.dumps(applicant)
            cache.set(KEY, pickled)
            
        if applicant.quitted:
            raise Gone("申请者已经退出")
        if applicant.wechat_info.openid != openid:
            raise PermissionDenied("你无权访问此申请者")
        
        return applicant
    
    def refresh_applicant_cache(self, applicant):
        KEY = self._get_applicant_key(applicant.id)
        cache.delete(KEY)
        
    def get_latest_match_by_openid(self, openid):
        if not AppConfig.passed(AppConfig.FIRST_ROUND_MATCH_RESULTS_RELEASE):
            raise PermissionDenied("匹配结果暂未公布")
        matches = Match.objects.filter(Q(applicant1__wechat_info=openid) |  Q(applicant2__wechat_info=openid))
        if not matches:
            return None
        if matches.count() == 1:
            return matches[0]
        active_Match = matches.filter(discarded=False).last()
        return active_Match

    def get_match(self, pk, openid):
        KEY = self._get_match_key(pk)
        cached_match = cache.get(KEY)
        if cached_match:
            match = pickle.loads(cached_match)
        else:
            match = Match.objects.filter(id=pk).first()
            if not match:
                raise PermissionDenied("你无权访问此配对")
            pickled = pickle.dumps(match)
            cache.set(KEY, pickled)
        
        if match.applicant1.wechat_info.openid != openid and match.applicant2.wechat_info.openid != openid:
                raise PermissionDenied("你无权访问此配对")
        return match
    
    def refresh_match_cache(self, match):
        KEY = self._get_match_key(match.id)
        cache.delete(KEY)
    
    
    def get_match_participants(self, match, openid):
        my_index = 1 if match.applicant1.wechat_info.openid == openid else 2
        me = match.applicant1 if my_index == 1 else match.applicant2
        partner = match.applicant2 if my_index == 1 else match.applicant1
        return my_index, me, partner
    

    def assert_match_auth(self, match, me):
        if me.payment is None:
            raise PaymentRequired("你需要支付押金以继续")
        if match.discarded:
            raise PermissionDenied(f"此配对已经作废, 原因是: {match.discard_reason or '未知'}")


    def get_task(self, match, day):
        KEY = self._get_task_key(match, day)
        cached_task = cache.get(KEY)
        
        if cached_task:
            task = pickle.loads(cached_task)
        else:
            task = match.tasks.filter(day=day).first()
            if task:
                cache.set(KEY, pickle.dumps(task))

        return task
    
    def refresh_task_cache(self, task):
        KEY = self._get_task_key(task.match, task.day)
        cache.delete(KEY)


    def assert_application_deadline(self):
        if AppConfig.passed(AppConfig.APPLICATION_DEADLINE):
            raise PermissionDenied("提交申请DDL已过, 明年再来吧")

    def assert_match_results_released(self, match):
        if match.round == 1 and not AppConfig.passed(AppConfig.FIRST_ROUND_MATCH_RESULTS_RELEASE):
            raise PermissionDenied("第一轮的匹配结果暂未公布")
        if match.round == 2 and not AppConfig.passed(AppConfig.SECOND_ROUND_MATCH_RESULTS_RELEASE):
            raise PermissionDenied("第二轮的匹配结果暂未公布")
        
    def assert_match_confirm_deadline(self, match):
        if match.round == 1 and AppConfig.passed(AppConfig.FIRST_ROUND_MATCH_RESULTS_CONFIRMATION_DEADLINE):
            raise PermissionDenied("第一轮的押金缴纳DDL已过")
        if match.round == 2 and AppConfig.passed(AppConfig.SECOND_ROUND_MATCH_RESULTS_CONFIRMATION_DEADLINE):
            raise PermissionDenied("第二轮的押金缴纳DDL已过")

    def assert_event_started(self):
        if not AppConfig.passed(AppConfig.EVENT_START):
            raise PermissionDenied("活动还未开始")
        
    def assert_event_not_ended(self):
        if AppConfig.passed(AppConfig.EVENT_END):
            raise PermissionDenied("活动已经结束")
        
    def assert_task_open(self, day):
        offset_day = int(day) - 1
        task_start_time = AppConfig.FIRST_TASK_START + timedelta(days=offset_day)
        task_end_time = AppConfig.FIRST_TASK_DEADLINE + timedelta(days=offset_day)
        
        if not AppConfig.passed(task_start_time):
            raise PermissionDenied(f"第{day}天的任务还未开始")
        if AppConfig.passed(task_end_time):
            raise PermissionDenied(f"第{day}天的任务已经结束")
