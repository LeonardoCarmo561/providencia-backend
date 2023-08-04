import os

from django.db import models
from django.core import validators
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from simple_history.models import HistoricalRecords

def upload_profile_picture_location(instance, filename):
    filebase, extension = os.path.splitext(filename)
    return 'users/%s/%s%s' % (instance.username, filebase, extension)

class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, is_superuser, is_staff, **kwargs):
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, username, email, password, **kwargs):
        return self._create_user(username, email, password, False, False, **kwargs)

    def create_superuser(self, username, email, password, **kwargs):
        return self._create_user(username, email, password, True, True, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('Name'),
        max_length=60,
        null=False,
        blank=False,
        validators=[
            validators.RegexValidator(
                regex='^[a-zA-Z\u00C0-\u00FF ]*$',
                message=_('Enter a valid username'),
                code=_('Invalid')
            )
        ]
    )

    email = models.EmailField(_('E-mail'),
        max_length=255,
        unique=True,
        blank=False,
        null=False
    )

    password = models.CharField(_('Password'),
        max_length=255,
        null=False,
        blank=False
    )

    number = models.CharField(_('Phone number'),
        null=True,
        blank=True,
        max_length=15,
    )

    profile_picture = models.ImageField(_('Profile picture'),
        upload_to=upload_profile_picture_location,
        null=True,
    )



    is_superuser = models.BooleanField(_('Superuser'),
        default=False
    )

    is_staff = models.BooleanField(_('staff status'),
        default=False
    )

    is_active = models.BooleanField(_('active'),
        default=True
    )

    created_at = models.DateTimeField(_('Created ad'),
        auto_now_add=True,
        auto_now=False
    )
    
    updated_at = models.DateTimeField(_('Atualizado em'),
        auto_now_add=False,
        auto_now=True
    )

    _historical = HistoricalRecords()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']
    
    objects = UserManager()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        ordering = ['-is_active', 'username']
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self) -> str:
        return self.username
