from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

from choises import USER_TYPES, USER_TYPE_TEAM_WORKER


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError(u'Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email, username=username, password=password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True, blank=False, null=False)
    account_type = models.CharField(max_length=256, choices=USER_TYPES, default=USER_TYPE_TEAM_WORKER)

    objects = CustomUserManager()

    USERNAME_FIELD = u'username'
    REQUIRED_FIELDS = [u'account_type']

    class Meta:
        verbose_name = u'User'
        verbose_name_plural = u'Users'

    def __unicode__(self):
        return unicode(self.username)

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

CustomUser._meta.get_field('password').max_length = 256
