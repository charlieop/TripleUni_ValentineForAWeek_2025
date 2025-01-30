from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied

from ..mixin import UtilMixin, Conflict, NotFound
from ..models import Applicant, PaymentVoucher
from ..serializers.ApplicantSerializer import CreateApplicantSerializer, GetApplicantSerializer
import uuid
import copy


def format_applicant_data(raw, openid):
    data = copy.deepcopy(raw)
    
    data.pop("payment", None)
    data.pop("quitted", None)
    data.pop("exclude", None)
    data["wechat_info"] = openid
    
    email = data.get("email", None)
    school = data.get("school", None)
    if school is None or email is None:
        raise ParseError("School and email are required")
    if school == "UST":
        if not email.endswith("@connect.ust.hk"):
            raise ParseError("The email is not a valid UST email")
    elif school == "HKU":
        if not email.endswith("@connect.hku.hk"):
            raise ParseError("The email is not a valid HKU email")
    elif school == "CUHK":
        if not email.endswith("@link.cuhk.edu.hk"):
            raise ParseError("The email is not a valid CUHK email")
    
    hobbies = data.pop("hobbies", [])
    if len(hobbies) > 3:
        raise ParseError("The number of hobbies should not exceed 3")
    for i, hobby in enumerate(hobbies):
        data[f"hobby{i+1}"] = hobby
        
    preferred_grades = data.pop("preferred_grades", [])
    grade = ""
    for preferred_grade in preferred_grades:
        grade += preferred_grade
        grade += "|"
    data["preferred_grades"] = grade[:-1]
    
    preferred_schools = data.pop("preferred_schools", [])
    school = ""
    for preferred_school in preferred_schools:
        school += preferred_school
        school += "|"
    data["preferred_schools"] = school[:-1]
    
    if not "continue_match" in data or data["continue_match"] is None:
        data["continue_match"] = True
    
    return data
    
    
def formatted_applicant_data_to_raw(data):
    raw = copy.deepcopy(data)
    
    hobbies = []
    for i in range(1, 4):
        hobby = raw.pop(f"hobby{i}", None)
        if hobby is not None:
            hobbies.append(hobby)
    raw["hobbies"] = hobbies
    
    preferred_grades = raw.pop("preferred_grades", None)
    if preferred_grades is not None:
        raw["preferred_grades"] = preferred_grades.split("|")
        
    preferred_schools = raw.pop("preferred_schools", None)
    if preferred_schools is not None:
        raw["preferred_schools"] = preferred_schools.split("|")
    
    return raw
    

class ApplicantView(APIView, UtilMixin):
    def get(self, request):
        openid = self.get_openid(request)
        applicant = Applicant.objects.filter(wechat_info=openid).first()
        if not applicant:
            return Response({"msg": "Applicant with the given \"openid\" does not exist"},
                            status=status.HTTP_204_NO_CONTENT)
        return Response({"data": {"id": applicant.id}}, status=status.HTTP_200_OK)


    def post(self, request):
        self.assert_application_deadline()
        
        openid = self.get_openid(request)
        data = format_applicant_data(request.data, openid)
        
        serializer = CreateApplicantSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"data": {"id": serializer.instance.id}}, status=status.HTTP_201_CREATED)



class ApplicantDetailView(APIView, UtilMixin):
    def get(self, request, pk):
        self.assert_application_deadline()
        
        openid = self.get_openid(request)
        applicant = self.get_applicant(pk, openid)
        serializer = GetApplicantSerializer(applicant)
        raw = formatted_applicant_data_to_raw(serializer.data)
        return Response({"data": raw}, status=status.HTTP_200_OK)


    def patch(self, request, pk):
        self.assert_application_deadline()
        
        openid = self.get_openid(request)
        applicant = self.get_applicant(pk, openid)
        
        data = format_applicant_data(request.data, openid)

        serializer = CreateApplicantSerializer(applicant, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.refresh_applicant_cache(applicant)
        return Response({"msg": "Applicant updated"}, status=status.HTTP_200_OK)


    def delete(self, request, pk):
        self.assert_application_deadline()

        openid = self.get_openid(request)
        applicant = self.get_applicant(pk, openid)
        
        applicant.quitted = True
        applicant.save()
        self.refresh_applicant_cache(applicant)
        return Response({"msg": "Applicant quitted"}, status=status.HTTP_204_NO_CONTENT)



class ApplicantDepositView(APIView, UtilMixin):
    def get(self, request, pk):
        openid = self.get_openid(request)
        applicant = self.get_applicant(pk, openid)
        if applicant.payment is None:
            return Response({"data": {"paid": False}}, status=status.HTTP_200_OK)
        return Response({"data": {"paid": True}}, status=status.HTTP_200_OK)


    def post(self, request, pk):
        code = request.data.get("code", None)
        if code is None:
            raise ParseError("Query parameter \"code\" is required")

        openid = self.get_openid(request)
        applicant = self.get_applicant(pk, openid)
        
        if applicant.payment is not None:
            raise Conflict("The applicant has already paid the deposit")

        try:
            uuid.UUID(code)
        except ValueError:
            raise ParseError("The code is not a valid UUID")
        payment = PaymentVoucher.objects.filter(id=code).first()
        if not payment:
            raise NotFound("The payment code does not exist")
        if hasattr(payment, "applicant") and payment.applicant is not None:
            raise Conflict("The payment code has already been redeemed")

        applicant.payment = payment
        applicant.save()
        self.refresh_applicant_cache(applicant)
        return Response({"msg": "Deposit paid successfully"}, status=status.HTTP_200_OK)