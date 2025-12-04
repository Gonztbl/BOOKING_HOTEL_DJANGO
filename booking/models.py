from django.db import models

class Hotel(models.Model):
    hotel_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    description = models.CharField(max_length=300)

    class Meta:
        managed = False
        db_table = 'HOTELS'

class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'USERS'

class Room(models.Model):
    room_id = models.IntegerField(primary_key=True)
    room_number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=50)
    price_per_night = models.FloatField()
    max_occupancy = models.IntegerField()
    description = models.CharField(max_length=300)
    status = models.CharField(max_length=50)
    hotel = models.ForeignKey(Hotel, on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ROOMS'

class Booking(models.Model):
    booking_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    room = models.ForeignKey(Room, on_delete=models.DO_NOTHING)
    check_in = models.DateField()
    check_out = models.DateField()
    total = models.FloatField()

    class Meta:
        managed = False
        db_table = 'BOOKINGS'

class Payment(models.Model):
    payment_id = models.IntegerField(primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.DO_NOTHING)
    payment_method = models.CharField(max_length=50)
    payment_date = models.DateField()
    amount = models.FloatField()

    class Meta:
        managed = False
        db_table = 'PAYMENTS'

class Review(models.Model):
    review_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    room = models.ForeignKey(Room, on_delete=models.DO_NOTHING)
    rating = models.IntegerField()
    comment = models.CharField(max_length=500)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'REVIEWS'

class Picture(models.Model):
    Hpicture_id = models.IntegerField(primary_key=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.DO_NOTHING, db_column='hotel_id')
    image_url = models.CharField(max_length=200)
    description = models.CharField(max_length=300)

    class Meta:
        managed = False
        db_table = 'PICTURES'

class RoomPicture(models.Model):
    picture_id = models.IntegerField(primary_key=True)
    room = models.ForeignKey('Room', on_delete=models.DO_NOTHING, db_column='room_id')
    picture_url = models.CharField(max_length=200)
    number = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Room_pictures'
        unique_together = (('picture_id', 'room'),)
