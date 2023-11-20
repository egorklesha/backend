from django.shortcuts import render, redirect

from .models import *


def index(request):
    query = request.GET.get("query")
    thematics = Indicator.objects.filter(name__icontains=query).filter(status=1) if query else Indicator.objects.filter(status=1)

    context = {
        "search_query": query if query else "",
        "indicators": thematics
    }

    return render(request, "home_page.html", context)


def indicator_details(request, indicator_id):
    context = {
        "indicator": Indicator.objects.get(id=indicator_id)
    }

    return render(request, "indicator_page.html", context)


# Которая по id находит показатель и вызывает его метод delete
# В методе delete отправляешь sql запрос на обновление статуса
def indicator_delete(request, indicator_id):
    indicator = Indicator.objects.get(id=indicator_id)
    indicator.delete()

    return redirect("/")
