from django.urls import path

from .views.WeChatInfoView import wechat_oauth
from .views.ApplicantView import ApplicantView, ApplicantDetailView, ApplicantDepositView
from .views.MatchedPairView import MatchedpartnerView, MatchedMentorView
from django.urls import re_path

urlpatterns = [
    path("oauth/wechat/", wechat_oauth),
    path("applicants/", ApplicantView.as_view()),
    re_path(r'^applicants/(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', ApplicantDetailView.as_view()),
    re_path(r'^applicants/(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/deposit/$', ApplicantDepositView.as_view()),
    path("matched/partner/", MatchedpartnerView.as_view()),
    path("matched/mentor/", MatchedMentorView.as_view()),
    
]
