from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Count, Avg
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from .models import Employee, Department, Message
from .forms import EmployeeForm, DepartmentForm, EmailMessageForm, WhatsAppMessageForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

import json
import requests


@never_cache
# Authentication Views
def user_login(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                next_page = request.GET.get('next', 'dashboard')
                return redirect(next_page)
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form' : form})


@never_cache
def user_register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})


@never_cache
def user_logout(request):
    """User Logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

# Create your views here.
@never_cache
@login_required
def dashboard(request):
    """Main dashboard view"""
    total_employees = Employee.objects.count()
    active_employees = Employee.objects.filter(status='active').count()
    total_departments = Department.objects.count()
    avg_salary = Employee.objects.aggregate(avg_salary=Avg('salary'))['avg_salary'] or 0

    # employee count department wise
    dept_stats = Department.objects.annotate(
        employee_count=Count('employees')
    ). order_by('-employee_count')[:5]

    # Recent employee
    recent_employees = Employee.objects.filter(status='active').order_by('-created_at')[:5]

    context = {
        'total_employees': total_employees,
        'active_employees': active_employees,
        'total_departments': total_departments,
        'avg_salary': round(avg_salary, 2),
        'dept_stats': dept_stats,
        'recent_employees': recent_employees,
        'user': request.user,
    }

    return render(request, 'employees/dashboard.html', context)

@never_cache
@login_required
def employee_list(request):
    """List all employees with search and filter"""
    employees = Employee.objects.select_related('department').all()

    # Search
    search_query = request.GET.get('search')
    if search_query:
        employees = employees.filter(first_name__icontains=search_query) | employees.filter(last_name__icontains=search_query) |employees.filter(employee_id__icontains=search_query) #|employees.filter(address__icontains=search_query)#

    # Filter department
    dept_filter = request.GET.get('department')
    if dept_filter:
        employees = employees.filter(department_id=dept_filter)

    # filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        employees = employees.filter(status=status_filter)
    
    # pagination
    paginator = Paginator(employees, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    departments = Department.objects.all()

    context = {
        'page_obj': page_obj,
        'departments': departments,
        'search_query': search_query,
        'dept_filter': dept_filter,
        'status_filter': status_filter,
    }
    return render(request, 'employees/employee_list.html', context)

@never_cache
@login_required
def employee_detail(request, pk):
    """Employee Details"""
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employees/employee_detail.html', {'employee':employee})

@never_cache
@login_required
def employee_create(request):
    """Create new employee"""
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee created successfully!')
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    
    return render(request, 'employees/employee_form.html', {
        'form': form,
        'title': 'ADD NEW EMPLOYEE'
    })

@never_cache
@login_required
def employee_update(request, pk):
    """ Upadate Employee"""
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee updated successfully')
            return redirect('employee_detail', pk=employee.pk)
    else:
        form = EmployeeForm(instance=employee)
    
    return render(request, 'employees/employee_form.html', {
        'form': form,
        'title': f'Update {employee.full_name}',
        'employee': employee
    })

@never_cache
@login_required
def employee_delete(request, pk):
    """ Delete employee"""
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, 'Employee Deleted successfully!')
        return redirect('employee_list')
    return render(request, 'employees/employee_confirm_delete.html', {'employee': employee})

@never_cache
@login_required
def department_list(request):
    """List all Department"""
    departments = Department.objects.annotate(
        employee_count = Count('employees')
    ).order_by('name')

    return render(request, 'employees/department_list.html', {'departments': departments})

@never_cache
@login_required
def department_create(request):
    """Create new department"""
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department created successfully!')
            return redirect('department_list')
    else:
        form = DepartmentForm()

    return render(request, 'employees/department_form.html', {
        'form': form,
        'title': 'Add New Department'
    })

@never_cache
@login_required
def department_update(request,pk):
    """update Department"""
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department updated successfully')
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    return render(request,'employees/department_form.html', {
        'form': form,
        'title': f'Update{department.name}',
        'department': department
    })

@never_cache
@login_required
def messaging_dashboard(request):
    employees = Employee.objects.filter(status='active')
    # last 5 messages, newest first
    recent_messages = Message.objects.filter(sender=request.user).order_by('-sent_at')[:5]

    context = {
        'employees': employees,
        'recent_messages': recent_messages,
    }
    return render(request, 'messaging/messaging_dashboard.html', context)

try:
    from twilio.rest import Client
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False

@never_cache
@login_required
def send_email(request, employee_id=None):
    """Send email to employee with improved error handling"""
    try:
        employee = None
        if employee_id:
            employee = get_object_or_404(Employee, id=employee_id)
        
        if request.method == 'POST':
            form = EmailMessageForm(request.POST)
            if form.is_valid():
                recipient_id = form.cleaned_data['recipient']
                subject = form.cleaned_data['subject']
                content = form.cleaned_data['content']

                try:
                    recipient = Employee.objects.get(id=recipient_id)
                except Employee.DoesNotExist:
                    messages.error(request, 'Selected employee not found.')
                    return redirect('messaging_dashboard')

                # Create message record
                try:
                    msg_record = Message.objects.create(
                        sender=request.user,
                        recipient=recipient,
                        message_type='email',
                        subject=subject,
                        content=content,
                        is_sent = False
                    )
                except Exception as e:
                    messages.error(request, f'Error creating message record: {str(e)}')
                    return redirect('messaging_dashboard')

                # Try to send email
                try:
                    result = send_mail(
                        subject=subject,
                        message=content,
                        from_email=getattr(settings, 'EMAIL_HOST_USER', 'noreply@example.com'),
                        recipient_list=[recipient.email],
                        fail_silently=False,
                    )

                    if result == 1:
                        msg_record.is_sent = True
                        messages.success(request, f'Email sent successfully to {recipient.full_name}!')
                    else:
                        msg_record.error_message = "SMTP server did not accept the email."
                        messages.error(request, f"Failed to send email to {recipient.full_name}.")
                    msg_record.save()

                except Exception as e:
                    msg_record.error_message = str(e)
                    msg_record.save()
                    messages.error(request, f'Failed to send email: {str(e)}')
                
                return redirect('messaging_dashboard')
            else:
                messages.error(request, 'Please correct the form errors.')
        else:
            initial_data = {}
            if employee:
                initial_data = {'recipient': employee.id}
            form = EmailMessageForm(initial=initial_data)

        context = {
            'form': form,
            'selected_employee': employee
        }
        return render(request, 'messaging/send_email.html', context)
        
    except Exception as e:
        messages.error(request, f'An unexpected error occurred: {str(e)}')
        return redirect('messaging_dashboard')


@never_cache
@login_required
def send_whatsapp(request, employee_id=None):
    """Send Whatsapp message to employee"""
    employee = None
    if employee_id:
        employee = get_object_or_404(Employee, id=employee_id)

    if request.method == 'POST':
        form = WhatsAppMessageForm(request.POST)
        if form.is_valid():
            recipient_id = form.cleaned_data['recipient']
            content = form.cleaned_data['content']

            recipient = get_object_or_404(Employee, id=recipient_id)

            if not recipient.phone_number:
                messages.error(request, f'{recipient.full_name} does not have a WhatsApp number configured.')
                return redirect('messaging_dashboard')
            
            # Create message Record
            msg_record = Message.objects.create(
                sender=request.user,
                recipient=recipient,
                message_type='whatsapp',
                content=content
            )

            try:
                # Send WhatsApp message using Twilio.
                success = send_whatsapp_message(recipient.phone_number, content)

                if success:
                    msg_record.is_sent = True
                    msg_record.save()
                    messages.success(request, f'WhatsApp message sent successfully to {recipient.full_name}!')
                else:
                    raise Exception("Failed to send WhatsApp message")
                
            except Exception as e:
                msg_record.error_message = str(e)
                msg_record.save()
                messages.error(request, f'Failed to send WhatsApp message: {str(e)}')
            
            return redirect('messaging_dashboard')
    else:
        initial_data = {'recipient': employee.id} if employee else {}
        form = WhatsAppMessageForm(initial_data)

    employees = Employee.objects.filter(status='active', phone_number__isnull=False)
    return render(request, 'messaging/send_whatsapp.html', {
        'form' : form,
        'employees' : employees,
        'selected_employee' : employee
    })

def send_whatsapp_message(phone_number, message_content):
    """Helper function to send whatsapp message via twilio"""
    if not TWILIO_AVAILABLE:
        print("Twilio library not installed. Install with: pip install twilio")
        return False


    try:
        # Get Twilio credentials from settings
        account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
        auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
        twilio_whatsapp_number = getattr(settings, 'TWILIO_WHATSAPP_NUMBER', None)

        if not all([account_sid, auth_token, twilio_whatsapp_number]):
            print("Twilio credentials not configured in settings")
            return False

        client = Client(account_sid, auth_token)

        # Format phone number - ensure it starts with +
        if not phone_number.startswith('+'):
            phone_number = '+' + phone_number

        message = client.messages.create(
            body=message_content,
            from_=f'whatsapp:{twilio_whatsapp_number}',
            to=f'whatsapp:{phone_number}'
        )

        print(f"WhatsApp message sent successfully. SID: {message.sid}")
        return True
        
    except Exception as e:
        print(f"WhatsApp send error: {e}")
        return False

@never_cache
@login_required
def message_history(request, employee_id):
    """View message history for specific employee"""

    employee = get_object_or_404(Employee, id=employee_id)
    messages_sent = Message.objects.filter(
        sender=request.user,
        recipient=employee
    ).order_by('-sent_at')  # newest first

    context = {
        'employee': employee,
        'message_list': messages_sent,
    }
    return render(request, 'messaging/message_history.html', context)

@never_cache
@login_required
def send_mail_view(request):
    """Alternative send email view"""
    return send_email(request)


@never_cache
def check_session(request):
    """Check if user session is still valid"""
    return JsonResponse({
        'authenticated': request.user.is_authenticated
    })