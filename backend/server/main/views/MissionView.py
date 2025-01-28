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
            return Response("Cannot find the corrsponding mission", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = GetMissionSerializer(missions)
        return Response(serializer.data)


class SecretMissionView(APIView, UtilMixin):
    def get(self, request):
        self.assert_event_started()
        
        missions = Mission.objects.filter(day=0).first()
        if missions is None:
            return Response("Cannot find the corrsponding mission", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = GetMissionSerializer(missions)
        return Response(serializer.data)