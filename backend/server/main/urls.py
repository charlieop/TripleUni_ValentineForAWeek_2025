from django.urls import path

from .views.WeChatInfoView import wechat_oauth
from .views.ApplicantView import ApplicantView, ApplicantDetailView, ApplicantDepositView
from .views.MatchView import MatchResultView, MatchMentorView, MatchPartnerView, MatchDetailView
from django.urls import re_path

urlpatterns = [
    path("oauth/wechat/", wechat_oauth),
    path("applicants/", ApplicantView.as_view()),
    re_path(r'^applicants/(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', ApplicantDetailView.as_view()),
    re_path(r'^applicants/(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/deposit/$', ApplicantDepositView.as_view()),
    path("matches/result/", MatchResultView.as_view()),
    re_path(r'^matches/(?P<pk>\d+)/mentor/$', MatchMentorView.as_view()),
    re_path(r'^matches/(?P<pk>\d+)/partner/$', MatchPartnerView.as_view()),
    re_path(r'^matches/(?P<pk>\d+)/$', MatchDetailView.as_view()),
]
