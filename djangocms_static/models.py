from django.db import models

# Create your models here.

class RemoteSiteConfig(models.Model):
    """Configuration of remote sites."""

    host = models.CharField(max_length=20)
