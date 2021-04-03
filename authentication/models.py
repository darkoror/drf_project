from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core import validators


class CustomAccountManager(UserManager):

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        user = self.create_user(email=email, username=username, password=password, **extra_fields)
        # user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    # username = models.CharField(max_length=150, unique=True, validators=[UnicodeUsernameValidator])
    username = models.CharField(max_length=150, unique=True)

    email = models.EmailField(verbose_name=_('email address'), max_length=255, unique=True)

    avatar = models.ImageField(upload_to='avatars', null=True, blank=True, max_length=255)

    # birth_year = models.PositiveIntegerField(null=True, blank=True,
    #                                          validators=[
    #                                              validators.MinValueValidator(
    #                                                  limit_value=1900
    #                                              )
    #                                          ])
    # location = models.CharField(max_length=255, null=True, blank=True)

    # annual_income = models.FloatField(null=True, blank=True)

    # industry = models.ForeignKey('industries.Industry', models.SET_NULL, null=True, blank=True)  # Can this be null?
    # financial_goals = models.TextField(null=True, blank=True)

    is_staff = models.BooleanField(default=False,
                                   help_text=_('Designates whether this user can access this admin site.'),
                                   verbose_name=_('is staff'))
    # is_active = models.BooleanField(
    #     default=False,
    #     help_text=_(
    #         'Designates whether this user should be treated as active. '
    #         'Unselect this instead of deleting accounts.'
    #     ),
    #     verbose_name=_('is active')
    # )
    # is_restoring_password = models.BooleanField(
    #     default=False,
    #     help_text=_(
    #         'Designates that this user should confirm email after password reset . '
    #     ),
    #     verbose_name=_('restoring_password')
    # )
    is_superuser = models.BooleanField(default=False,
                                       help_text=_('Designates that this user has all permissions without '
                                                   'explicitly assigning them.'),
                                       verbose_name=_('is superuser'))

    # date_joined = models.DateTimeField(auto_now_add=True, verbose_name=_('date joined'))
    # last_login = models.DateTimeField(_('last login'), blank=True, null=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    def __str__(self):
        return f"{self.id}, {self.email}"

    def has_perm(self, perm, obj=None):
        """
        Return True if the user has the specified permission. Query all
        available auth backends, but return immediately if any backend returns
        True. Thus, a user who has permission from a single auth backend is
        assumed to have permission in general. If an object is provided, check
        permissions for that object.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_staff:
            return True

        # Otherwise we need to check the backends.
        return super().has_perm(perm, obj)

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Second simplest possible answer: yes, if user is staff
        return self.is_staff

    class Meta:
        db_table = 'users'
        verbose_name = _('user')
        verbose_name_plural = _('users')
