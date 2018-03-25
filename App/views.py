# Create your views here.
from decimal import Decimal

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from App.models import Rate
from App.serializers import RateSerializer


def convert(amount, base, rate):
    source = Rate.objects.get(target__code=base.value)
    target = Rate.objects.get(target__code=rate.value)
    return ((amount.value / source.rate) * target.rate).quantize(Decimal("0.00000001"))


class ApiRate(APIView):
    """
    Currency conversion.
    """

    def get(self, request):
        serializer = RateSerializer(data=request.query_params)

        if serializer.is_valid():
            result = convert(serializer['amount'], serializer['base'], serializer['rate'])
            return Response({'result': result})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
