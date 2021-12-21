from django.db import models
from django.db.models.deletion import CASCADE


class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100, default=None)
    auth_code = models.CharField(max_length=50, default=None, null=True)
    fcm_token = models.TextField(null=True, default=None)
    
    class Meta:
        db_table = 'users'


class Category(models.Model):
    name = models.CharField(max_length=50, default=None)

    class Meta:
        db_table = 'categories'


class Notice(models.Model):
    content = models.TextField()
    password = models.CharField(max_length=50, default=None)
    like_count = models.IntegerField(null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    
    class Meta:
        db_table = 'notices'


class UserLike(models.Model):
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=CASCADE, null=True)
    
    class Meta:
        db_table = 'user_like'


class Comment(models.Model):
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comments'