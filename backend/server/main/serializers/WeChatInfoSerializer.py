from rest_framework import serializers
from ..models import WeChatInfo

class GetWeChatInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeChatInfo
        fields = ["nickname", "head_image", "head_image_url"]
        read_only_fields = fields
