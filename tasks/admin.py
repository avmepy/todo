from django.contrib import admin
from tasks.models import Todo, Subtask

# Register your models here.

admin.site.register(Todo)
admin.site.register(Subtask)
