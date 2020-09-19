from .models import IndexedVideo, ClassifiedImage
from rest_framework import serializers


class IndexedVideoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = IndexedVideo
        fields = ('videofile', 'id', 'title', 'url')


class ClassifiedImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClassifiedImage
        fields = ('imagefile', 'id', 'title', 'url',
                  'classification_label', 'associated_video')
