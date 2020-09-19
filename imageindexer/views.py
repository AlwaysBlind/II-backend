from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import render
from .serializer import IndexedVideoSerializer, ClassifiedImageSerializer
from .models import IndexedVideo, ClassifiedImage
from rest_framework.decorators import action


class IndexedVideoViewSet(viewsets.ModelViewSet):
    queryset = IndexedVideo.objects.all().order_by('title')
    serializer_class = IndexedVideoSerializer

    @action(detail=True)
    def images(self, request, pk=None):
        video = self.get_object()  # retrieve an object by pk provided
        images = video.classifiedimage_set.filter(
            associated_video=video).distinct()
        images_json = ClassifiedImageSerializer(
            images, many=True, context={'request': request})
        return Response(images_json.data)


class ClassifiedImageViewSet(viewsets.ModelViewSet):
    queryset = ClassifiedImage.objects.all().order_by('title')
    serializer_class = ClassifiedImageSerializer

# Create your views here.
