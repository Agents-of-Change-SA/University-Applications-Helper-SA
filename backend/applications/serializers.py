from rest_framework import serializers

from .models import ApplicationEntry


class ApplicationEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationEntry
        fields = [
            'id',
            'institution_name',
            'open_date',
            'close_date',
            'application_fee',
            'portal_url',
        ]

    def validate(self, data):
        open_date = data.get('open_date')
        close_date = data.get('close_date')
        if open_date and close_date and open_date > close_date:
            raise serializers.ValidationError(
                {'close_date': 'Close date must be on or after open date.'}
            )
        return data
