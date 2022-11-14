from django.http import HttpResponse

import functionalModule


def index(request):
    return HttpResponse('Hello world!')


def students(request):
    return HttpResponse(functionalModule.func.select_students())
