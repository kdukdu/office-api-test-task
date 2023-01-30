from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.generics import get_object_or_404

from .models import Seat, History

CURRENT_TIME = timezone.now()
DEFAULT_TIME_BOOKING = CURRENT_TIME + timedelta(hours=1)


class SeatMessages:
    def __init__(self, instance):
        self.instance = instance

    def seat_busy_error(self):
        response = {
            "data": {"error": f"Seat #{self.instance.id} is already taken by {self.instance.user.username}"},
            "status": status.HTTP_403_FORBIDDEN
        }
        return response

    def seat_vacated_notification(self):
        response = {
            "data": {"success": f"Seat #{self.instance.id} successfully vacated"},
            "status": status.HTTP_204_NO_CONTENT
        }
        return response

    def seat_free_notification(self):
        response = {
            "data": {"success": f"Seat #{self.instance.id} is free! You can take it"},
            "status": status.HTTP_204_NO_CONTENT
        }
        return response

    def seat_delete_notification(self):
        response = {
            "data": {"success": f"Seat successfully deleted"},
            "status": status.HTTP_204_NO_CONTENT
        }
        return response


class SeatConfiguration(SeatMessages):
    def __init__(self, request, pk):
        self.request = request
        self.pk = pk
        self.instance = self.__get_instance()
        super().__init__(self.instance)

    def __get_instance(self):
        return get_object_or_404(Seat, pk=self.pk)

    def get_end_booking(self):
        end_booking = self.request.data.get('end_booking')
        if end_booking is None:
            end_booking = DEFAULT_TIME_BOOKING
        self.request.data['end_booking'] = end_booking
        return end_booking

    def increase_room_free_seats(self):
        room = self.instance.room
        room.free_seats += 1
        room.save()

    def reduce_room_free_seats(self):
        room = self.instance.room
        room.free_seats -= 1
        room.save()

    def __save(self):
        self.instance.save()

    def is_booked_time(self):
        return self.instance.end_booking > CURRENT_TIME

    def update_seat_instance(self, user_id=None, start_booking=None, end_booking=None):
        self.increase_room_free_seats()
        self.instance.user_id = user_id
        self.instance.start_booking = start_booking
        self.instance.end_booking = end_booking
        self.__save()

    def save_user_history(self, new_user):
        History.objects.create(user=new_user,
                               room=self.instance.room,
                               seat=self.instance,
                               start_booking=CURRENT_TIME,
                               end_booking=self.get_end_booking())
