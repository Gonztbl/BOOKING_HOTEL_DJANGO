# BookingHotel/urls.py (Phiên bản cuối cùng)

"""
URL configuration for BookingHotel project.
... (phần comment của bạn) ...
"""

from django.contrib import admin
from django.urls import path, include

# BƯỚC 1: BỔ SUNG 2 DÒNG IMPORT NÀY
from django.conf import settings
from django.conf.urls.static import static

# Đoạn urlpatterns của bạn được giữ nguyên
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('booking.urls')),
]

# BƯỚC 2: BỔ SUNG KHỐI LỆNH NÀY VÀO CUỐI FILE
if settings.DEBUG:
    # Dòng này sẽ bảo Django phục vụ các file ảnh mà người dùng upload
    # trong môi trường phát triển (development).
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)