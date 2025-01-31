from django.urls import path

from .views.WeChatInfoView import wechat_oauth
from .views.ApplicantView import ApplicantView, ApplicantDetailView, ApplicantDepositView
from .views.MatchView import MatchResultView, MatchMentorView, MatchPartnerView, MatchDetailView
from .views.TaskView import TaskDetailView
from .views.ImageView import ImageView, ImageDetailView
from .views.MissionView import MissionView, SecretMissionView
from .views.WeChatPaymentView import WeChatPaymentView
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
    
    re_path(r'^matches/(?P<pk>\d+)/tasks/day(?P<day>[1-7])/$', TaskDetailView.as_view()),
    re_path(r'^matches/(?P<pk>\d+)/tasks/day(?P<day>[1-7])/$', TaskDetailView.as_view()),
    
    re_path(r'^matches/(?P<pk>\d+)/tasks/day(?P<day>[1-7])/images/$', ImageView.as_view()),
    re_path(r'^matches/(?P<pk>\d+)/tasks/day(?P<day>[1-7])/images/(?P<img_pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', ImageDetailView.as_view()),
    
    path("missions/", MissionView.as_view()),
    path("secret-missions/", SecretMissionView.as_view()),
    
    path("wechat/payment/", WeChatPaymentView.as_view()),
]
