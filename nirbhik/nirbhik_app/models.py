from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, username, email, mobile_no, address, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            mobile_no=mobile_no,
            address=address
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, mobile_no, address, password=None):
        user = self.create_user(
            username=username,
            email=email,
            mobile_no=mobile_no,
            address=address,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    mobile_no = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    has_token = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'mobile_no', 'address']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    

User = get_user_model()


class UserLocationRecordTable(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    longitude = models.CharField(max_length=50)
    latitude = models.CharField(max_length=50)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.email} - {self.longitude}, {self.latitude} at {self.timestamp}"
