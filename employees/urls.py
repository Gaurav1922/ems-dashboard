from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),

    # Session check URL
    path('check-session/', views.check_session, name='check_session'),
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Employee URLS
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('employees/add/', views.employee_create, name='employee_create'),
    path('employees/<int:pk>/edit/', views.employee_update, name='employee_update'),
    path('employees/<int:pk>/delete/', views.employee_delete, name='employee_delete'),

    # Department URLS
    path('departments/', views.department_list, name='department_list'),
    path('departments/add/', views.department_create, name='department_create'),
    path('departments/<int:pk>/edit/', views.department_update, name='department_update'),

    # Messaging Urls
    path('messaging/', views.messaging_dashboard, name='messaging_dashboard'),
    path('messaging/send-email/', views.send_email, name='send_email'), 
    path('messaging/send-email/<int:employee_id>/', views.send_email, name='send_email_to'), 
    path('messaging/send-whatsapp/', views.send_whatsapp, name='send_whatsapp'),
    path('messaging/send-whatsapp/<int:employee_id>/', views.send_whatsapp, name='send_whatsapp_to'),
    path('messaging/history/<int:employee_id>/', views.message_history, name='message_history'),
]
