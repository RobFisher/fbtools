from django.db import models
from fandjango.models import User

class UserState(models.Model):
    fbuser = models.ForeignKey(User)
    current_retrieval_start = models.IntegerField()
    last_photo_retrieval = models.IntegerField()
    last_album_retrieval = models.IntegerField()
    def __unicode__(self):
        return self.fbuser.full_name


class Photo(models.Model):
    user_state = models.ForeignKey(UserState)
    object_id = models.TextField()
    retrieval_time = models.IntegerField()
    name = models.TextField()
    from_name = models.TextField()
    link = models.TextField()
    source = models.TextField()
    def __unicode__(self):
        return self.from_name + ' : ' + self.name


class Album(models.Model):
    user_state = models.ForeignKey(UserState)
    object_id = models.TextField()
    retrieval_time = models.IntegerField()
    name = models.TextField()
    link = models.TextField()
    def __unicode__(self):
        return self.name
