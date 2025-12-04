from .models import User, Review
from django import forms


class SearchForm(forms.Form):
    keyword = forms.CharField(
        label='Từ khóa (Tên khách sạn)',
        max_length=100,
        required=False
    )
    CITY_CHOICES = [
        ('', '--- Chọn thành phố ---'),
        ('Hà Nội', 'Hà Nội'),
        ('Đà Nẵng', 'Đà Nẵng'),
        ('TPHCM', 'TPHCM'),
    ]

    city = forms.ChoiceField(
        label='Lọc theo thành phố',
        choices=CITY_CHOICES,
        required=False
    )


class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")

    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("confirm_password"):
            raise forms.ValidationError("Mật khẩu nhập lại không khớp.")
        return cleaned_data


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Viết nhận xét của bạn...'}),
        }