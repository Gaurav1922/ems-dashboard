from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms.widgets import TextInput, PasswordInput
from .models import Employee, Department

"""class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class' : 'form-control'})
        
         # Add placeholders
        self.fields['username'].widget.attrs.update({'placeholder': 'Enter username'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Enter first name'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Enter last name'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter email address'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Enter password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm password'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user"""

class LoginForm(AuthenticationForm):
    """Custom login form with better styling"""
    username = forms.CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter username'
    }))
    password = forms.CharField(widget=PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter password'
    }))


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

class EmailMessageForm(forms.Form):
    recipient = forms.ChoiceField(choices=[])
    subject = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Enter subject'
    }))
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class' : 'form-control',
        'rows' : 6,
        'placeholder' : 'Enter your message..'
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recipient'].choices = [
            (emp.id, f"{emp.first_name} {emp.last_name} - {emp.department}")
            for emp in Employee.objects.filter(status='active')
        ]
        self.fields['recipient'].widget.attrs.update({'class': 'form-control'})

class WhatsAppMessageForm(forms.Form):
    recipient = forms.ChoiceField(choices=[])
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class' : 'form-control',
        'rows' : 4,
        'placeholder' : 'Enter your WhatsApp message..',
        'maxlength' : '1600'
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recipient'].choices = [
            (emp.id, f"{emp.first_name} {emp.last_name} - {emp.phone_number}")
            for emp in Employee.objects.filter(status='active', phone_number__isnull=False)
        ]
        self.fields['recipient'].widget.attrs.update({'class' : 'form-control'})