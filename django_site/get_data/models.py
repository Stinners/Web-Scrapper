from django.db import models

# Create your models here.

class Tag(models.Model):
    tag_name = models.CharField(max_length=50)

class Submission(models.Model):
    # Will need to check that the lengths are appropriate and
    # add checks to the scrapper to ensure nothing overflows them
    name       = models.CharField(max_length=250)
    city       = models.CharField(max_length=50)
    link       = models.CharField(max_length=250)
    extra_info = models.TextField()
    date       = models.DateTimeField(auto_now_add=False)
    tags       = models.ManyToManyField(Tag)
