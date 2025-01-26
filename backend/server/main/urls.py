from django.urls import path

from .views.WeChatInfoView import wechat_oauth

urlpatterns = [
    # path("", views.hello_world),
    path("oauth/wechat", wechat_oauth),
]

# PATHS To be added

# POST
# /applicants

# GET PUT DELETE
# r'^applicants/(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$'

