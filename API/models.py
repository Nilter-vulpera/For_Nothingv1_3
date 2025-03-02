from django.db import models
class Song(models.Model):
    song = models.FileField(blank=True,null=True, upload_to="media/audio")
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    album = models.CharField(max_length=255, blank=True)
    release_date = models.DateField(null=True, blank=True)

    def str(self):
        return f"{self.title} by {self.artist}"
# Create your models here.
