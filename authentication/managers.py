from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        user = self.create_user(email=email, username=username, password=password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
