from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from datetime import datetime
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
import json
from django.utils import timezone


class UserAccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, first_name, last_name, password, is_staff, is_superuser):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not email:
            raise ValueError('The email address must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff,
                          is_superuser=is_superuser, date_joined=datetime.now())
        user.set_password(password)
        user.save(using=self._db)
        profile = UserProfile(user=user, first_name=first_name, last_name=last_name, birthday=timezone.now(),
                              where_you_live="", introduction="", profile_image_storage_url="")
        profile.save()
        #request.session.modified = True
        return user

    def create_user(self, email=None, first_name=None, last_name=None, password=None):
        print("create_user()")
        return self._create_user(email=email, first_name=first_name, last_name=last_name, password=password, is_staff=False,
                                 is_superuser=False)

    def create_superuser(self, email, password):
        print("create_superuser()")
        first_name = input("Enter last name: ")
        last_name = input("Enter first name: ")
        return self._create_user(email=email, first_name=first_name, last_name=last_name,
                                 password=password, is_staff=True,
                                 is_superuser=True)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    #profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, default=None)
    watch_list = JSONField(default=list)
    hangouts_to_join = JSONField(default=list)

    is_staff = models.BooleanField(default=False,
                                   help_text='Designates whether the user is a team staff.')

    is_superuser = models.BooleanField(default=False,
                                        help_text='Designates whether the user can log into this admin site.')

    date_joined = models.DateTimeField(default=None, help_text="Time when the user account is created.")

    #Tell Django that this User uses UserManager instead of the default BaseUserManager
    objects = UserAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def has_it_in_join_list(self, event_id):
        """
        :param User_obj:
        :param event_id:
        :return: Checks if the user object has event_id in its hangouts_to_join list.
        """
        user_hangouts = self.hangouts_to_join
        if event_id in user_hangouts:
            #print(self, event_id, "in watch_list:", watch_list)
            return True
        else:
            #print(self, event_id, "NOT in watch_list:", watch_list)
            return False


    def has_it_in_watch_list(self, event_id):
        """
        :param User_obj:
        :param event_id:
        :return: Checks if the user object has event_id in its hangouts_to_join list.
        """
        watch_list = self.watch_list
        if event_id in watch_list:
            #print(self, event_id, "in watch_list:", watch_list)
            return True
        else:
            #print(self, event_id, "NOT in watch_list:", watch_list)
            return False


    def add_to_join_list(self, event_id):
        user_hangouts = self.hangouts_to_join
        user_hangouts.append(event_id)
        self.hangouts_to_join = user_hangouts
        print(self, "added", event_id, "to its join list.")
        self.save()

    def remove_from_join_list(self, event_id):
        user_hangouts = self.hangouts_to_join
        user_hangouts.remove(event_id)
        self.hangouts_to_join = user_hangouts
        print(self, "removed", event_id, "from its join list.")
        self.save()

    def add_to_watch_list(self, event_id):
        watch_list = self.watch_list
        watch_list.append(event_id)
        self.watch_list = watch_list
        print(self, "added", event_id, "to its watch list.")
        self.save()

    def remove_from_watch_list(self, event_id):
        watch_list = self.watch_list
        watch_list.remove(event_id)
        self.watch_list = watch_list
        print(self, "removed", event_id, "from its watch list.")
        self.save()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False)
    first_name = models.CharField(blank=False, default="", max_length=30)
    last_name = models.CharField(blank=False, default="", max_length=30)
    middle_name = models.CharField(blank=True, default="", max_length=30)
    birthday = models.DateField(null=True)
    where_you_live = models.CharField(default="", max_length=160)
    introduction = models.CharField(default="", max_length=300)
    profile_image_storage_url = models.CharField(default="", max_length=160, blank=False)


