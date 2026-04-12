from django.db import models


class Tutor(models.Model):
    """A tutor available for learner support."""
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']
        verbose_name = 'Tutor'
        verbose_name_plural = 'Tutors'

    def __str__(self):
        return f"{self.name} ({self.subject})"
