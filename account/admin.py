from django.contrib import admin
from .models import DiseaseHistory, Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'mobile', 'age', 'bp_problem', 'blood_group',
                    'major_health_problem', 'city', 'any_operation')


class DiseaseHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'description', 'remark')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(DiseaseHistory, DiseaseHistoryAdmin)
