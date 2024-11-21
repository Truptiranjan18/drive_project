from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User


class Folder(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subfolders', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='folders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class File(models.Model):
    name = models.CharField(max_length=255)
    folder = models.ForeignKey(Folder, null=True, blank=True, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
