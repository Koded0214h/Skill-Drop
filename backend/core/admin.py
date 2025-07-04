from django.contrib import admin
from .models import (
    CustomUser, StudentProfile, EmployerProfile,
    Gig, Application, Badge, Notification
)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'wallet_address')
    list_filter = ('role',)
    search_fields = ('username', 'email')


@admin.register(Gig)
class GigAdmin(admin.ModelAdmin):
    list_display = ('title', 'employer', 'deadline', 'created_at')
    search_fields = ('title', 'employer__username')
    list_filter = ('deadline',)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('gig', 'student', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('gig__title', 'student__username')
    actions = ['mark_accepted', 'mark_rejected']

    def mark_accepted(self, request, queryset):
        updated = queryset.update(status='accepted')
        self.message_user(request, f"{updated} applications marked as accepted.")
    mark_accepted.short_description = "Mark selected as accepted"

    def mark_rejected(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f"{updated} applications marked as rejected.")
    mark_rejected.short_description = "Mark selected as rejected"


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('recipient_address', 'tx_hash', 'block_number', 'created_at')


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'skills', 'github')


@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read',)
