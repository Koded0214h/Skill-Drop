from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('employer', 'Employer'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    wallet_address = models.CharField(max_length=42, blank=True, null=True)
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self):
        return f"{self.username} ({self.role})"

class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_profile")
    bio = models.TextField(blank=True)
    skills = models.CharField(max_length=255, blank=True)
    github = models.URLField(blank=True)

    def __str__(self):
        return f"Student Profile for {self.user.username}"

class EmployerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="employer_profile")
    company_name = models.CharField(max_length=255)
    company_website = models.URLField(blank=True)

    def __str__(self):
        return f"Employer Profile for {self.user.username}"


class Badge(models.Model):
    recipient_address = models.CharField(max_length=42)
    tx_hash = models.CharField(max_length=66)
    block_number = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Badge to {self.recipient_address} in Tx {self.tx_hash[:10]}..."
    
class Gig(models.Model):
    employer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='gigs')
    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.employer.username}"



class Application(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    gig = models.ForeignKey(Gig, on_delete=models.CASCADE, related_name='applications')
    cv = models.FileField(upload_to='cvs/')
    motivation = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ], default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    feedback = models.TextField(blank=True, null=True)
    rating = models.PositiveIntegerField(null=True, blank=True)  # 1 to 5
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.username} applied for {self.gig.title}"
    
class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To {self.user.username}: {self.message[:30]}"
