from django import forms
from .models import *
from django import forms
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class SimpleRegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter any password',
            'class': 'form-control'
        }),
        min_length=4,
        required=True
    )
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm password',
            'class': 'form-control'
        }),
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Username',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email address',
                'class': 'form-control'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and password != confirm_password:
            raise ValidationError("Passwords don't match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = [
            'username', 'full_name', 'date_of_birth', 'gender', 'blood_group',
            'phone_number', 'email', 'address', 'city', 'state', 'zip_code',
            'last_donation_date', 'is_available', 'health_report', 'profile_picture'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ZIP Code'}),
            'last_donation_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'health_report': forms.FileInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }


from django import forms
from .models import Recipient

class RecipientForm(forms.ModelForm):
    required_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d']
    )
    
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d']
    )

    class Meta:
        model = Recipient
        fields = '__all__'
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})



from django import forms
from .models import Donation

class DonationForm(forms.ModelForm):
    donation_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d']
    )
    
    class Meta:
        model = Donation
        fields = '__all__'
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['donor'].queryset = Donor.objects.filter(is_available=True)


from django import forms
from .models import BloodRequest

class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ['recipient', 'blood_group', 'units_required', 'status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})



from django import forms
from .models import Doctor

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'
        widgets = {
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})