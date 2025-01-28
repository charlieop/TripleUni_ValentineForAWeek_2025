from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import MethodNotAllowed, ParseError, NotFound

from ..serializers.TaskSerializer import GetTaskSerializer, CreateTaskSerializer
from ..mixin import UtilMixin


class TaskDetailView(APIView, UtilMixin):
    def get(self, request, pk, day):
        openid = self.get_openid(request)
        match = self.get_match(pk, openid)
        my_index, me, partner = self.get_match_participants(match, openid)
        self.assert_match_auth(match, me)
        task = self.get_task(match, day)
        
        if task is None:
            return Response({"msg": f"No Task found for day {day}"}, status=status.HTTP_204_NO_CONTENT)
        
        serializer = GetTaskSerializer(task)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    
    
    def post(self, request, pk, day):
        openid = self.get_openid(request)
        match = self.get_match(pk, openid)
        my_index, me, partner = self.get_match_participants(match, openid)
        self.assert_match_auth(match, me)

        task = self.get_task(match, day)
        if task is not None:
            raise MethodNotAllowed(f"Task already exists for day {day}, use PATCH to update")
        
        data = {
            "match": match.id,
            "day": day,
            "submit_by": me.id,
            "submit_text": request.data.get("submit_text", None)
        }
        serializer = CreateTaskSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"msg": f"Task created for day {day}"}, status=status.HTTP_201_CREATED)
    
    
    def patch(self, request, pk, day):
        submit_text = request.data.get("submit_text", None)
        if submit_text is None:
            raise ParseError("Field: \"submit_text\" is required in body")
        
        openid = self.get_openid(request)
        match = self.get_match(pk, openid)
        my_index, me, partner = self.get_match_participants(match, openid)
        self.assert_match_auth(match, me)
        
        task = self.get_task(match, day)
        if task is None:
            raise NotFound(f"No Task exist for day {day}, use POST to create")

        data = {
            "submit_text": submit_text
        }
        serializer = CreateTaskSerializer(task, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"msg": f"Task updated for day {day}"}, status=status.HTTP_200_OK)