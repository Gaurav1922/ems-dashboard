from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Count, Avg
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Employee, Department
from .forms import EmployeeForm, DepartmentForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


# Create your views here.
"""def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username ="""
"""def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'employees/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')

@login_required
"""
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

def employee_detail(request, pk):
    """Employee Details"""
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employees/employee_detail.html', {'employee':employee})

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

def employee_delete(request, pk):
    """ Delete employee"""
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, 'Employee Deleted successfully!')
        return redirect('employee_list')
    return render(request, 'employees/employee_confirm_delete.html', {'employee': employee})

def department_list(request):
    """List all Department"""
    departments = Department.objects.annotate(
        employee_count = Count('employees')
    ).order_by('name')

    return render(request, 'employees/department_list.html', {'departments': departments})

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