from django.db import connection
from django.shortcuts import render, redirect

from .models import *


def get_draft_estimate():
    return Estimate.objects.filter(status=1).first()


def index(request):
    query = request.GET.get("query", "")
    indicators = Indicator.objects.filter(name__icontains=query).filter(status=1)
    draft_estimate = get_draft_estimate()

    context = {
        "query": query,
        "indicators": indicators,
        "draft_estimate_id": draft_estimate.pk if draft_estimate else None
    }

    return render(request, "home_page.html", context)


def indicator_details(request, indicator_id):
    context = {
        "indicator": Indicator.objects.get(id=indicator_id)
    }

    return render(request, "indicator_page.html", context)


def indicator_delete(request, indicator_id):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE app_indicator SET status = 2 WHERE id = %s", [indicator_id])

    return redirect("/")


def get_indicators(estimate):
    items = IndicatorEstimate.objects.filter(estimate=estimate)
    return [item.indicator for item in items]


def estimate_details(request, estimate_id):
    estimate = Estimate.objects.get(id=estimate_id)
    context = {
        "estimate": estimate,
        "indicators": get_indicators(estimate)
    }

    return render(request, "estimate_page.html", context)
