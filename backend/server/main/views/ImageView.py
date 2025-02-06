from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError, NotFound, UnsupportedMediaType
from django.http.request import QueryDict
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile


from ..mixin import UtilMixin
from ..models import Image
from ..serializers.ImageSerializer import GetImageSerializer

from ..AppConfig import AppConfig


class ImageView(APIView, UtilMixin):
    def get(self, request, pk, day):
        self.assert_event_started()
        openid = self.get_openid(request)
        match = self.get_match(pk, openid)
        my_index, me, partner = self.get_match_participants(match, openid)
        self.assert_match_auth(match, me)

        task = self.get_task(match, day)
        if task is None:
            raise NotFound(f"找不到第{day}天的任务")
        
        imgs = task.imgs.filter(deleted=False).all()
        serializer = GetImageSerializer(imgs, many=True)
        
        return Response({"data": {"imgs": serializer.data}}, status=status.HTTP_200_OK)


    def post(self, request, pk, day):
        self.assert_task_open(day)
        if type(request.data) != QueryDict:
            raise ParseError("Field: \"image\" is required in body with multipart/form-data")
        
        images = request.data.getlist("images", [])
        for img in images:
            if type(img) not in [InMemoryUploadedFile, TemporaryUploadedFile]:
                raise UnsupportedMediaType("上传的内容中包含非图片内容")
            if img.content_type not in ['image/jpeg', 'image/png', 'image/jpg', 'image/heic']:
                raise UnsupportedMediaType("不支持的图片格式, 只支持JPEG, PNG, JPG, HEIC")
            if img.size > 2 * 1024 * 1024:
                raise ParseError('文件过大, 请保证图片大小在2MB以内')
        
        openid = self.get_openid(request)
        match = self.get_match(pk, openid)
        my_index, me, partner = self.get_match_participants(match, openid)
        self.assert_match_auth(match, me)
        
        task = self.get_task(match, day)
        if task is None:
            raise NotFound(f"找不到第{day}天的任务")
        
        self.refresh_task_cache(task)
        for img in images:
            data = {
                "task": task,
                "image": img
            }
            image = Image.objects.create(**data)
            image.save()
        
        return Response({"msg": "图片上传成功"}, status=status.HTTP_201_CREATED)



class ImageDetailView(APIView, UtilMixin):
    def delete(self, request, pk, day, img_pk):
        self.assert_task_open(day)
        openid = self.get_openid(request)
        match = self.get_match(pk, openid)
        my_index, me, partner = self.get_match_participants(match, openid)
        self.assert_match_auth(match, me)
        
        task = self.get_task(match, day)
        if task is None:
            raise NotFound(f"找不到第{day}天的任务")
        
        image = task.imgs.filter(id=img_pk).first()
        if not image or image.deleted:
            raise NotFound("找不到此ID对应的图片")
        image.deleted = True
        image.save()
        self.refresh_task_cache(task)
        return Response({"msg": "图片删除成功"}, status=status.HTTP_204_NO_CONTENT)