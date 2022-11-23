from django.urls import path
from academic_performance.views import *

urlpatterns = [
    path('', index),
]
