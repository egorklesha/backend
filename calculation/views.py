from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *


def get_draft_estimate():
    estimate = Estimate.objects.filter(status=1).first()

    if estimate is None:
        return None

    return estimate


@api_view(["GET"])
def search_indicators(request):
    query = request.GET.get("query", "")

    indicators = Indicator.objects.filter(status=1).filter(name__icontains=query)

    serializer = IndicatorSerializer(indicators, many=True)

    draft_estimate = get_draft_estimate()

    resp = {
        "indicators": serializer.data,
        "draft_estimate": draft_estimate.pk if draft_estimate else None
    }

    return Response(resp)


@api_view(["GET"])
def get_indicator_by_id(request, indicator_id):
    if not Indicator.objects.filter(pk=indicator_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    indicator = Indicator.objects.get(pk=indicator_id)
    serializer = IndicatorSerializer(indicator, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_indicator(request, indicator_id):
    if not Indicator.objects.filter(pk=indicator_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    indicator = Indicator.objects.get(pk=indicator_id)
    serializer = IndicatorSerializer(indicator, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
def create_indicator(request):
    Indicator.objects.create()

    indicators = Indicator.objects.filter(status=1)
    serializer = IndicatorSerializer(indicators, many=True)

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_indicator(request, indicator_id):
    if not Indicator.objects.filter(pk=indicator_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    indicator = Indicator.objects.get(pk=indicator_id)
    indicator.status = 5
    indicator.save()

    indicators = Indicator.objects.filter(status=1)
    serializer = IndicatorSerializer(indicators, many=True)

    return Response(serializer.data)


@api_view(["POST"])
def add_indicator_to_estimate(request, indicator_id):
    if not Indicator.objects.filter(pk=indicator_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    indicator = Indicator.objects.get(pk=indicator_id)

    draft_estimate = get_draft_estimate()

    if draft_estimate is None:
        draft_estimate = Estimate.objects.create()

    if IndicatorEstimate.objects.filter(estimate=draft_estimate, indicator=indicator).exists():
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    cons = IndicatorEstimate.objects.create()
    cons.estimate = draft_estimate
    cons.indicator = indicator
    cons.save()

    serializer = EstimateSerializer(draft_estimate, many=False)

    return Response(serializer.data["indicators"])


@api_view(["GET"])
def get_indicator_image(request, indicator_id):
    if not Indicator.objects.filter(pk=indicator_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    indicator = Indicator.objects.get(pk=indicator_id)

    return HttpResponse(indicator.image, content_type="image/png")


@api_view(["PUT"])
def update_indicator_image(request, indicator_id):
    if not Indicator.objects.filter(pk=indicator_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    indicator = Indicator.objects.get(pk=indicator_id)
    serializer = IndicatorSerializer(indicator, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["GET"])
def search_estimates(request):
    status_id = int(request.GET.get("status", -1))
    date_start = request.GET.get("date_start", None)
    date_end = request.GET.get("date_end", None)

    estimates = Estimate.objects.all()

    if status_id != -1:
        estimates = estimates.filter(status=status_id)

    if date_start:
        # date_start = datetime.date()
        estimates = estimates.filter(date_of_formation__gt=date_start)

    if date_end:
        # date_end = datetime.fromtimestamp(date_end).date()
        estimates = estimates.filter(date_of_formation__lt=date_end)
        
    serializer = EstimateSerializer(estimates, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_estimate_by_id(request, estimate_id):
    if not Estimate.objects.filter(pk=estimate_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    estimate = Estimate.objects.get(pk=estimate_id)
    serializer = EstimateSerializer(estimate, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_estimate(request, estimate_id):
    if not Estimate.objects.filter(pk=estimate_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    estimate = Estimate.objects.get(pk=estimate_id)
    serializer = EstimateSerializer(estimate, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    estimate.status = 1
    estimate.save()

    return Response(serializer.data)


@api_view(["PUT"])
def update_status_user(request, estimate_id):
    if not Estimate.objects.filter(pk=estimate_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    estimate = Estimate.objects.get(pk=estimate_id)

    if estimate.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    estimate.status = 2
    estimate.date_of_formation = datetime.now(tz=timezone.utc)
    estimate.save()

    serializer = EstimateSerializer(estimate, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_status_admin(request, estimate_id):
    if not Estimate.objects.filter(pk=estimate_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = request.data["status"]

    if request_status not in [3, 4]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    estimate = Estimate.objects.get(pk=estimate_id)

    if estimate.status != 2:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    estimate.date_complete = datetime.now(tz=timezone.utc)
    estimate.status = request_status
    estimate.save()

    serializer = EstimateSerializer(estimate, many=False)

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_estimate(request, estimate_id):
    if not Estimate.objects.filter(pk=estimate_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    estimate = Estimate.objects.get(pk=estimate_id)

    if estimate.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    estimate.status = 5
    estimate.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["DELETE"])
def delete_indicator_from_estimate(request, estimate_id, indicator_id):
    if not IndicatorEstimate.objects.filter(indicator_id=indicator_id, estimate_id=estimate_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = IndicatorEstimate.objects.get(indicator_id=indicator_id, estimate_id=estimate_id)
    item.delete()

    estimate = Estimate.objects.get(pk=estimate_id)

    serializer = EstimateSerializer(estimate, many=False)

    return Response(serializer.data["indicators"])


@api_view(["DELETE"])
def update_estimate_indicator(request,  estimate_id, indicator_id):
    if not IndicatorEstimate.objects.filter(indicator_id=indicator_id, estimate_id=estimate_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = IndicatorEstimate.objects.get(indicator_id=indicator_id, estimate_id=estimate_id)

    serializer = IndicatorEstimateSerializer(item, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)