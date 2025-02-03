from rest_framework import serializers
from ..models import Applicant

class CreateApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = "__all__"
        
        read_only_fields = ["id", "created_at", "updated_at", "quitted", "payment", "exclude", "confirmed", "payment_expired"]

class GetApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        exclude = ["id", "created_at", "updated_at", "quitted", "payment", "wechat_info", "exclude", "confirmed", "payment_expired"]

