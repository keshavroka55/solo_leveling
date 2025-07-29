from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Task)
admin.site.register(TaskCategory)
admin.site.register(TaskProgress)
admin.site.register(DailySummary)
admin.site.register(UserProfile)
admin.site.register(Notification)
