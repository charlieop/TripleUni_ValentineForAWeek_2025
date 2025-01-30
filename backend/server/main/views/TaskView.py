from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import MethodNotAllowed, ParseError, NotFound

from ..serializers.TaskSerializer import GetTaskSerializer, CreateTaskSerializer
from ..mixin import UtilMixin

from ..AppConfig import AppConfig


class TaskDetailView(APIView, UtilMixin):
    def get(self, request, pk, day):
        self.assert_event_started()
        openid = self.get_openid(request)
        match = self.get_match(pk, openid)
        my_index, me, partner = self.get_match_participants(match, openid)
        self.assert_match_auth(match, me)
        task = self.get_task(match, day)
        
        if task is None:
            return Response({"msg": f"找不到第{day}天的任务提交"}, status=status.HTTP_204_NO_CONTENT)
        
        serializer = GetTaskSerializer(task)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


    def post(self, request, pk, day):
        self.assert_task_open(day)
        openid = self.get_openid(request)
        match = self.get_match(pk, openid)
        my_index, me, partner = self.get_match_participants(match, openid)
        self.assert_match_auth(match, me)

        task = self.get_task(match, day)
        if task is not None:
            raise MethodNotAllowed(f"第{day}天的任务提交已经存在, 使用 PATCH 来更新")
        
        data = {
            "match": match.id,
            "day": day,
            "submit_by": me.id,
            "submit_text": request.data.get("submit_text", None)
        }
        serializer = CreateTaskSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"msg": f"第{day}天的任务提交创建成功"}, status=status.HTTP_201_CREATED)


    def patch(self, request, pk, day):
        self.assert_task_open(day)
        submit_text = request.data.get("submit_text", None)
        if submit_text is None:
            raise ParseError("请求体中需要包含 submit_text 字段")
        
        openid = self.get_openid(request)
        match = self.get_match(pk, openid)
        my_index, me, partner = self.get_match_participants(match, openid)
        self.assert_match_auth(match, me)
        
        task = self.get_task(match, day)
        if task is None:
            raise NotFound(f"找不到第{day}天的任务提交, 使用 POST 来创建")

        data = {
            "submit_text": submit_text
        }
        serializer = CreateTaskSerializer(task, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.refresh_task_cache(task)
        return Response({"msg": f"第{day}天任务更新成功"}, status=status.HTTP_200_OK)