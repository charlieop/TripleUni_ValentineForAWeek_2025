from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ParseError

from ..mixin import UtilMixin, Conflict, NotFound
from ..models import Applicant, PaymentVoucher
from ..serializers.ApplicantSerializer import CreateApplicantSerializer, GetApplicantSerializer
import uuid


""" FOR TESTING PURPOSES
"openid":"ocuJM7I1DSEuJI036h4_teUBbJwk"

{
    "name": "test",
    "sex": "M",
    "grade": "UG3",
    "school": "UST",
    "email": "123@aa.com",
    "wechat_account": "testla",
}
"""


class ApplicantView(APIView, UtilMixin):
    def get(self, request):
        openid = self.get_openid(request)
        applicant = Applicant.objects.filter(wechat_info=openid).first()
        if not applicant:
            return Response({"error": "Applicant with the given \"openid\" does not exist"},
                            status=status.HTTP_204_NO_CONTENT)
        return Response({"data": {"id": applicant.id}}, status=status.HTTP_200_OK)

    def post(self, request):
        openid = self.get_openid(request)
        data = request.data
        data.pop("payment", None)
        data.pop("quitted", None)
        data["wechat_info"] = openid
        
        serializer = CreateApplicantSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"data": {"id": serializer.instance.id}}, status=status.HTTP_201_CREATED)


class ApplicantDetailView(APIView, UtilMixin):
    def get(self, request, pk):
        openid = self.get_openid(request)
        applicant = self.get_applicant(pk, openid)
        serializer = GetApplicantSerializer(applicant)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        openid = self.get_openid(request)
        applicant = self.get_applicant(pk, openid)
        
        data = request.data
        data.pop("wechat_info", None)
        data.pop("payment", None)
        data.pop("quitted", None)

        serializer = CreateApplicantSerializer(applicant, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"msg": "Applicant updated"}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        openid = self.get_openid(request)
        applicant = self.get_applicant(pk, openid)
        
        applicant.quitted = True
        applicant.save()
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
        return Response({"msg": "Deposit paid successfully"}, status=status.HTTP_200_OK)
    