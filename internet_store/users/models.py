from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class MyUsersManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, card_number, is_active=True, password=None):
        if not email:
            raise ValueError('The user must have an email address.')
        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            card_number = card_number,
            is_active = is_active
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, card_number, password=None):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            card_number=card_number,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

class Users(AbstractBaseUser):
    first_name = models.CharField(verbose_name='First Name', max_length=50)
    last_name = models.CharField(verbose_name='Last Name', max_length=50)
    email = models.EmailField(verbose_name='User Email', unique=True)
    card_number = models.CharField(verbose_name='Card Number', max_length=100, null=True, blank=True)

    #required
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Registration date')
    last_login = models.DateTimeField(null=True, blank=True, verbose_name='Last entry')
    is_admin = models.BooleanField(default=False, verbose_name='Admin')
    is_staff = models.BooleanField(default=False, verbose_name='Staff')
    is_active = models.BooleanField(default=False, verbose_name='Active')
    is_superuser = models.BooleanField(default=False, verbose_name='Super user ')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'card_number']

    objects = MyUsersManager()

    def __str__(self):
        return self.first_name
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

    def get_absolute_url(self):
        return f'/users/{self.id}'
    
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"