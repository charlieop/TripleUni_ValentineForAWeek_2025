from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError, PermissionDenied
from django.db.models import Q


from ..mixin import UtilMixin, Conflict, PaymentRequired
from ..models import Match
from ..serializers.MentorSerializer import GetMentorSerializer
from ..serializers.WeChatInfoSerializer import GetWeChatInfoSerializer
from ..serializers.TaskSerializer import GetTaskSerializer

from ..AppConfig import AppConfig


class MatchResultView(APIView, UtilMixin):
    def get(self, request):
        openid = self.get_openid(request)
        latest_match = self.get_latest_match_by_openid(openid)
        if not latest_match:
            return Response({"msg": "找不到你的匹配结果"},
                            status=status.HTTP_204_NO_CONTENT)
        return Response({"data": {"id": latest_match.id, "round": latest_match.round}}, status=status.HTTP_200_OK)



class MatchMentorView(APIView, UtilMixin):
    def get(self, request, pk):
        openid = self.get_openid(request)
        match = self.get_match(pk, openid)
        self.assert_match_results_released(match)
        mentor = match.mentor
        
        serializer = GetMentorSerializer(mentor)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)



class MatchPartnerView(APIView, UtilMixin):
    def get(self, request, pk):
        if not AppConfig.passed(AppConfig.FIRST_ROUND_MATCH_RESULTS_RELEASE):
            raise PermissionDenied("匹配结果暂未公布")
        
        openid = self.get_openid(request)
        match = self.get_match(pk, openid)
        self.assert_match_results_released(match)
        my_index, me, partner = self.get_match_participants(match, openid)
        if me.payment is None:
            raise PaymentRequired("你需要支付押金才能继续")
        
        return_data = {
            "round": match.round,
            "discarded": match.discarded,
            "discard_reason": match.discard_reason,
            "my_status": match.applicant1_status if my_index == 1 else match.applicant2_status,
            "partner_status": match.applicant2_status if my_index == 1 else match.applicant1_status,
            "partner_info": GetWeChatInfoSerializer(partner.wechat_info).data,
            "partner_paid": partner.payment is not None,
            "partner_sex": partner.sex,
            "partner_school": partner.school,
        }
        return Response({"data": return_data}, status=status.HTTP_200_OK)


    def post(self, request, pk):
        action = request.data.get("action", None)
        if action is None:
            raise ParseError("请求体中的 action 字段是必需的")
        if action not in ["A", "R"]:
            raise ParseError("请求体中的 action 字段必须是 A 或 R (接受 或 拒绝)")
        
        openid = self.get_openid(request)
        match = self.get_match(pk, openid)
        self.assert_match_results_released(match)
        self.assert_match_confirm_deadline(match)
        
        my_index, me, partner = self.get_match_participants(match, openid)
        self.assert_match_auth(match, me)
                
        my_status = match.applicant1_status if my_index == 1 else match.applicant2_status
        if my_status != "P":
            raise Conflict(f"你已经选择了{my_status}, 无法更改")
        
        if my_index == 1:
            match.applicant1_status = action
        else:
            match.applicant2_status = action
        
        if action == "R":
            match.discarded = True
            match.discard_reason = f"由 { me.wechat_info.nickname } 拒绝了此次匹配结果"
        
        match.save()
        self.refresh_match_cache(match)
        return Response({"msg": "匹配已更新"}, status=status.HTTP_200_OK)



class MatchDetailView(APIView, UtilMixin):
    def get(self, request, pk):
        self.assert_event_started()

        openid = self.get_openid(request)
        match = self.get_match(pk, openid)
        my_index, me, partner = self.get_match_participants(match, openid)
        self.assert_match_auth(match, me)
        
        tasks = []
        total_score = 0
        
        for task in match.tasks.all().order_by("day"):
            tasks.append(GetTaskSerializer(task).data)
            total_score += task.basic_score or 0
            total_score += task.bonus_score or 0
            total_score += task.daily_score or 0
        
        return_data = {
            "id": match.id,
            "name": match.name,
            "my_info": GetWeChatInfoSerializer(me.wechat_info).data,
            "partner_info": GetWeChatInfoSerializer(partner.wechat_info).data,
            "partner_wxid": partner.wxid,
            "tasks": tasks,
            "total_score": total_score,
        }
        return Response({"data": return_data}, status=status.HTTP_200_OK)


    def patch(self, request, pk):
        self.assert_event_started()
        self.assert_event_not_ended()
        
        name = str(request.data.get("name", ""))
        if name == "":
            raise ParseError("请求体中的 name 字段是必需的")
        if len(name) > 30:
            raise ParseError("Name字段不能超过30个字符")
        if len(name) < 2:
            raise ParseError("Name字段不能少于2个字符")
        
        openid = self.get_openid(request)
        match = self.get_match(pk, openid)
        my_index, me, partner = self.get_match_participants(match, openid)
        self.assert_match_auth(match, me)
        
        match.name = name
        match.save()
        self.refresh_match_cache(match)
        return Response({"msg": "匹配更新成功"}, status=status.HTTP_200_OK)