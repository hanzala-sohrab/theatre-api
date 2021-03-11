from rest_framework import serializers
from seat.models import Seat


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        extra_kwargs = {
            'seatNum': {'read_only': True},
            'status': {'read_only': True}
        }
        fields = ['name', 'seatNum', 'ticketID', 'status']
