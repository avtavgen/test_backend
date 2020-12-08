from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class ApiUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_full_name()


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        ApiUser.objects.create(user=instance)
    instance.apiuser.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Content(models.Model):
    title = models.CharField(max_length=255)
    preview_path = models.CharField(max_length=255)
    file_path = models.CharField(max_length=80)
    description = models.TextField()
    is_premium = models.BooleanField(default=False)
    categories = models.ManyToManyField(Category, related_name='content_categories')

    class Meta:
        verbose_name_plural = "Content"

    def __str__(self):
        return self.title
