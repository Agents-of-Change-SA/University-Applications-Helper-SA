from django.conf import settings
from django.db import models


class SchoolProfile(models.Model):
    """Learner's school name and subjects with marks."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='school_profile',
    )
    school_name = models.CharField(max_length=255)

    class Meta:
        ordering = ['school_name']
        verbose_name = 'School Profile'
        verbose_name_plural = 'School Profiles'

    def __str__(self):
        return self.school_name


class SchoolSubject(models.Model):
    """A single subject entry within a school profile."""
    profile = models.ForeignKey(
        SchoolProfile,
        on_delete=models.CASCADE,
        related_name='subjects',
    )
    name = models.CharField(max_length=100)
    percentage = models.IntegerField()
    level = models.IntegerField()

    class Meta:
        ordering = ['name']
        verbose_name = 'School Subject'
        verbose_name_plural = 'School Subjects'

    def __str__(self):
        return f"{self.name} ({self.percentage}%)"
