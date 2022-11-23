import json

from django.http import HttpResponse, Http404, HttpResponseBadRequest, HttpResponseServerError
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from functionalModule import func_students as students


def select(id):
    if id is None:
        pass
    obj = students.select_student(id)
    return obj


def toJson(obj):
    return json.dumps(obj, ensure_ascii=False)


@csrf_protect
@csrf_exempt
def index(request):
    if request.method == "GET":
        studentid = request.GET.get('id')
        fname = request.GET.get('first_name')
        sname = request.GET.get('second_name')
        lname = request.GET.get('last_name')
        group = request.GET.get('groupid')
        student = students.select_student(studentid, fname, sname, lname, group)
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
        if students.delete_student(studentid) is not None:
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
        fname = request.GET.get('first_name')
        sname = request.GET.get('second_name')
        lname = request.GET.get('last_name')
        group = request.GET.get('groupid')
        if students.update_student(studentid, fname, sname, lname, group) is not None:
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
        fname = request.GET.get('first_name')
        sname = request.GET.get('second_name')
        lname = request.GET.get('last_name')
        group = request.GET.get('groupid')
        if fname is None:
            return HttpResponseBadRequest(toJson({"status": "error", "description": "Отсутствует параметр first_name"}))
        if sname is None:
            return HttpResponseBadRequest(toJson({"status": "error", "description": "Отсутствует параметр second_name"}))
        if lname is None:
            return HttpResponseBadRequest(toJson({"status": "error", "description": "Отсутствует параметр last_name"}))
        if group is None:
            return HttpResponseBadRequest(toJson({"status": "error", "description": "Отсутствует параметр groupid"}))
        if students.insert_student(studentid, fname, sname, lname, group) is not None:
            student = select(studentid)
            return HttpResponse(toJson({"status": "successful", "object": student}))
        else:
            return HttpResponseServerError(toJson({"status": "error", "object": student,
                                                   "description": "Неизвестная ошибка с Базой данных"}))

    else:
        return HttpResponse(students.select_students())
