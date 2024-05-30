from django.db import models
from django.core.validators import FileExtensionValidator
import random
from django.utils import timezone
from embed_video.fields import EmbedVideoField
from profiles.models import countryChoice, Profile


def generate_pk():
    number = random.randint(1000, 9999)
    return "{}-{}{}".format("moviemafia", timezone.now().strftime('%y%m%d'), number)


class Category(models.Model):
    name = models.CharField(max_length=40)
    image = models.ImageField(upload_to='Category', validators=[
                              FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank=False)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100)
    year  = models.IntegerField(default=1900)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='gallary', validators=[
        FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank=False)
    video = EmbedVideoField()

    code = models.CharField(default="0000", max_length=255,
                            unique=True,  editable=False)

    liked = models.ManyToManyField(
        Profile, default=None, related_name='likesm', blank=True ,editable = False)
    category = models.ManyToManyField(
        Category, default=None, related_name='catagory', blank=False,)

    rate = models.IntegerField(default=0)

    country = models.CharField(
        max_length=15, choices=countryChoice, default="UNITED STATES")

    language = models.CharField(max_length=20)

    budget = models.IntegerField(default=0)
    collection = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.code = generate_pk()
        super(Movie, self).save(*args, **kwargs)

    def __str__(self):
        return str(f'{self.title}-{self.code}')

    def reviewsCount(self):
        return self.review_set.all().count()
     
    class Meta:
        ordering = ['-created_at']



class Review(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Movie, on_delete=models.CASCADE)
    body = models.TextField()
    liked = models.ManyToManyField(
        Profile, default=None, related_name='likesr', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def repliessCount(self):
        return self.reply_set.all().count()

    def __str__(self):
        return str(self.pk)

    class Meta:
        ordering = ['-created']


class Reply(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment = models.ForeignKey(Review, on_delete=models.CASCADE)
    body = models.TextField()
    liked = models.ManyToManyField(
        Profile, default=None, related_name='likerep', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


     

    def __str__(self):
        return str(self.pk)

    class Meta:
        ordering = ['-created']
