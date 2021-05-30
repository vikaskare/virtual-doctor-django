from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'Virtual Doctor'
admin.site.site_title = "Virtual Doctor admin"
# admin.site.index_title = "Custom Bookstore Admin"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/', include('account.urls')),
    path('api/predict/', include('predict.urls')),
]
