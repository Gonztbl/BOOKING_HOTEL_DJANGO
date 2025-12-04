from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('hotel/<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.user_profile, name='profile'),
    path('room/<int:room_id>/', views.room_detail, name='room_detail'),
    path('book/<int:room_id>/', views.book_room, name='book_room'),
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('make_payment/<int:booking_id>/', views.make_payment, name='make_payment'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('register/', views.register_view, name='register'),
    # === URL MỚI CHO PAYOS ===
    path('payment-return/', views.payment_return_page, name='payment_return'),
    path('payment-cancel/', views.payment_cancel_page, name='payment_cancel'),
    path('payment-webhook/', views.payment_webhook_receiver, name='payment_webhook'),
]
