# views.py (đã cập nhật)

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Hotel, User, Room, Booking, Payment, RoomPicture, Picture, Review
from django.contrib import messages
from django.contrib.auth import logout
from .forms import SearchForm, RegisterForm, ReviewForm
from django.utils import timezone
from datetime import datetime
from django.core.paginator import Paginator
from django.db.models import Max
from django.utils.timezone import now
import logging

# --- Thêm các import cần thiết cho PayOS ---
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import json
from payos import PayOS
from payos.type import PaymentData, ItemData
from payos.custom_error import PayOSError

# --- Kết thúc phần import cho PayOS ---


# --- Khởi tạo PayOS Client ---
logger = logging.getLogger(__name__)

payos_client = None
if settings.PAYOS_CLIENT_ID and settings.PAYOS_API_KEY and settings.PAYOS_CHECKSUM_KEY:
    try:
        payos_client = PayOS(
            client_id=settings.PAYOS_CLIENT_ID,
            api_key=settings.PAYOS_API_KEY,
            checksum_key=settings.PAYOS_CHECKSUM_KEY
        )
        logger.info("PayOS client initialized successfully.")
    except Exception as e:
        logger.error(f"An unexpected error occurred during PayOS client initialization: {e}")
else:
    logger.warning("PAYOS credentials not found in settings. Payment via PayOS will not be available.")


# --- Kết thúc khởi tạo PayOS Client ---


def logout_view(request):
    # ... (giữ nguyên)
    logout(request)
    return redirect('home')


def login_view(request):
    # ... (giữ nguyên)
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email, password=password)
            request.session['user_id'] = user.user_id
            return redirect('home')
        except User.DoesNotExist:
            messages.error(request, "Sai thông tin đăng nhập")
    return render(request, 'login.html')


def home(request):
    # ... (giữ nguyên)
    hotels = Hotel.objects.all()
    form = SearchForm(request.GET or None)

    if form.is_valid():
        keyword = form.cleaned_data.get('keyword', '').strip().lower()
        city = form.cleaned_data.get('city', '').strip().lower()

        if keyword:
            hotels = hotels.filter(name__icontains=keyword)
        if city:
            filtered_hotels = []
            for hotel in hotels:
                parts = hotel.address.split(',')
                if len(parts) > 1 and parts[-1].strip().lower() == city:
                    filtered_hotels.append(hotel)
            hotels = filtered_hotels

    paginator = Paginator(hotels, 5)
    page_number = request.GET.get('page')
    hotels = paginator.get_page(page_number)

    return render(request, 'home.html', {'hotels': hotels, 'form': form})


def hotel_detail(request, hotel_id):
    # ... (giữ nguyên)
    hotel = Hotel.objects.get(hotel_id=hotel_id)
    rooms = Room.objects.filter(hotel=hotel)
    pictures = Picture.objects.filter(hotel=hotel)
    return render(request, 'hotel_detail.html', {'hotel': hotel, 'rooms': rooms, 'pictures': pictures})


def user_profile(request):
    # ... (giữ nguyên)
    user_id = request.session.get('user_id')
    user = User.objects.get(user_id=user_id)
    return render(request, 'profile.html', {'user': user})


def room_detail(request, room_id):
    # ... (giữ nguyên)
    room = Room.objects.get(room_id=room_id)
    pictures = RoomPicture.objects.filter(room=room)
    reviews = Review.objects.filter(room=room).select_related('user').order_by('-created_at')
    user_id = request.session.get('user_id')
    user = User.objects.filter(user_id=user_id).first() if user_id else None
    if request.method == 'POST' and user:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.room = room
            review.user = user
            review.created_at = now()
            max_id = Review.objects.aggregate(Max('review_id'))['review_id__max'] or 0
            review.review_id = max_id + 1
            review.save()
            return redirect('room_detail', room_id=room_id)
    else:
        form = ReviewForm()
    return render(request, 'room_detail.html',
                  {'room': room, 'pictures': pictures, 'reviews': reviews, 'form': form, 'user': user})


def book_room(request, room_id):
    # ... (giữ nguyên)
    room = Room.objects.get(room_id=room_id)
    if request.method == 'POST':
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login')
        user = User.objects.get(user_id=user_id)
        try:
            check_i = datetime.strptime(check_in, "%Y-%m-%d").date()
            check_o = datetime.strptime(check_out, "%Y-%m-%d").date()
        except ValueError:
            return render(request, 'book_room.html', {'room': room, 'error': 'Vui lòng nhập đúng định dạng ngày.'})
        nights = (check_o - check_i).days
        if nights <= 0:
            return render(request, 'book_room.html', {'room': room, 'error': 'Ngày trả phải sau ngày nhận phòng.'})
        overlap = Booking.objects.filter(room=room, check_in__lt=check_o, check_out__gt=check_i).exists()
        if overlap:
            messages.error(request, "❌ Phòng này đã được đặt trong khoảng thời gian bạn chọn.")
            return redirect('room_detail', room_id=room.room_id)
        total = room.price_per_night * nights
        max_id = Booking.objects.aggregate(Max('booking_id'))['booking_id__max'] or 0
        new_id = max_id + 1
        Booking.objects.create(booking_id=new_id, user=user, room=room, check_in=check_i, check_out=check_o,
                               total=total)
        messages.success(request, "🎉 Đặt phòng thành công!")
        return redirect('my_bookings')
    return render(request, 'book_room.html', {'room': room})


