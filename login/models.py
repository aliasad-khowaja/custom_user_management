from django.db import models


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, default='', unique=True)


class User(models.Model):
    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 2
    STATUS_CHOICES = (
        (STATUS_ACTIVE, 'Active'),
        (STATUS_INACTIVE, 'Inactive'),
    )
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, null=False, default='', unique=True)
    password = models.CharField(max_length=500, null=False, default='')
    display_name = models.CharField(max_length=255, null=False, default='')
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
