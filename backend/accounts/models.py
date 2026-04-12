from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Extended user model for Univice learners."""

    class Meta:
        ordering = ['username']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username
