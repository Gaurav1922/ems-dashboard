from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from employees.models import User

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("department_details", kwargs={"pk": self.pk})
    
    class Meta:
        ordering = ['name']

class Employee(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('terminated', 'Terminated'),
    ]

    employee_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format:'+999999999'. upto 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField()
    department = models.ForeignKey(Department, on_delete= models.CASCADE, related_name='employees')
    position = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    hire_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_absolute_url(self):
        return reverse("employee_detail", kwargs={"pk": self.pk})
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ['first_name', 'last_name']


class Message(models.Model):
    MESSAGE_TYPES = [
        ('email', 'Email'),
        ('whatsapp', 'WhatsApp'),
    ]

    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient = models.ForeignKey("Employee", on_delete=models.CASCADE)  # ✅ string reference
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES)
    subject = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField()
    is_sent = models.BooleanField(default=False)
    error_message = models.TextField(blank=True, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.message_type} to {self.recipient} ({'Sent' if self.is_sent else 'Failed'})"
