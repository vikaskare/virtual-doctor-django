from django.contrib import admin
from django.urls import path, include
admin.site.site_header = 'Virtual Doctor'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/', include('account.urls')),
    path('api/predict/', include('predict.urls')),
]
