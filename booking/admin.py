from django.contrib import admin
from .models import Hotel, Room, Booking, Payment, Review, Picture, RoomPicture

admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(Review)
admin.site.register(Picture)
admin.site.register(RoomPicture)
