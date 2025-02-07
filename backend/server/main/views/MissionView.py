from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..mixin import UtilMixin
from ..models import Mission
from ..serializers.MissionSerializer import GetMissionSerializer

from..AppConfig import AppConfig

class MissionView(APIView, UtilMixin):
    def get(self, request):
        self.assert_event_started()
        now = datetime.now()
        
        first_task_start = AppConfig.FIRST_TASK_START
        days_passed = (now - first_task_start).days + 1
        if days_passed > 7:
            days_passed = 7
        
        missions = Mission.objects.filter(day=days_passed).first()
        if missions is None:
            return Response(f"找不到第{days_passed}天的任务", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = GetMissionSerializer(missions)
        return Response({"data": serializer.data} )


class SecretMissionView(APIView, UtilMixin):
    def get(self, request):
        self.assert_event_started()
        
        openid = self.get_openid(request)
        match = self.get_latest_match_by_openid(openid)
        if match is None:
            return Response("找不到你的匹配记录", status=status.HTTP_404_NOT_FOUND)
        my_index, me, partner = self.get_match_participants(match, openid)
        self.assert_match_auth(match, me)
        
        mymMission = match.applicant1_secret_mission if my_index == 1 else match.applicant2_secret_mission
        querykey = 90 + mymMission
        
        missions = Mission.objects.filter(day=querykey).first()
        if missions is None:
            return Response("找不到你的秘密任务", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        serializer = GetMissionSerializer(missions)
        return Response({"data": serializer.data} )