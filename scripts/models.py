from django.db import models

# Create your models here.


class ScriptRecord(models.Model):
    script_id = models.CharField( default='-', max_length=64, blank=True)
    path = models.CharField(default='-', max_length=128, blank=True)
    name = models.CharField(default='-', max_length=64)
    category = models.CharField(max_length=64, default='None category')
    description = models.TextField(default='-')
    code = models.TextField(default='#! Empty script')
    last_time_used = models.CharField( default='-', max_length=64, blank=True)
    def __str__(self):
        return self.name