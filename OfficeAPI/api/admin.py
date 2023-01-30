from django.contrib import admin
from .models import Office, Room, Seat

admin.site.register(Office)
admin.site.register(Room)


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    exclude = ('is_free',)
