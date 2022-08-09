from django.contrib import admin
from django.template.response import TemplateResponse
from .models import Hostel, User, Complain

# Register your models here.

# Admin Action Functions
def change_attendance_status(modeladmin, request, queryset):
    queryset.update(is_attended = 'YES')


# Action description
change_attendance_status.short_description = "Mark Selected Complains as YES"


class ComplainAdmin(admin.ModelAdmin):
    list_display = ('user','category', 'subject','date_reported', 'desc', 'is_attended')
    list_filter = ('category','date_reported', 'is_attended')
    search_fields = ['category', 'date_reported', 'desc']
    list_editable = ['is_attended']
    actions = [change_attendance_status]

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email','is_admin', 'is_supervisor', 'is_student', 'hostel')
    list_filter = ('is_admin', 'is_supervisor', 'is_student', 'hostel')
    search_fields = ['username', 'first_name', 'last_name','is_admin', 'is_supervisor', 'is_student']
    list_editable = ['is_admin', 'is_supervisor', 'is_student']

class HostelAdmin(admin.ModelAdmin):
    list_display = ('name','gender','block','room_no')
    list_filter = ('gender','name','block')
    search_fields = ('gender','name','block','room_no')

admin.site.site_header = "Hostel Room Complaint Administration"
admin.site.register(Complain, ComplainAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Hostel, HostelAdmin)