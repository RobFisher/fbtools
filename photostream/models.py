from django.db import models
from fandjango.models import User

class UserState(models.Model):
    fbuser = models.ForeignKey(User)
    current_retrieval_start = models.IntegerField()
    last_photo_retrieval = models.IntegerField()
    last_album_retrieval = models.IntegerField()


class Photo(models.Model):
    user_state = models.ForeignKey(UserState)
    object_id = models.TextField()
    retrieval_time = models.IntegerField()
    name = models.TextField()
    from_name = models.TextField()
    link = models.TextField()
    source = models.TextField()


class Album(models.Model):
    user_state = models.ForeignKey(UserState)
    object_id = models.TextField()
    retrieval_time = models.IntegerField()
    name = models.TextField()
    link = models.TextField()
    
