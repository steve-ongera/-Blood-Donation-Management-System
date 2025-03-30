# models.py
from django.db import models
from django.contrib.auth.models import User

class Donor(models.Model):
    BLOOD_GROUPS = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    username= models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    last_donation_date = models.DateField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    health_report = models.FileField(upload_to='donor_reports/', null=True, blank=True)
    profile_picture = models.ImageField(upload_to='doner/profile_pictures/', null=True, blank=True)

    def __str__(self):
        return f"{self.full_name} ({self.blood_group})"

class Recipient(models.Model):
    username= models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    blood_group = models.CharField(max_length=3, choices=Donor.BLOOD_GROUPS)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    hospital_name = models.CharField(max_length=100)
    doctor_name = models.CharField(max_length=100)
    required_date = models.DateField()
    reason = models.TextField()
    profile_picture = models.ImageField(upload_to='recipient/profile_pictures/', null=True, blank=True)

    def __str__(self):
        return f"{self.full_name} (Needs {self.blood_group})"

class BloodInventory(models.Model):
    blood_group = models.CharField(max_length=3, choices=Donor.BLOOD_GROUPS)
    units_available = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.blood_group} - {self.units_available} units"

class Donation(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    donation_date = models.DateField()
    blood_group = models.CharField(max_length=3, choices=Donor.BLOOD_GROUPS)
    units_donated = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        # Update inventory when donation is saved
        super().save(*args, **kwargs)
        inventory, created = BloodInventory.objects.get_or_create(blood_group=self.blood_group)
        inventory.units_available += self.units_donated
        inventory.save()

    def __str__(self):
        return f"{self.donor.full_name} donated {self.units_donated} units on {self.donation_date}"

class BloodRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
    ]

    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=3, choices=Donor.BLOOD_GROUPS)
    units_required = models.PositiveIntegerField()
    request_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    approved_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Request for {self.units_required} units of {self.blood_group} by {self.recipient.full_name}"
    


class Doctor(models.Model):
    SPECIALIZATION_CHOICES = [
        ('Hematologist', 'Hematologist'),
        ('General Practitioner', 'General Practitioner'),
        ('Surgeon', 'Surgeon'),
        ('Pediatrician', 'Pediatrician'),
        ('Other', 'Other'),
    ]
    
    username = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES)
    license_number = models.CharField(max_length=50, unique=True)
    hospital = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    profile_picture = models.ImageField(upload_to='doctors/profile_pictures/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    joining_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Dr. {self.full_name} ({self.specialization})"

    @property
    def imageURL(self):
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            return self.profile_picture.url
        else:
            return "/static/images/default_doctor.jpg"  # Default image path