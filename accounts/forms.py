from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        label='کد ملی (دانشجو) / ایمیل (استاد)',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'کد ملی یا ایمیل خود را وارد کنید',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور (ایمیل)',
        })
    )
    remember_me = forms.BooleanField(
        label='مرا به خاطر بسپار',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )