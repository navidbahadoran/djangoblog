import datetime
from django.db import models  # <-- This is already in the file
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_date(value):
    if value.year > datetime.datetime.now().year:
        raise ValidationError(
            _('chosen date should be current or older'),
            params={'value': value},
        )
    elif value.year == datetime.datetime.now().year:
        if value.month > datetime.datetime.now().month:
            raise ValidationError(
                _('chosen date should be current or older'),
                params={'value': value},
            )
        elif value.month == datetime.datetime.now().month:
            if value.day > datetime.datetime.now().day:
                raise ValidationError(
                    _('chosen date should be current or older'),
                    params={'value': value},
                )


class Post(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(blank=True, null=True, validators=[validate_date])

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class PostCategory(models.Model):
    category_name = models.ForeignKey('Category', on_delete=models.CASCADE)
    post_name = models.ForeignKey(Post, on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)
    posts = models.ManyToManyField(Post, blank=True, related_name='categories', through=PostCategory)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
