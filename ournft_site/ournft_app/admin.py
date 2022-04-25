from django.contrib import admin
from .models import Comment, Image, History, Notification, Report
# Register your models here.
admin.site.register(Image)
admin.site.register(History)
admin.site.register(Notification)
admin.site.register(Comment)
admin.site.register(Report)

