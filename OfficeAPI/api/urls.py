from django.urls import path

from .views import *

urlpatterns = [
    path('office/', OfficeAPIView.as_view()),
    path('office/<int:pk>/', OfficeAPIDetailView.as_view()),

    path('room/', RoomAPIView.as_view()),
    path('room/available/', RoomAPIAvailableView.as_view()),
    path('room/<int:pk>/', RoomAPIDetailView.as_view()),
    path('room/<int:pk>/seat/', SeatRoomAPIView.as_view()),

    path('seat/', SeatAPIView.as_view()),
    path('seat/available/', SeatAPIAvailableView.as_view()),
    path('seat/<int:pk>/', SeatAPIDetailView.as_view()),

    path('user/<int:pk>/history/', HistoryUserAPIView.as_view())
]
