from django.contrib import admin
from .models import Prescription


class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'created', 'updated')


admin.site.register(Prescription, PrescriptionAdmin)
