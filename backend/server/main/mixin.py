from rest_framework.exceptions import APIException, NotFound, PermissionDenied, ParseError
import uuid

from .models import Applicant, Match


class Gone(APIException):
    status_code = 410
    default_detail = "The requested resource is no longer available."
    default_code = "gone"


class Conflict(APIException):
    status_code = 409
    default_detail = "A conflict occurred."
    default_code = "conflict"


class PaymentRequired(APIException):
    status_code = 402
    default_detail = "Payment is required to proceed."
    default_code = "payment_required"


class UtilMixin:
    def get_openid(self, request):
        openid = request.headers.get('Authorization')
        if openid is None:
            raise ParseError("Authorization header with user \"openid\" is required")
        return openid


    def get_applicant(self, pk, openid):
        try:
            uuid.UUID(pk)
        except ValueError:
            raise ParseError("The code is not a valid UUID")
        applicant = Applicant.objects.filter(id=pk).first()
        if not applicant:
            raise PermissionDenied("Unauthorized to access this applicant")
        if applicant.quitted:
            raise Gone("Applicant has quitted")
        if applicant.wechat_info.openid != openid:
            raise PermissionDenied("Unauthorized to access this applicant")
        return applicant


    def get_match(self, pk, openid):
        match = Match.objects.filter(id=pk).first()
        if not match:
            raise PermissionDenied("Unauthorized to access this match")
        if match.applicant1.wechat_info.openid != openid and match.applicant2.wechat_info.openid != openid:
            raise PermissionDenied("Unauthorized to access this match")
        return match
    
    
    def get_match_participants(self, match, openid):
        my_index = 1 if match.applicant1.wechat_info.openid == openid else 2
        me = match.applicant1 if my_index == 1 else match.applicant2
        partner = match.applicant2 if my_index == 1 else match.applicant1
        return my_index, me, partner
    
    
    def assert_match_auth(self, match, me):
        if me.payment is None:
            raise PaymentRequired("Deposit payment is required to proceed")
        if match.discarded:
            raise PermissionDenied(f"Match has already been discarded due to: {match.discard_reason or 'Unknown'}")


    def get_task(self, match, day):
        return match.tasks.filter(day=day).first()