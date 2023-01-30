from rest_framework import serializers

from .models import Office, Room, Seat, History


class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = "__all__"


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
        read_only_fields = ('free_seats',)


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = "__all__"
        read_only_fields = ('start_booking',)


class HistoryUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = "__all__"
