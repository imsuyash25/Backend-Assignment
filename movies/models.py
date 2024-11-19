from django.db import models
import uuid
from accounts.models import User


class BaseModel(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Collection(BaseModel):
    title = models.CharField(max_length=60)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Movie(BaseModel):
    title = models.CharField(max_length=60)
    description = models.TextField(blank=True, null=True)
    genres = models.CharField(max_length=60, blank=True, null=True)
    collection = models.ForeignKey(Collection, related_name='movies',
                                   on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("Movie")
        verbose_name_plural = ("Movies")

    def __str__(self):
        return self.title