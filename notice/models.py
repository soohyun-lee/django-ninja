from django.db import models

class Notice(models.Model):
    content = models.TextField()
    password = models.CharField(max_length=10, default=None)
    like_count = models.IntegerField(null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'notices'


class User(models.Model):
    name = models.CharField(max_length=50)
    phone = models.IntegerField()

    class Meta:
        db_table = 'users'