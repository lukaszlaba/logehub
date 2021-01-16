from django.db import models

# Create your models here.


class ScriptRecord(models.Model):
    name = models.CharField(max_length=64)
    category = models.CharField(max_length=64, default='None category')
    description = models.TextField(default='-')
    code = models.TextField(default='#! Empty script')

    def __str__(self):
        return self.name