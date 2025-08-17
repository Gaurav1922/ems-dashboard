from django import forms
from .models import Employee, Department


"""class createUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())"""

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hire_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }