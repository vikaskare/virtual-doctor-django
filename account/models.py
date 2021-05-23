from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=CASCADE, related_name="user")
    mobile = models.CharField(max_length=15, null=True, blank=True)
    age = models.CharField(max_length=3, null=True, blank=True)
    bp_problem = models.CharField(max_length=10, null=True, blank=True)
    blood_group = models.CharField(max_length=10, null=True, blank=True)
    major_health_problem = models.CharField(
        max_length=10, null=True, blank=True)
    city = models.CharField(max_length=225, null=True, blank=True)
    any_operation = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.user.username


class DiseaseHistory(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_disease")
    description = models.TextField(blank=False, null=False)
    remark = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "disease history"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.user.save()
