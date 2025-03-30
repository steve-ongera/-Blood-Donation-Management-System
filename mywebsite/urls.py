from django.urls import path
from . import views

urlpatterns = [
    path('donors/', views.donor_list, name='donor_list'),
    path('<int:pk>/', views.donor_detail, name='donor-detail'),
    path('add/', views.donor_add, name='donor-add'),
    path('<int:pk>/update/', views.donor_update, name='donor-update'),
    path('<int:pk>/delete/', views.donor_delete, name='donor-delete'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('help_support/', views.help_support, name='help_support'),
    path('donation_trends_report/', views.donation_trends_report, name='donation_trends_report'),

    path('recipients/', views.recipient_list, name='recipient_list'),
    path('add_recipients/', views.add_recipient, name='add_recipient'),
    path('recipients/<int:pk>/', views.recipient_detail, name='recipient_detail'),
    path('recipients/<int:pk>/edit/', views.edit_recipient, name='edit_recipient'),
    path('recipients/<int:pk>/delete/', views.delete_recipient, name='delete_recipient'),

    path('donations/', views.donation_list, name='donation_list'),
    path('donations/add/', views.donation_create, name='donation_create'),
    path('donations/<int:pk>/', views.donation_detail, name='donation_detail'),
    path('donations/<int:pk>/edit/', views.donation_update, name='donation_update'),
    path('donations/<int:pk>/delete/', views.donation_delete, name='donation_delete'),

    path('bloodrequests/', views.bloodrequest_list, name='bloodrequest_list'),
    path('bloodrequests/add/', views.bloodrequest_create, name='bloodrequest_create'),
    path('bloodrequests/<int:pk>/', views.bloodrequest_detail, name='bloodrequest_detail'),
    path('bloodrequests/<int:pk>/edit/', views.bloodrequest_update, name='bloodrequest_update'),
    path('bloodrequests/<int:pk>/delete/', views.bloodrequest_delete, name='bloodrequest_delete'),

    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/add/', views.doctor_create, name='doctor_create'),
    path('doctors/<int:pk>/', views.doctor_detail, name='doctor_detail'),
    path('doctors/<int:pk>/edit/', views.doctor_update, name='doctor_update'),
    path('doctors/<int:pk>/delete/', views.doctor_delete, name='doctor_delete'),

]
