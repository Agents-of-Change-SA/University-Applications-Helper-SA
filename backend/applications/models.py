from django.core.exceptions import ValidationError
from django.db import models


class ApplicationEntry(models.Model):
    """An institution's application period with dates, fee, and portal link."""
    institution_name = models.CharField(max_length=255)
    open_date = models.DateField()
    close_date = models.DateField()
    application_fee = models.DecimalField(max_digits=10, decimal_places=2)
    portal_url = models.URLField(max_length=500)

    class Meta:
        ordering = ['institution_name']
        verbose_name = 'Application Entry'
        verbose_name_plural = 'Application Entries'

    def __str__(self):
        return self.institution_name

    def clean(self):
        if self.open_date and self.close_date and self.open_date > self.close_date:
            raise ValidationError(
                {'close_date': 'Close date must be on or after open date.'}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
