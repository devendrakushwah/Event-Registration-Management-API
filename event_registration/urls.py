from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('authentication.urls')),
    path('api/',include('event.urls')),
]

# documentation = https://documenter.getpostman.com/view/10090782/SWLk4R1H
#TODO path('api/docs/', get_swagger_view(title='Event registration API')),