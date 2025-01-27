from rest_framework import serializers
from ..models import Mentor

class GetMentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = ["name", "wechat", "wechat_qrcode"]
        read_only_fields = fields
