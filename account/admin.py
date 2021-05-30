from django.contrib import admin
from .models import Profile
from .models import DiseaseHistory


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'mobile', 'age', 'bp_problem', 'blood_group',
                    'major_health_problem', 'city', 'any_operation', 'created', 'updated')
    list_per_page = 20


admin.site.register(Profile, ProfileAdmin)


class DiseaseHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'disease',
                    'prescription', 'created', 'updated')


admin.site.register(DiseaseHistory, DiseaseHistoryAdmin)
