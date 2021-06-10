from django.urls import path
from salecars.views import start_polling

urlpatterns = [
    path('start', start_polling)
]