from __future__ import unicode_literals

from django.db import models

class WishedForItem(models.Model):
    url = models.URLField(max_length=1000)
    date_added = models.DateTimeField(auto_now_add=True)
    purchased = models.BooleanField(default=False)
    number_wished_for = models.SmallIntegerField(default=1)
    thumbnail = models.ImageField(upload_to="thumbnails/", blank=True)