def my_bookings(request):
    # ... (giữ nguyên)
    user = User.objects.get(user_id=request.session.get('user_id'))
    bookings = Booking.objects.filter(user=user)
    return render(request, 'my_bookings.html', {'bookings': bookings})


# --- CẬP NHẬT VIEW make_payment ---
def make_payment(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)

    # ... (code kiểm tra thanh toán giữ nguyên)

    if request.method == 'POST':
        method = request.POST.get('payment_method')

        if method == 'vietqr_payos':
            if not payos_client:
                messages.error(request, "Dịch vụ thanh toán hiện không khả dụng. Vui lòng chọn phương thức khác.")
                return render(request, 'make_payment.html', {'booking': booking})

            try:
                # --- SỬA LẠI DÒNG DESCRIPTION Ở ĐÂY ---
                # Rút gọn description để đảm bảo dưới 25 ký tự.
                # Cú pháp "TT BK" là viết tắt của "Thanh toán Booking".
                # Ví dụ: "TT BK 101"
                description_text = f"TT BK {booking.booking_id}"

                # Cắt bớt nếu vẫn quá dài (phòng trường hợp booking_id quá lớn)
                if len(description_text) > 25:
                    description_text = str(booking.booking_id)[:25]

                logger.info(f"Generated PayOS description: '{description_text}' for booking {booking.booking_id}")
                # --- KẾT THÚC PHẦN SỬA ---

                # Dữ liệu cho PayOS
                payment_data = PaymentData(
                    orderCode=booking.booking_id,
                    amount=int(booking.total*1000),
                    description=description_text,  # <-- SỬ DỤNG BIẾN MỚI
                    items=[ItemData(
                        name=f"Phòng {booking.room.room_type}",
                        quantity=1,
                        price=int(booking.total)
                    )],
                    cancelUrl=request.build_absolute_uri(reverse('payment_cancel')),
                    returnUrl=request.build_absolute_uri(reverse('payment_return')),
                    buyerName=booking.user.name,
                    buyerEmail=booking.user.email,
                    buyerPhone=booking.user.phone
                )

                # Tạo link thanh toán
                create_payment_result = payos_client.createPaymentLink(payment_data)

                if create_payment_result and create_payment_result.checkoutUrl:
                    logger.info(f"PayOS payment link created for booking {booking.booking_id}.")
                    return redirect(create_payment_result.checkoutUrl)
                else:
                    logger.error(f"PayOS: checkoutUrl is invalid for booking {booking.booking_id}.")
                    messages.error(request, "Lỗi tạo link thanh toán. Vui lòng thử lại.")

            except PayOSError as pe:
                logger.error(f"PayOS API Error for booking {booking.booking_id}: {str(pe)}")
                messages.error(request, f"Lỗi từ PayOS: {str(pe)}")
            except Exception as e:
                logger.exception(f"General Error during PayOS link creation for booking {booking.booking_id}: {e}")
                messages.error(request, "Đã xảy ra lỗi không mong muốn. Vui lòng thử lại.")

        else:  # Xử lý các phương thức thanh toán khác (Tiền mặt,...)
            # ... (giữ nguyên phần này)
            max_id = Payment.objects.aggregate(Max('payment_id'))['payment_id__max'] or 0
            new_id = max_id + 1
            Payment.objects.create(
                payment_id=new_id,
                booking=booking,
                payment_method=method,
                payment_date=timezone.now().date(),
                amount=booking.total
            )
            messages.success(request, f"🎉 Đã ghi nhận thanh toán bằng '{method}' thành công!")
            return redirect('my_bookings')

    return render(request, 'make_payment.html', {'booking': booking})
def register_view(request):
    # ... (giữ nguyên)
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            latest_user = User.objects.order_by('-user_id').first()
            next_id = latest_user.user_id + 1 if latest_user else 1
            user = form.save(commit=False)
            user.user_id = next_id
            user.save()
            messages.success(request, "Đăng ký thành công!")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def cancel_booking(request, booking_id):
    # ... (giữ nguyên)
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    booking = get_object_or_404(Booking, pk=booking_id, user_id=user_id)
    if request.method == "POST":
        booking.delete()
    return redirect('my_bookings')


