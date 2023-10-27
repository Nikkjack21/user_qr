from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None, *args, **kwargs):
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password, *args, **kwargs):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_superadmin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Accounts(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=150, unique=True)

    is_superadmin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = MyAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superadmin

    def has_module_perms(self, add_label):
        return True


class ShortenURL(models.Model):
    user = models.ForeignKey(Accounts, on_delete=models.CASCADE, related_name='urls')
    original_url = models.TextField()
    shorten_url = models.TextField(unique=True)
    token = models.CharField(max_length=10)
    qr_image = models.ImageField(upload_to="images/")
    visited_count = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.user.email
