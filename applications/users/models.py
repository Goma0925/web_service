from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from datetime import datetime
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField


class UserAccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, is_staff, is_superuser):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not email:
            raise ValueError('The email address must be set')
        username = email.split("@")[0]
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, is_staff=is_staff,
                          is_superuser=is_superuser, date_joined=datetime.now())
        user.set_password(password)
        user.save(using=self._db)
        #request.session.modified = True
        return user

    def create_user(self, email=None, password=None):
        print("create_user()")
        return self._create_user(email=email, password=password, is_staff=False,
                                 is_superuser=False)

    def create_superuser(self, email, password):
        print("create_superuser()")
        return self._create_user(email=email, password=password, is_staff=True,
                                 is_superuser=True)


#Define a table here
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(default="", max_length=30)
    self_introduction = models.CharField(default="", max_length=280)
    #watch_list = models.CharField(default="", max_length=)
    joined_hangouts = JSONField(default=list)

    is_staff = models.BooleanField(default=False,
                                   help_text='Designates whether the user is a team staff.')

    is_superuser = models.BooleanField(default=False,
                                        help_text='Designates whether the user can log into this admin site.')

    date_joined = models.DateTimeField(default=None, help_text="Time when the user account is created.")

    #Tell Django that this User uses UserManager instead of the default BaseUserManager
    objects = UserAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

