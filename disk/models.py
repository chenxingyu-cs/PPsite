from django.db import models

import datetime
from django.db import models

class Project(models.Model):
    user_id = models.CharField(max_length = 30)
    project_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    mod_date = models.DateTimeField('date modified')


class Version(models.Model):
    project = models.ForeignKey(Project)
    version_name = models.CharField(max_length=200)
    upload_date = models.DateTimeField('date uploaded')
    head_img = models.FileField()
