# from user.views import upload
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True,default=f'Nice being here!')
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    photos = models.ImageField(default='default.jpg', upload_to='img')

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
        return cls.objects.filter(title__icontains=search_term)    


class Rating(models.Model):
    rating = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    )

    design = models.IntegerField(choices=rating, default=0, blank=True)
    usability = models.IntegerField(choices=rating, blank=True)
    content = models.IntegerField(choices=rating, blank=True)
    score = models.FloatField(default=0, blank=True)
    design_average = models.FloatField(default=0, blank=True)
    usability_average = models.FloatField(default=0, blank=True)
    content_average = models.FloatField(default=0, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='rater')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings', null=True)

    def save_rating(self):
        self.save()

    @classmethod
    def get_ratings(cls, id):
        ratings = Rating.objects.filter(post_id=id).all()
        return ratings

    def __str__(self):
        return f'{self.post} Rating'
