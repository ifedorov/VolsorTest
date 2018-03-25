from django.conf import settings
from rest_framework import serializers


class RateSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=17, decimal_places=8, coerce_to_string=False, min_value=0)
    base = serializers.CharField()
    rate = serializers.CharField()

    def validate_base(self, value):
        if value not in settings.CURRENCY_CODES:
            codes = ', '.join(settings.CURRENCY_CODES)
            raise serializers.ValidationError('This field must be one of - {codes}'.format(codes=codes))
        return value

    def validate_rate(self, value):
        if value not in settings.CURRENCY_CODES:
            codes = ', '.join(settings.CURRENCY_CODES)
            raise serializers.ValidationError('This field must be one of - {codes}'.format(codes=codes))
        return value
