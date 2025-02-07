from django.db import models

# Create your models here.

class candidate(models.Model):
    channel_id = models.CharField(max_length=100, null=False, unique=True, default='')
    
class Channel(models.Model):
    channel_id = models.CharField(max_length=100, null=False, unique=True, default='')
    title = models.CharField(max_length=200, default='')
    profile_image_url = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.title

class Playlist(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='playlists')
    channel_title = models.CharField(max_length=200)
    playlist_id = models.CharField(max_length=100)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title
    
class Video(models.Model):
    Channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='videos', null=True)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='videos')
    video_id = models.CharField(max_length=100)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title    
    
class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    

class Score(models.Model):
    Channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='scores')
    Playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='scores')
    Video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='scores')
    thx_comment = models.IntegerField()    

    def __str__(self):
        return self.thx_comment