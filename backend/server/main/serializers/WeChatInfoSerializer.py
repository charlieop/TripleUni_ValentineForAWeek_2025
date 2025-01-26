from rest_framework import serializers
from ..models import WeChatInfo

class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeChatInfo
        fields = "__all__"
        
        read_only_fields = ["created_at"]