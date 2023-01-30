from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .misc import CURRENT_TIME
from .misc import SeatConfiguration
from .models import User, Office, Room, Seat, History
from .serializers import OfficeSerializer, RoomSerializer, SeatSerializer, HistoryUserSerializer


class OfficeAPIView(generics.ListCreateAPIView):
    queryset = Office.objects.all()
    serializer_class = OfficeSerializer


class OfficeAPIDetailView(generics.RetrieveUpdateAPIView):
    queryset = Office.objects.all()
    serializer_class = OfficeSerializer


class RoomAPIView(APIView):
    def get(self, request, qs=None):
        qs = Room.objects.all() if qs is None else qs
        serializer = RoomSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class RoomAPIAvailableView(RoomAPIView):
    def get(self, request, qs=None):
        qs = Room.objects.filter(free_seats__gt=0)
        return super().get(request, qs)


class RoomAPIDetailView(generics.RetrieveUpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class SeatAPIView(APIView):
    def get(self, request, pk=None, qs=None):
        qs = Seat.objects.all() if qs is None else qs
        serializer = SeatSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request, pk=None, *args, **kwargs):
        serializer = SeatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class SeatAPIAvailableView(SeatAPIView):
    def get(self, request, pk=None, qs=None):
        qs = Seat.objects.filter(is_free=True)
        return super().get(request, pk, qs)


class SeatRoomAPIView(SeatAPIView):
    def get(self, request, pk=None, qs=None):
        room_id = self.kwargs.get('pk')
        qs = Seat.objects.filter(room_id=room_id)
        return super().get(request, pk, qs)

    def post(self, request, pk=None, *args, **kwargs):
        request.data['room'] = pk
        return super().post(request, pk, *args, **kwargs)


class SeatAPIDetailView(APIView):
    def get(self, request, pk, format=None):
        instance = get_object_or_404(Seat, pk=pk)
        serializer = SeatSerializer(instance)
        return Response(serializer.data)

    def put(self, request, pk):
        new_user = User.objects.filter(pk=request.data.get('user')).first()
        seat = SeatConfiguration(request, pk)

        if not new_user and seat.instance.is_free:  # IF NO USER AND SEAT FREE
            return Response(**seat.seat_free_notification())

        elif not new_user and not seat.instance.is_free:  # IF NO USER AND SEAT BUSY
            seat.update_seat_instance(user_id=None,
                                      start_booking=None,
                                      end_booking=None)
            return Response(**seat.seat_vacated_notification())

        elif new_user and not seat.instance.user:  # IF NEW USER AND SEAT EMPTY
            seat.reduce_room_free_seats()
            seat.update_seat_instance(user_id=new_user.id,
                                      start_booking=CURRENT_TIME,
                                      end_booking=seat.get_end_booking())
            seat.save_user_history(new_user)

        elif new_user and seat.instance.user and new_user != seat.instance.user:  # IF NEW USER AND SEAT BUSY

            if seat.is_booked_time():  # IF SEAT IS BUSY BY TIME
                return Response(**seat.seat_busy_error())

            else:
                seat.update_seat_instance(user_id=new_user.id,
                                          start_booking=CURRENT_TIME,
                                          end_booking=seat.get_end_booking())
                seat.save_user_history(new_user)

        serializer = SeatSerializer(instance=seat.instance,
                                    data=request.data,
                                    partial=True)

        if serializer.is_valid():
            return Response(serializer.data)

        return Response(data=serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        seat = SeatConfiguration(request, pk)
        seat.reduce_room_free_seats()
        seat.instance.delete()
        return Response(**seat.seat_delete_notification())


class HistoryUserAPIView(APIView):
    def get(self, request, pk):
        qs = History.objects.filter(user_id=pk).select_related('user')
        return Response({f"history": HistoryUserSerializer(qs, many=True).data})