# --- CÁC VIEW MỚI CHO PAYOS ---

@csrf_exempt
def payment_webhook_receiver(request):
    """
    Lắng nghe tín hiệu từ PayOS để cập nhật trạng thái thanh toán.
    Đây là cách xác nhận thanh toán đáng tin cậy nhất.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    if not payos_client:
        logger.error("PayOS client not initialized. Cannot process webhook.")
        return JsonResponse({'error': 'Payment service not configured'}, status=500)

    try:
        webhook_data = json.loads(request.body)
        logger.info(f"Received PayOS webhook: {json.dumps(webhook_data, indent=2)}")

        # TODO: Xác thực chữ ký webhook từ PayOS để tăng cường bảo mật (xem tài liệu của PayOS)

        order_code_str = str(webhook_data.get('orderCode'))
        if not order_code_str:
            logger.error("Webhook data missing 'orderCode'")
            return JsonResponse({'code': '99', 'desc': 'Missing orderCode'}, status=400)

        # Chỉ xử lý khi thanh toán thành công
        if webhook_data.get('code') == '00':
            with transaction.atomic():
                try:
                    booking = Booking.objects.select_for_update().get(booking_id=int(order_code_str))

                    # Kiểm tra xem đã có thanh toán chưa để tránh tạo trùng lặp
                    if Payment.objects.filter(booking=booking).exists():
                        logger.info(f"Booking {order_code_str} already has a payment record. Webhook ignored.")
                        return JsonResponse({'code': '00', 'desc': 'Success (Already processed)'}, status=200)

                    # Tạo bản ghi thanh toán
                    max_id = Payment.objects.aggregate(Max('payment_id'))['payment_id__max'] or 0
                    new_id = max_id + 1
                    Payment.objects.create(
                        payment_id=new_id,
                        booking=booking,
                        payment_method='PayOS',
                        payment_date=timezone.now().date(),
                        amount=booking.total
                    )
                    logger.info(f"Payment record created for booking {order_code_str} via webhook.")

                except Booking.DoesNotExist:
                    logger.error(f"Booking {order_code_str} not found for PayOS webhook.")
                    return JsonResponse({'code': '02', 'desc': 'Order not found'}, status=200)

        return JsonResponse({'code': '00', 'desc': 'Success'}, status=200)

    except json.JSONDecodeError:
        logger.error("Invalid JSON in PayOS webhook request body.")
        return JsonResponse({'code': '99', 'desc': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.exception(f"Error processing PayOS webhook: {str(e)}")
        return JsonResponse({'code': '99', 'desc': 'Internal server error'}, status=500)


def payment_return_page(request):
    """
    Trang mà người dùng được chuyển về sau khi hoàn tất thanh toán trên cổng PayOS.
    Chủ yếu dùng để hiển thị thông báo cho người dùng.
    """
    order_code_str = request.GET.get('orderCode')
    status = request.GET.get('status')

    if not order_code_str:
        messages.error(request, "Không tìm thấy thông tin giao dịch.")
        return redirect('my_bookings')

    if status == 'PAID':
        messages.success(request, f"Giao dịch cho booking #{order_code_str} đã được ghi nhận. Hệ thống đang cập nhật.")
    elif status == 'CANCELLED':
        messages.warning(request, f"Bạn đã hủy thanh toán cho booking #{order_code_str}.")
    else:  # PENDING, FAILED
        messages.error(request, f"Thanh toán cho booking #{order_code_str} không thành công hoặc đang chờ xử lý.")

    return redirect('my_bookings')


def payment_cancel_page(request):
    """
    Trang mà người dùng được chuyển về khi họ nhấn nút "Hủy" trên cổng PayOS.
    """
    order_code_str = request.GET.get('orderCode')
    messages.info(request, f"Giao dịch cho booking #{order_code_str} đã được hủy.")
    return redirect('my_bookings')


# booking/views.py
from .forms import RegisterForm  # Đảm bảo đã import


# ... các view khác

# THÊM HÀM NÀY VÀO CUỐI FILE VIEWS.PY
def register_view(request):
    if request.method == 'POST':
        # Logic xử lý khi người dùng gửi form
        # Lưu ý: form hiện tại của bạn dùng cho User mặc định của Django,
        # trong khi model của bạn lại là User tùy chỉnh.
        # Bạn cần phải viết logic để lưu vào đúng model User của mình.
        # Ví dụ:
        # form = YourCustomRegisterForm(request.POST)
        # if form.is_valid():
        #     user = User.objects.create(...)
        #     return redirect('login')
        pass  # Tạm thời để trống
    else:
        # Khi người dùng truy cập lần đầu
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})