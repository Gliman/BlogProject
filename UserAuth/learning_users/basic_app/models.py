from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfileInfo(models.Model):

    user = models.OneToOneField(User, on_delete=models.DO_NOTHING,)#you don't have any special requirements for on_delete, you could use the option DO_NOTHING,)

    portfolio_site = models.URLField(blank = True)

    profolio_pic = models.ImageField(upload_to = 'profile_pics', blank = True )

    def __str__(self):
        return self.user.username
