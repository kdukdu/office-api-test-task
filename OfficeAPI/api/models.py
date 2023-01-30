from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Office(models.Model):
    name = models.CharField(max_length=50, null=False)
    address = models.CharField(max_length=100, null=False)

    objects = models.Manager()

    def __str__(self):
        return f'{self.name} - {self.address}'


class Room(models.Model):
    name = models.CharField(max_length=50)
    free_seats = models.IntegerField(default=0, null=False, blank=False)
    office = models.ForeignKey(Office, on_delete=models.CASCADE, related_name='rooms')

    objects = models.Manager()

    def __str__(self):
        return f"{self.name}"


class Seat(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='seats')
    is_free = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    start_booking = models.DateTimeField(null=True, blank=True)
    end_booking = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        string = f"Seat {self.id}. Is free: {self.is_free}."
        book_info = f" {self.start_booking} - {self.end_booking}. {self.user}"
        return string if not self.start_booking else string + book_info

    def save(self, *args, **kwargs):
        self.is_free = not bool(self.user)
        seats_query = Seat.objects.filter(room=self.room)
        super().save(*args, **kwargs)
        self.room.free_seats = seats_query.filter(is_free=True).count()
        self.room.save()


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='histories')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='histories')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name='histories')
    start_booking = models.DateTimeField(null=True, blank=True)
    end_booking = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return f"History for {self.user.username}"
