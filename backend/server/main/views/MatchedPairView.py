from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ParseError

from ..mixin import UtilMixin, Conflict, NotFound
from ..models import MatchedPair, Applicant, Mentor, Task
# from ..serializers.MatchedPairSerializer import GetMatchedPairSerializer, CreateMatchedPairSerializer


class MatchedpartnerView(APIView, UtilMixin):
    def get(self, request):
        # get the headimg, nickname and wechatAccount of the matched person
        raise NotImplementedError
    
class MatchedMentorView(APIView, UtilMixin):
    def get(self, request):
        # get the name, wechatAccount and QR code of the mentor
        raise NotImplementedError
    
    
