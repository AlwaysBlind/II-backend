from django.db import models
from .imageindexer import ImageIndexer
import cv2
from io import BytesIO
from django.core.files import File
import traceback


class IndexedVideo(models.Model):
    title = models.CharField(max_length=255)
    videofile = models.FileField(
        upload_to='videos/', null=True, verbose_name='')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            self.IndexVideo(self.videofile)
        except Exception as e:
            traceback.print_exc()
            print(f"Could not index video. Exception {e} thrown")

    def __str__(self):
        return f'{self.title}: {self.videofile}'

    def IndexVideo(self, videopath):
        process = psutil.Process(os.getpid())
        ii = ImageIndexer(frames_per_image=50)
        for word, image, frame_number in ii.classify_video(videopath):
            imfilename = f'{self.videofile.name.split(r"/")[-1]}'\
                f'_image_{word}_{frame_number}'
            ci = ClassifiedImage(title=imfilename,
                                 classification_label=word,
                                 time=frame_number, associated_video=self)
            imfile = File(BytesIO(self.get_bytes(image)))
            ci.imagefile.save(f'{ci.title}.jpeg', imfile)
            print(f'Saved {ci.title} successfully')

    def get_bytes(self, image):
        return cv2.imencode('.jpeg', image)[1].tostring()


class ClassifiedImage(models.Model):
    title = models.CharField(max_length=255)
    classification_label = models.CharField(max_length=255, default="")
    imagefile = models.ImageField(upload_to='images/')
    time = models.CharField(max_length=255, null=True)
    associated_video = models.ForeignKey(
        IndexedVideo, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}: {self.imagefile}'
# Create your models here.
