from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


# Create your models here.

class Channels(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	channelTitle = models.CharField(max_length=50, default='')
	about = models.TextField(default='',max_length=5000)
	def __str__(self):
		return self.channelTitle

class Videos(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	channel = models.ForeignKey(Channels, on_delete=models.CASCADE)
	videoTitle = models.CharField(max_length=200, default='')
	desc = models.TextField(default='',max_length=5000)
	thumbnail = models.ImageField(upload_to='public/videos/thumbnail',max_length=200,default='')
	videoFile = models.FileField(upload_to='public/videos/',max_length=200,default='')
	views = models.IntegerField(default=0)
	datetime = models.DateTimeField(default=now)
	def __str__(self):
		return self.videoTitle

class userHistory(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	vid_id = models.IntegerField()
	datetime = models.DateTimeField(default=now)
	def __str__(self):
		vid = str(self.vid_id)
		return vid