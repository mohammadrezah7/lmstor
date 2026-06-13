from django import forms
from .models import Student
from courses.models import Program
from accommodation.models import Accommodation


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'firstname', 'lastname', 'birthdate', 'gender',
            'nationalid', 'email', 'phonenumber', 'enrollmentyear',
            'programid', 'gpa', 'accommodationid'
        ]
        widgets = {
            'firstname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام دانشجو',
            }),
            'lastname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام خانوادگی',
            }),
            'birthdate': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select',
            }),
            'nationalid': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'کد ملی ۱۰ رقمی',
                'maxlength': '10',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@domain.com',
            }),
            'phonenumber': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '09120000000',
            }),
            'enrollmentyear': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'مثلاً 1403',
            }),
            'programid': forms.Select(attrs={
                'class': 'form-select',
            }),
            'gpa': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'معدل از ۲۰',
                'min': '0',
                'max': '20',
                'step': '0.01',
            }),
            'accommodationid': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
        labels = {
            'firstname': 'نام',
            'lastname': 'نام خانوادگی',
            'birthdate': 'تاریخ تولد',
            'gender': 'جنسیت',
            'nationalid': 'کد ملی',
            'email': 'ایمیل',
            'phonenumber': 'شماره تماس',
            'enrollmentyear': 'سال ورود',
            'programid': 'رشته تحصیلی',
            'gpa': 'معدل',
            'accommodationid': 'خوابگاه',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make some fields optional for edit
        self.fields['birthdate'].required = False
        self.fields['phonenumber'].required = False
        self.fields['gpa'].required = False
        self.fields['accommodationid'].required = False
        
        # Load choices from database
        self.fields['programid'].queryset = Program.objects.all()
        self.fields['programid'].empty_label = '-- انتخاب رشته --'
        self.fields['accommodationid'].queryset = Accommodation.objects.all()
        self.fields['accommodationid'].empty_label = '-- بدون خوابگاه --'
    
    def clean_nationalid(self):
        nationalid = self.cleaned_data.get('nationalid')
        if nationalid and (len(nationalid) != 10 or not nationalid.isdigit()):
            raise forms.ValidationError('کد ملی باید ۱۰ رقم باشد')
        # Check uniqueness excluding current instance
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            exists = Student.objects.filter(nationalid=nationalid).exclude(pk=instance.pk).exists()
        else:
            exists = Student.objects.filter(nationalid=nationalid).exists()
        if exists:
            raise forms.ValidationError('این کد ملی قبلاً ثبت شده است')
        return nationalid
    
    def clean_gpa(self):
        gpa = self.cleaned_data.get('gpa')
        if gpa and (gpa < 0 or gpa > 20):
            raise forms.ValidationError('معدل باید بین ۰ تا ۲۰ باشد')
        return gpa