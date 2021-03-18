from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

from django.db import models

from account.models import MyUser


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='likes',
                             on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Category(models.Model):
    slug = models.SlugField(max_length=100,primary_key=True)
    name = models.CharField(max_length=150,unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(MyUser, on_delete= models.CASCADE,related_name ='posts')
    telegram_bot = models.CharField(max_length=100,blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name= 'posts')
    title = models.CharField(max_length=255)
    text = models.TextField()
    draft = models.BooleanField("Черновик", default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    likes = GenericRelation(Like)

    def __str__(self):
        return self.title

    @property
    def total_likes(self):
        return self.likes.count()

class PostImage(models.Model):
    image = models.ImageField(upload_to='posts',blank=True ,null=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='images')



class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='replies')
    body = models.TextField()
    author = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING,related_name='replies')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.post}: {self.body}'


    class Meta:
        ordering = ('-created',)


class Favorite(models.Model):
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE,related_name='favorites')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='favorites')
    favorite = models.BooleanField(default=False)
