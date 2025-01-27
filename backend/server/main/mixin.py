from rest_framework.exceptions import APIException, NotFound, PermissionDenied, ParseError

from .models import Applicant

class Gone(APIException):
    status_code = 410
    default_detail = "The requested resource is no longer available."
    default_code = "gone"
    
class Conflict(APIException):
    status_code = 409
    default_detail = "A conflict occurred."
    default_code = "conflict"



class UtilMixin:
    def get_openid(self, request):
        openid = request.headers.get('Authorization')
        if openid is None:
            raise ParseError("Authorization header with user \"openid\" is required")
        return openid

    def get_applicant(self, pk, openid):
        applicant = Applicant.objects.filter(id=pk).first()
        if not applicant:
            raise NotFound("Applicant with the given \"id\" does not exist")
        if applicant.quitted:
            raise Gone("Applicant has quitted")
        if applicant.wechat_info.openid != openid:
            raise PermissionDenied("Unauthorized to access this applicant")
        return applicant
    
    
