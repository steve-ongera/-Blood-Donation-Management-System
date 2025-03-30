from django.shortcuts import render
from mywebsite.models import *
from django.shortcuts import render
from django.core.paginator import Paginator
from mywebsite.models import Donor
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import SimpleRegisterForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = SimpleRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Auto-login after registration
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = SimpleRegisterForm()

    return render(request, 'auth/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            remember = request.POST.get('remember')
            if remember:
                request.session.set_expiry(1209600)  # 2 weeks
            
            messages.success(request, 'logged in successfully welcome back.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'auth/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

def donor_list(request):
    query = request.GET.get('q', '')  # Get search query from request

    if query:
        donors = Donor.objects.filter(
            full_name__icontains=query
        ) | Donor.objects.filter(
            blood_group__icontains=query
        ) | Donor.objects.filter(
            city__icontains=query
        )
    else:
        donors = Donor.objects.all()  # Ensure donors is always assigned

    # Pagination setup (show 10 donors per page)
    paginator = Paginator(donors, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'donors/donor_list.html', {'page_obj': page_obj , 'query': query})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Donor
from .forms import DonorForm


# View Single Donor Details
def donor_detail(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    return render(request, 'donors/donor_detail.html', {'donor': donor})

# Add a New Donor
def donor_add(request):
    if request.method == "POST":
        form = DonorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('donor_list')
    else:
        form = DonorForm()
    return render(request, 'donors/donor_form.html', {'form': form})

# Update Donor Information
def donor_update(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    if request.method == "POST":
        form = DonorForm(request.POST, request.FILES, instance=donor)
        if form.is_valid():
            form.save()
            return redirect('donor_list')
    else:
        form = DonorForm(instance=donor)
    return render(request, 'donors/donor_form.html', {'form': form})

# Delete a Donor
def donor_delete(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    if request.method == "POST":
        donor.delete()
        return redirect('donor_list')
    return render(request, 'donors/donor_confirm_delete.html', {'donor': donor})


from django.shortcuts import render
from .models import Donor, Recipient, BloodInventory, Donation, BloodRequest

def dashboard(request):
    # Get counts for summary cards
    donor_count = Donor.objects.count()
    recipient_count = Recipient.objects.count()
    
    # Blood inventory data
    blood_inventory = BloodInventory.objects.all().order_by('blood_group')
    total_units = sum(item.units_available for item in blood_inventory)
    max_units = max(item.units_available for item in blood_inventory) if blood_inventory else 0
    
    # Get pending requests count
    pending_requests = BloodRequest.objects.filter(status='Pending').count()
    
    # Get recent activities
    recent_donations = Donation.objects.select_related('donor').order_by('-donation_date')[:5]
    recent_requests = BloodRequest.objects.select_related('recipient').order_by('-request_date')[:5]
    
    context = {
        'donor_count': donor_count,
        'recipient_count': recipient_count,
        'blood_inventory': blood_inventory,
        'total_units': total_units,
        'max_units': max_units,
        'pending_requests': pending_requests,
        'recent_donations': recent_donations,
        'recent_requests': recent_requests,
    }
    
    return render(request, 'dashboard/admin_dashboard.html', context)



from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Recipient

def recipient_list(request):
    query = request.GET.get('q', '')
    
    if query:
        recipients = Recipient.objects.filter(
            models.Q(full_name__icontains=query) |
            models.Q(hospital_name__icontains=query) |
            models.Q(blood_group__icontains=query)
        ).order_by('-required_date')
    else:
        recipients = Recipient.objects.all().order_by('-required_date')
    
    paginator = Paginator(recipients, 10)  # Show 10 recipients per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'recipients': page_obj,
        'page_obj': page_obj,
        'is_paginated': paginator.num_pages > 1,
    }
    return render(request, 'receivers/recipient_list.html', context)


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Recipient
from .forms import RecipientForm  # We'll create this form next

def recipient_detail(request, pk):
    """
    View to display detailed information about a recipient
    """
    recipient = get_object_or_404(Recipient, pk=pk)
    context = {
        'recipient': recipient,
        'title': f'Recipient Details - {recipient.full_name}'
    }
    return render(request, 'receivers/recipient_detail.html', context)

def edit_recipient(request, pk):
    """
    View to edit an existing recipient
    """
    recipient = get_object_or_404(Recipient, pk=pk)
    
    if request.method == 'POST':
        form = RecipientForm(request.POST, request.FILES, instance=recipient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Recipient updated successfully!')
            return redirect('recipient_detail', pk=recipient.id)
    else:
        form = RecipientForm(instance=recipient)
    
    context = {
        'form': form,
        'title': f'Edit Recipient - {recipient.full_name}',
        'recipient': recipient
    }
    return render(request, 'receivers/recipient_form.html', context)

def delete_recipient(request, pk):
    """
    View to delete a recipient (with confirmation)
    """
    recipient = get_object_or_404(Recipient, pk=pk)
    
    if request.method == 'POST':
        recipient.delete()
        messages.success(request, 'Recipient deleted successfully!')
        return redirect('recipient_list')
    
    context = {
        'recipient': recipient,
        'title': f'Delete Recipient - {recipient.full_name}'
    }
    return render(request, 'receivers/recipient_confirm_delete.html', context)


def add_recipient(request):
    if request.method == 'POST':
        form = RecipientForm(request.POST, request.FILES)
        if form.is_valid():
            recipient = form.save()
            messages.success(request, f'Recipient {recipient.full_name} added successfully!')
            return redirect('recipient_detail', pk=recipient.id)
    else:
        form = RecipientForm()
    
    context = {
        'form': form,
        'title': 'Add New Recipient'
    }
    return render(request, 'receivers/recipient_form.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Donation, Donor, BloodInventory
from .forms import DonationForm

def donation_list(request):
    donations = Donation.objects.all().order_by('-donation_date')
    context = {'donations': donations}
    return render(request, 'donations/donation_list.html', context)

def donation_detail(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    context = {'donation': donation}
    return render(request, 'donations/donation_detail.html', context)

def donation_create(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save()
            messages.success(request, 'Donation record created successfully!')
            return redirect('donation_detail', pk=donation.pk)
    else:
        form = DonationForm()
    
    context = {'form': form, 'title': 'Add New Donation'}
    return render(request, 'donations/donation_form.html', context)

def donation_update(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    
    if request.method == 'POST':
        form = DonationForm(request.POST, instance=donation)
        if form.is_valid():
            # Get original units before update
            original_units = donation.units_donated
            donation = form.save()
            
            # If units changed, update inventory
            if original_units != donation.units_donated:
                inventory = BloodInventory.objects.get(blood_group=donation.blood_group)
                inventory.units_available += (donation.units_donated - original_units)
                inventory.save()
            
            messages.success(request, 'Donation record updated successfully!')
            return redirect('donation_detail', pk=donation.pk)
    else:
        form = DonationForm(instance=donation)
    
    context = {'form': form, 'title': 'Edit Donation', 'donation': donation}
    return render(request, 'donations/donation_form.html', context)

def donation_delete(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    
    if request.method == 'POST':
        # Update inventory before deletion
        inventory = BloodInventory.objects.get(blood_group=donation.blood_group)
        inventory.units_available -= donation.units_donated
        inventory.save()
        
        donation.delete()
        messages.success(request, 'Donation record deleted successfully!')
        return redirect('donation_list')
    
    context = {'donation': donation}
    return render(request, 'donations/donation_confirm_delete.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import BloodRequest, Recipient
from .forms import BloodRequestForm

@login_required
def bloodrequest_list(request):
    requests = BloodRequest.objects.all().order_by('-request_date')
    return render(request, 'bloodrequests/request_list.html', {'requests': requests})

@login_required
def bloodrequest_detail(request, pk):
    blood_request = get_object_or_404(BloodRequest, pk=pk)
    return render(request, 'bloodrequests/request_detail.html', {'request': blood_request})

@login_required
def bloodrequest_create(request):
    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            blood_request = form.save()  # Save the form first to get the pk
            messages.success(request, 'Blood request created successfully!')
            return redirect('bloodrequest_detail', pk=blood_request.pk)  # Now we have the pk
    else:
        form = BloodRequestForm()
    
    return render(request, 'bloodrequests/request_form.html', {
        'form': form,
        'title': 'Create Blood Request'
    })

@login_required
def bloodrequest_update(request, pk):
    blood_request = get_object_or_404(BloodRequest, pk=pk)
    if request.method == 'POST':
        form = BloodRequestForm(request.POST, instance=blood_request)
        if form.is_valid():
            if form.cleaned_data['status'] == 'Approved' and blood_request.status != 'Approved':
                form.instance.approved_by = request.user
            form.save()
            messages.success(request, 'Blood request updated successfully!')
            return redirect('bloodrequest_detail', pk=blood_request.pk)
    else:
        form = BloodRequestForm(instance=blood_request)
    
    return render(request, 'bloodrequests/request_form.html', {
        'form': form,
        'title': 'Update Blood Request',
        'request': blood_request
    })

@login_required
def bloodrequest_delete(request, pk):
    blood_request = get_object_or_404(BloodRequest, pk=pk)
    if request.method == 'POST':
        blood_request.delete()
        messages.success(request, 'Blood request deleted successfully!')
        return redirect('bloodrequest_list')
    
    return render(request, 'bloodrequests/request_confirm_delete.html', {'request': blood_request})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Doctor
from .forms import DoctorForm

def doctor_list(request):
    doctors = Doctor.objects.all().order_by('-joining_date')
    return render(request, 'doctors/doctor_list.html', {'doctors': doctors})

def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    return render(request, 'doctors/doctor_detail.html', {'doctor': doctor})

def doctor_create(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES)
        if form.is_valid():
            doctor = form.save()
            messages.success(request, 'Doctor created successfully!')
            return redirect('doctor_detail', pk=doctor.pk)
    else:
        form = DoctorForm()
    
    return render(request, 'doctors/doctor_form.html', {
        'form': form,
        'title': 'Add New Doctor'
    })

def doctor_update(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor updated successfully!')
            return redirect('doctor_detail', pk=doctor.pk)
    else:
        form = DoctorForm(instance=doctor)
    
    return render(request, 'doctors/doctor_form.html', {
        'form': form,
        'title': 'Edit Doctor',
        'doctor': doctor
    })

def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        doctor.delete()
        messages.success(request, 'Doctor deleted successfully!')
        return redirect('doctor_list')
    
    return render(request, 'doctors/doctor_confirm_delete.html', {'doctor': doctor})


from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

def help_support(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Send email to support team
        send_mail(
            f"Support Request: {subject}",
            f"From: {name} <{email}>\n\n{message}",
            settings.DEFAULT_FROM_EMAIL,
            [settings.SUPPORT_EMAIL],
            fail_silently=False,
        )
        
        messages.success(request, 'Your support request has been submitted. We will contact you soon!')
        return redirect('help_support')
    
    return render(request, 'help_support.html')

#Reports 
from django.shortcuts import render
from django.db.models.functions import TruncMonth
from django.db.models import Count, Sum
from django.utils import timezone
from .models import Donation
import json

def donation_trends_report(request):
    # Get last 12 months of data
    end_date = timezone.now().date()
    start_date = end_date - timezone.timedelta(days=365)
    
    # Query: Count donations per month
    monthly_data = Donation.objects.filter(
        donation_date__gte=start_date,
        donation_date__lte=end_date
    ).annotate(
        month=TruncMonth('donation_date')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')
    
    # Prepare data for JavaScript
    months = [entry['month'].strftime("%b %Y") for entry in monthly_data]
    counts = [entry['count'] for entry in monthly_data]
    
    # Calculate totals in Python instead of template
    total_donations = sum(counts)
    avg_donations = round(total_donations / 12, 1) if len(counts) > 0 else 0
    
    context = {
        'months': json.dumps(months),
        'counts': json.dumps(counts),
        'start_date': start_date,
        'end_date': end_date,
        'total_donations': total_donations,
        'avg_donations': avg_donations
    }
    return render(request, 'reports/donation_trends.html', context)