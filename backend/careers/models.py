from django.conf import settings
from django.db import models


class CareerAspiration(models.Model):
    """A saved career goal for a learner."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='career_aspirations',
    )
    aspiration = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Career Aspiration'
        verbose_name_plural = 'Career Aspirations'

    def __str__(self):
        return self.aspiration


class CareerGuidanceEntry(models.Model):
    """Subject recommendation for a career aspiration."""
    aspiration = models.CharField(max_length=255, db_index=True)
    subject = models.CharField(max_length=100)
    explanation = models.TextField()

    class Meta:
        ordering = ['aspiration', 'subject']
        verbose_name = 'Career Guidance Entry'
        verbose_name_plural = 'Career Guidance Entries'

    def __str__(self):
        return f"{self.aspiration} → {self.subject}"
