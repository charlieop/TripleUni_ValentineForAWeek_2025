import requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.files.base import ContentFile

from ..models import WeChatInfo

APP_ID = "wx04ddbc9e6bebf0e5"
SECRET = "11f812177e08f6e4851e798541820aca"

@api_view(["POST"])
def wechat_oauth(request):
    if "code" not in request.data:
        return Response({"detail": "code not found"}, status=status.HTTP_400_BAD_REQUEST)
    
    code = request.data["code"]
    
    # fetch access token
    ACCESS_TOKEN_URL = (
        "https://api.weixin.qq.com/sns/oauth2/access_token?"
        f"appid={APP_ID}&"
        f"secret={SECRET}&"
        f"code={code}&"
        "grant_type=authorization_code"
    )
    
    response = requests.get(ACCESS_TOKEN_URL)
    if response.status_code != 200:
        return Response({"detail": "failed to fetch access token"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    content = response.json()
    if "errcode" in content:
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    ACCESS_TOKEN = content["access_token"]
    OPENID = content["openid"]
    
    # fetch user info
    USER_INFO_URL = (
        f"https://api.weixin.qq.com/sns/userinfo?"
        f"access_token={ACCESS_TOKEN}&"
        f"openid={OPENID}"
        f"lang=zh_CN"
    )
    
    user_info_response = requests.get(USER_INFO_URL)
    if user_info_response.status_code != 200:
        return Response({"detail": "failed to fetch user info"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    user_info_content = user_info_response.json()
    if "errcode" in user_info_content:
        return Response(user_info_content, status=status.HTTP_400_BAD_REQUEST)
    
    NICKNAME = user_info_content["nickname"]
    HEADIMGURL = user_info_content["headimgurl"]
    
    return _saveToModel(OPENID, NICKNAME, HEADIMGURL)


def _saveToModel(openid, nickname, headimgurl):
    existing_user = WeChatInfo.objects.filter(openid=openid).first()
    if existing_user:
        existing_user.nickname = nickname
        if existing_user.head_image_url != headimgurl:
            image_file = _fetchImage(openid, headimgurl)
            if image_file:
                existing_user.head_image = image_file
                existing_user.head_image_url = headimgurl
        existing_user.save()
        return Response({"data": {"openid" : openid}}, status=status.HTTP_200_OK)

    # If the user does not exist, proceed to create a new one
    image_file = _fetchImage(openid, headimgurl)
    if not image_file:
        return Response({"detail": "failed to fetch head image"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    data = {
        "openid": openid,
        "nickname": nickname,
        "head_image": image_file,
        "head_image_url": headimgurl
    }
    newWeChatInfo = WeChatInfo(**data)
    
    try:
        newWeChatInfo.full_clean()
        newWeChatInfo.save()
        return Response({"data": {"openid" : openid}}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

def _fetchImage(openid, url):
    image_response = requests.get(url)
    if image_response.status_code != 200:
        return None
    image_file = ContentFile(image_response.content)
    image_file.name = f"{openid}.jpg"
    return image_file
