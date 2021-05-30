from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True,default=f'Nice being here!')
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username}'

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Post(models.Model):
    ''' a model for Image posts '''
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to='img/')
    live_link = models.URLField()
    description = models.TextField(blank=True)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    def save_post(self):
        ''' method to save an image post instance '''
        self.save()

    def delete_post(self):
        '''method to delete an image post instance '''
        self.delete()

    @classmethod
    def search_project(cls, search_term):
        ''' method to search projects by title '''
        return cls.objects.filter(title__icontains=search_term).all()    