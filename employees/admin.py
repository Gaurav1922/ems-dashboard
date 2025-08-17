from django.contrib import admin
from .models import Employee, Department
# Register your models here.

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    ordering = ['name']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        'employee_id', 'first_name', 'last_name', 'department', 'position', 'status', 'hire_date'
    ]
    list_filter = ['department', 'status', 'gender', 'hire_date']
    search_fields = ['first_name', 'last_name', 'employee_id', 'email', 'address']
    ordering = ['first_name', 'last_name']
    date_hierarchy = 'hire_date'

    fieldsets = (
        ('Personal Information', {
            'fields' : ('employee_id', 'first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'gender', 'address')
        }),
        ('Employment Details',{
            'fields': ('department', 'position', 'salary', 'hire_date', 'status')
        }),
    )
