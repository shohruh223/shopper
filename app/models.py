from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import integer_validator
from django.db.models import SlugField, CharField, CASCADE
from django.utils.text import slugify
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

"""Vedio """

class Category(MPTTModel):
    title = CharField(max_length=55)
    parent = TreeForeignKey('self', on_delete=CASCADE, null=True, blank=True, related_name='children')
    slug = SlugField(max_length=255, unique=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        return f'{self.title}'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.title)
        i = Category.objects.filter(slug=self.slug).count()
        while Category.objects.filter(slug=self.slug).exists():
            self.slug += f'{i}'

        super().save(force_insert, force_update, using, update_fields)


class Product(models.Model):
    class ChoiceSize(models.TextChoices):
        XS = 'xs'
        X = 'x'
        M = 'm'
        L = 'l'
        XL = 'xl'

    class ChoiceColor(models.TextChoices):
        BLACK = 'Black'
        WHITE = 'White'
        RED = 'Red'
        BLUE = 'Blue'
        GREEN = 'Green'

    image = models.ImageField(upload_to='product/')
    title = models.CharField(max_length=155)
    review = models.IntegerField(default=1, null=True, blank=True)
    price = models.FloatField()
    text = models.TextField()
    choice = models.CharField(max_length=55, choices=ChoiceSize.choices, default=ChoiceSize.XL)
    color = models.CharField(max_length=25, choices=ChoiceColor.choices, default=ChoiceColor.WHITE)
    quantity = models.IntegerField(default=1)
    category = models.ForeignKey('app.Category', on_delete=models.CASCADE)


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have a phone number!')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = models.CharField(max_length=155, unique=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=25, validators=[integer_validator], null=True, blank=True)
    address = models.CharField(max_length=155, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()


class Contact(models.Model):
    user = models.ForeignKey('app.User', models.CASCADE, 'contact')
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return f'{self.user} {self.subject}'

