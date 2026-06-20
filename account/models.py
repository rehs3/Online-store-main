from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django_countries.fields import CountryField

from .manager import CustomUserManager

Gender = (
    ("N", "Not specified"),
    ("F", "Female"),
    ("M", "Male"),
)

image = "account_image/default_account_image/Default_avatar_without_gender.png"


class CustomUser(PermissionsMixin, AbstractBaseUser):
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    email = models.EmailField("email address", unique=True)
    user_name = models.CharField(max_length=20)

    country = CountryField()
    city = models.CharField(max_length=15, blank=True, default="Not specified")
    date_joined = models.DateTimeField(default=timezone.now)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=13, choices=Gender, default="Not specified"
    )
    main_image = models.ImageField(default=image, upload_to="account_image/")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["user_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.user_name

    def get_absolute_url(self):
        return reverse("account:profile", args=[self.id])

    @property
    def age(self):
        if not self.birth_date:
            return 0
        today = timezone.now()
        has_had_birthday = (today.month, today.day) < (
            self.birth_date.month,
            self.birth_date.day,
        )
        return today.year - self.birth_date.year - int(has_had_birthday)
