from django.contrib.auth.models import (
    AbstractBaseUser,
    Permission,
    UserManager,
    BaseUserManager,
    )
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    # Implementation based on:
    # https://github.com/django/django/blob/a9093dd3763df6b2045a08b0520f248bda708723/django/contrib/auth/models.py#L162
    # But with the 'username' field dropped ('email' is used as username field)

    def _create_user(self, email, password,
                     is_staff, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True,
                                 **extra_fields)


class CustomUser(AbstractBaseUser):
    """
    Some of this was copied from:
    https://github.com/django/django/blob/master/django/contrib/auth/models.py#L353
    """
    first_name = models.CharField(max_length=255, blank=True)

    last_name = models.CharField(max_length=255, blank=True)

    title = models.CharField(max_length=255, blank=True)

    email = models.EmailField('email address', max_length=255,
                              blank=True, unique=True)

    is_staff = models.BooleanField('staff status', default=False,
                help_text='Designates whether the user can log into this admin '
                          'site.')

    is_active = models.BooleanField('active', default=True,
                help_text='Designates whether this user should be treated as '
                          'active. Unselect this instead of deleting accounts.')

    date_joined = models.DateTimeField('date joined', default=timezone.now)

    permissions = models.ManyToManyField(Permission,
                                         related_name="auth_user_set",
                                         blank=True)

    is_demo = models.BooleanField(default=False, verbose_name='Demo Account?')

    phone_number = models.CharField(max_length=255, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        app_label = 'tests'
        abstract = False

    def has_perm(self, perm, obj=None):
        print "has_perm: {}, {}".format(perm, obj)

        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    def get_full_name(self):
        return u"{} {}".format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.get_full_name()
