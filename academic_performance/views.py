import json

from django.http import HttpResponse, Http404, HttpResponseBadRequest, HttpResponseServerError
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from functionalModule import func_perfomance as performance


def select(id):
    if id is None:
        pass
    obj = performance.select_student(id)
    return obj


def toJson(obj):
    return json.dumps(obj, ensure_ascii=False)


@csrf_protect
@csrf_exempt
def index(request):
    if request.method == "GET":
        studentid = request.GET.get('id')
        if studentid is None:
            return HttpResponse(performance.select_students())
        student = performance.select_student(studentid)
        if student is None:
            raise Http404(toJson({"status": "error", "description": "Студент не найден"}))
        return HttpResponse(student)

    elif request.method == "DELETE":
        studentid = request.GET.get('id')
        if studentid is None:
            return HttpResponseBadRequest(toJson({"status": "error", "description": f"Отсутствует параметр id"}))
        student = select(studentid)
        if student is None:
            raise Http404(toJson({"status": "error", "description": "Студент не найден"}))
        if performance.delete_student(studentid) is not None:
            return HttpResponse(toJson({"status": "successful", "object": student}))
        else:
            return HttpResponseServerError(toJson({"status": "error", "object": student,
                                                   "description": "Неизвестная ошибка с Базой данных"}))

    elif request.method == "POST":
        studentid = request.GET.get('id')
        if studentid is None:
            return HttpResponseBadRequest(toJson({"status": "error", "description": f"Отсутствует параметр id"}))
        student = select(studentid)
        if student is None:
            raise Http404(toJson({"status": "error", "description": "Студент не найден"}))
        lecture_visits = request.GET.get('lecture_visits')
        practice_visits = request.GET.get('practice_visits')
        practice = request.GET.get('practice')
        if performance.update_student(studentid, lecture_visits, practice_visits, practice) is not None:
            student = select(studentid)
            return HttpResponse(toJson({"status": "successful", "object": student}))
        else:
            return HttpResponseServerError(toJson({"status": "error", "object": student,
                                                   "description": "Неизвестная ошибка с Базой данных"}))

    elif request.method == "PUT":
        studentid = request.GET.get('id')
        if studentid is None:
            return HttpResponseBadRequest(toJson({"status": "error", "description": f"Отсутствует параметр id"}))
        student = select(studentid)
        if not (student is None):
            raise Http404(toJson({"status": "error", "object": student, "description": "Студент уже записан"}))
        if performance.insert_student(studentid) is not None:
            student = select(studentid)
            return HttpResponse(toJson({"status": "successful", "object": student}))
        else:
            return HttpResponseServerError(toJson({"status": "error", "object": student,
                                                   "description": "Неизвестная ошибка с Базой данных"}))

    else:
        return HttpResponse(performance.select_students())
