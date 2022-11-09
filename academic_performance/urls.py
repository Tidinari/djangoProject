from django.urls import path
from academic_performance.views import index

urlpatterns = [
    path('', index),
]