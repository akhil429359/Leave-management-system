from django.contrib import admin
from .models import LeaveRequest,Leavetype
# Register your models here.

admin.site.register(LeaveRequest)
admin.site.register(Leavetype)
