from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils import timezone



from .manager import UserManager
# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=255, default='')
    email = models.EmailField(max_length=255,unique=True)
    password = models.CharField(max_length=255)
    # phonenumber = models.CharField(max_length=20,default=None)
    phonenumber = models.CharField(max_length=20, default=None, null=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=200 , null=True, blank=True)  
    forgot_token = models.CharField(max_length=128, null=True, blank=True)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('-id',)
        managed = True
        db_table = 'users_user'
        
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)
        
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    
    # def name(self):
    #     return self.name

    def __str__(self):
        return self.email
    
class PendingUser(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=128)
    otp = models.CharField(max_length=200 , null=True, blank=True)  
    created_at = models.DateTimeField(default=timezone.now)

# from django.db import models
# from django.contrib.auth.models import User

from django.db import models

class QueryModel(models.Model):
    user_query = models.TextField()

    def __str__(self):
        return self.user_query
    
from django.db import models

class ChatHistory(models.Model):
    user = models.CharField(max_length=255, default='', null=True)
    user_query = models.TextField()
    generated_sql_query = models.TextField()

    def _str_(self):
        return f"User Query: {self.user_query}, Generated SQL Query: {self.generated_sql_query}, User: {self.user}"


from django.db import models

class QueryRun(models.Model):
    user = models.CharField(max_length=255, default='', null=True)
    user_query = models.TextField()
    generated_sql_query = models.TextField()
    query_result = models.TextField(null=True)  # Store the result of the executed query

    def __str__(self):
        return f"User Query: {self.user_query}, Generated SQL Query: {self.generated_sql_query}, User: {self.user}"
