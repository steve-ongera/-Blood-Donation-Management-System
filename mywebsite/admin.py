from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Donor, Recipient, BloodInventory, Donation, BloodRequest, Doctor
from django.utils import timezone
from django.utils.safestring import mark_safe

# Unregister default User admin if needed
# admin.site.unregister(User)

# Custom admin classes
class DonorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'blood_group', 'city', 'is_available', 'last_donation_date')
    list_filter = ('blood_group', 'is_available', 'city', 'state')
    search_fields = ('full_name', 'email', 'phone_number', 'username')
    readonly_fields = ('last_donation_date',)
    fieldsets = (
        ('Personal Info', {
            'fields': ('username', 'full_name', 'date_of_birth', 'gender')
        }),
        ('Contact Info', {
            'fields': ('phone_number', 'email', 'address', 'city', 'state', 'zip_code')
        }),
        ('Medical Info', {
            'fields': ('blood_group', 'last_donation_date', 'is_available', 'health_report')
        }),
    )

class RecipientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'blood_group', 'hospital_name', 'required_date')
    list_filter = ('blood_group', 'hospital_name')
    search_fields = ('full_name', 'email', 'phone_number', 'hospital_name')
    fieldsets = (
        ('Personal Info', {
            'fields': ('username', 'full_name', 'date_of_birth', 'gender')
        }),
        ('Medical Needs', {
            'fields': ('blood_group', 'required_date', 'reason')
        }),
        ('Hospital Info', {
            'fields': ('hospital_name', 'doctor_name')
        }),
        ('Contact Info', {
            'fields': ('phone_number', 'email')
        }),
    )

class BloodInventoryAdmin(admin.ModelAdmin):
    list_display = ('blood_group', 'units_available', 'last_updated')
    list_filter = ('blood_group',)
    readonly_fields = ('last_updated',)
    ordering = ('blood_group',)

class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor', 'donation_date', 'blood_group', 'units_donated')
    list_filter = ('donation_date', 'blood_group')
    search_fields = ('donor__full_name', 'notes')
    date_hierarchy = 'donation_date'
    readonly_fields = ('blood_group',)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('donor', 'donation_date', 'units_donated')
        return self.readonly_fields

class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'blood_group', 'units_required', 'request_date', 'status')
    list_filter = ('status', 'blood_group', 'request_date')
    search_fields = ('recipient__full_name', 'hospital_name')
    readonly_fields = ('request_date',)
    actions = ['approve_requests', 'reject_requests']

    def approve_requests(self, request, queryset):
        queryset.update(status='Approved', approved_by=request.user, approved_date=timezone.now())
    approve_requests.short_description = "Mark selected requests as Approved"

    def reject_requests(self, request, queryset):
        queryset.update(status='Rejected', approved_by=request.user, approved_date=timezone.now())
    reject_requests.short_description = "Mark selected requests as Rejected"

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'specialization', 'hospital', 'is_verified', 'joining_date')
    list_filter = ('specialization', 'is_verified', 'hospital')
    search_fields = ('full_name', 'license_number', 'hospital', 'email')
    readonly_fields = ('joining_date', 'image_preview')
    fieldsets = (
        ('Personal Info', {
            'fields': ('username', 'full_name', 'profile_picture', 'image_preview')
        }),
        ('Professional Info', {
            'fields': ('specialization', 'license_number', 'hospital', 'is_verified')
        }),
        ('Contact Info', {
            'fields': ('phone_number', 'email', 'address')
        }),
    )

    def image_preview(self, obj):
        if obj.profile_picture:
            return mark_safe(f'<img src="{obj.profile_picture.url}" width="150" />')
        return "No Image"
    image_preview.short_description = 'Profile Picture Preview'

# Register all models
admin.site.register(Donor, DonorAdmin)
admin.site.register(Recipient, RecipientAdmin)
admin.site.register(BloodInventory, BloodInventoryAdmin)
admin.site.register(Donation, DonationAdmin)
admin.site.register(BloodRequest, BloodRequestAdmin)
admin.site.register(Doctor, DoctorAdmin)

# Optional: Customize the admin site header
admin.site.site_header = "Blood Bank Management System Admin"
admin.site.site_title = "BBMS Admin Portal"
admin.site.index_title = "Welcome to Blood Bank Management System"