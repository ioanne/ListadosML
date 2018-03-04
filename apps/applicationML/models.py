from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Application(models.Model):
    name = models.CharField(max_length=255)
    app_id = models.CharField(max_length=255)
    secret_key = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    authorized = models.BooleanField()

    def __str__(self):
        return '%s' % self.name

    def get_by_user(user):
        data = Application.objects.filter(user=user).first()
        return data

    def get_authorized(user):
        data = Application.objects.filter(user=user, authorized=True).first()
        return data

    def get_by_id(application_id):
        data = Application.objects.get(id=application_id)
        return data

    def get_all():
        data = Application.objects.all()
        return data
