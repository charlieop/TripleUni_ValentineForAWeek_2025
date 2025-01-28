from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from django.db.models import Q


from ..mixin import UtilMixin, Conflict, PaymentRequired
from ..models import Match
from ..serializers.MentorSerializer import GetMentorSerializer
from ..serializers.WeChatInfoSerializer import GetWeChatInfoSerializer


class MatchResultView(APIView, UtilMixin):
    def get(self, request):
        openid = self.get_openid(request)
        matches = Match.objects.filter(Q(applicant1__wechat_info=openid) |  Q(applicant2__wechat_info=openid))
        if not matches:
            return Response({"msg": "No Match found"},
                            status=status.HTTP_204_NO_CONTENT)
        if matches.count() == 1:
            return Response({"data": {"id": matches[0].id}}, status=status.HTTP_200_OK)
        
        active_Match = matches.filter(discarded=False).last()
        return Response({"data": {"id": active_Match.id}}, status=status.HTTP_200_OK)



class MatchMentorView(APIView, UtilMixin):
    def get(self, request, pk):
        openid = self.get_openid(request)
        match = self.get_match(pk, openid)
        mentor = match.mentor
        serializer = GetMentorSerializer(mentor)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)



class MatchPartnerView(APIView, UtilMixin):
    def get(self, request, pk):
        openid = self.get_openid(request)
        match = self.get_match(pk, openid)
        my_index, me, partner = self.get_match_participants(match, openid)
        
        
        if me.payment is None:
            raise PaymentRequired("Deposit payment is required to proceed")
        
        return_data = {
            "discarded": match.discarded,
            "discard_reason": match.discard_reason,
            "my_status": match.applicant1_status if my_index == 1 else match.applicant2_status,
            "partner_status": match.applicant2_status if my_index == 1 else match.applicant1_status,
            "my_info": GetWeChatInfoSerializer(me.wechat_info).data,
            "partner_info": GetWeChatInfoSerializer(partner.wechat_info).data,
            "partner_paid": partner.payment is not None
        }
        return Response({"data": return_data}, status=status.HTTP_200_OK)


    def post(self, request, pk):
        action = request.data.get("action", None)
        if action is None:
            raise ParseError(
                "Body field \"action\" is required "
                "with value \"A\" for Accept or \"R\" for reject"
            )
        if action not in ["A", "R"]:
            raise ParseError("Invalid action value, must be \"A\" for Accept or \"R\" for reject")
        
        openid = self.get_openid(request)
        match = self.get_match(pk, openid)
        my_index, me, partner = self.get_match_participants(match, openid)
        self.assert_match_auth(match, me)
        
        my_status = match.applicant1_status if my_index == 1 else match.applicant2_status
        if my_status != "P":
            raise Conflict(f"You have already responded with {my_status}")
        
        if my_index == 1:
            match.applicant1_status = "A" if action == "A" else "R"
        else:
            match.applicant2_status = "A" if action == "A" else "R"
        
        if action == "R":
            match.discarded = True
            match.discard_reason = f"Rejected by { me.wechat_info.nickname }"
        
        match.save()
        self.refresh_match_cache(match)
        return Response({"msg": "Match updated"}, status=status.HTTP_200_OK)



class MatchDetailView(APIView, UtilMixin):
    def get(self, request, pk):
        openid = self.get_openid(request)
        match = self.get_match(pk, openid)
        my_index, me, partner = self.get_match_participants(match, openid)
        self.assert_match_auth(match, me)
        
        tasks = []
        total_score = 0
        
        for task in match.tasks.all().order_by("day"):
            tasks.append({
                "day": task.day,
                "completed": task.basic_completed,
                "basic_score": task.basic_score,
                "bonus_score": task.bonus_score,
                "daily_score": task.daily_score,
            })
            total_score += task.basic_score or 0
            total_score += task.bonus_score or 0
            total_score += task.daily_score or 0
        
        return_data = {
            "name": match.name,
            "my_info": GetWeChatInfoSerializer(me.wechat_info).data,
            "partner_info": GetWeChatInfoSerializer(partner.wechat_info).data,
            "partner_wechat_account": partner.wechat_account,
            "tasks": tasks,
            "total_score": total_score,
        }
        return Response({"data": return_data}, status=status.HTTP_200_OK)


    def patch(self, request, pk):
        name = str(request.data.get("name", ""))
        if name == "":
            raise ParseError("Query parameter \"name\" is required")
        if len(name) > 30:
            raise ParseError("Name must be less than 30 characters")
        if len(name) < 2:
            raise ParseError("Name must be more than 2 characters")
        
        openid = self.get_openid(request)
        match = self.get_match(pk, openid)
        my_index, me, partner = self.get_match_participants(match, openid)
        self.assert_match_auth(match, me)
        
        match.name = name
        match.save()
        self.refresh_match_cache(match)
        return Response({"msg": "Match updated"}, status=status.HTTP_200_OK)