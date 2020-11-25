from django.contrib import admin
from .models import ChatMessage,Thread,ThreadManager,Profile
# Register your models here.
admin.site.register(Profile)

class ChatMessage(admin.TabularInline):
    model = ChatMessage

class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage]
    class Meta:
        model = Thread 


admin.site.register(Thread, ThreadAdmin)
