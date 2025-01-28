from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError, NotFound, UnsupportedMediaType
from django.http.request import QueryDict
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile


from ..mixin import UtilMixin
from ..models import Image
from ..serializers.ImageSerializer import GetImageSerializer


class ImageView(APIView, UtilMixin):
    def get(self, request, pk, day):
        openid = self.get_openid(request)
        match = self.get_match(pk, openid)
        my_index, me, partner = self.get_match_participants(match, openid)
        self.assert_match_auth(match, me)

        task = self.get_task(match, day)
        if task is None:
            raise NotFound(f"No Task exist for day {day}")
        
        imgs = task.imgs.filter(deleted=False).all()
        serializer = GetImageSerializer(imgs, many=True)
        
        return Response({"data": {"imgs": serializer.data}}, status=status.HTTP_200_OK)
    
    
    def post(self, request, pk, day):
        if type(request.data) != QueryDict:
            raise ParseError("Field: \"image\" is required in body with multipart/form-data")
        
        images = request.data.getlist("images", [])
        for img in images:
            if type(img) not in [InMemoryUploadedFile, TemporaryUploadedFile]:
                raise UnsupportedMediaType("Field: \"image\" should only contain images")
            if img.content_type not in ['image/jpeg', 'image/png', 'image/jpg', 'image/heic']:
                raise UnsupportedMediaType("Unsupported file type, only JPEG, PNG, JPG and HEIC are allowed")
            if img.size > 5 * 1024 * 1024:
                raise ParseError('File too large, each image size should not exceed 5 MiB')
        
        openid = self.get_openid(request)
        match = self.get_match(pk, openid)
        my_index, me, partner = self.get_match_participants(match, openid)
        self.assert_match_auth(match, me)
        
        task = self.get_task(match, day)
        if task is None:
            raise NotFound(f"No Task exist for day {day}")
        
        for img in images:
            data = {
                "task": task,
                "image": img
            }
            image = Image.objects.create(**data)
            image.save()
        return Response({"msg": "Image uploaded"}, status=status.HTTP_201_CREATED)


class ImageDetailView(APIView, UtilMixin):
    def delete(self, request, pk, day, img_pk):
        openid = self.get_openid(request)
        match = self.get_match(pk, openid)
        my_index, me, partner = self.get_match_participants(match, openid)
        self.assert_match_auth(match, me)
        
        task = self.get_task(match, day)
        if task is None:
            raise NotFound(f"No Task exist for day {day}")
        
        image = task.imgs.filter(id=img_pk).first()
        if not image or image.deleted:
            raise NotFound("Image of this ID does not exist")
        print(image)
        image.deleted = True
        image.save()
        return Response({"msg": "Image deleted"}, status=status.HTTP_204_NO_CONTENT)
