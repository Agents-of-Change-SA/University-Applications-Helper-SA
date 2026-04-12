from django.conf import settings
from django.db import models


class UserDetails(models.Model):
    """Learner profile: name, surname, age, career aspiration."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='details',
    )
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    career_aspiration = models.CharField(max_length=255, blank=True, default='')

    class Meta:
        ordering = ['name']
        verbose_name = 'User Details'
        verbose_name_plural = 'User Details'

    def __str__(self):
        return f"{self.name} {self.surname}"
