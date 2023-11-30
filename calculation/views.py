from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *


@api_view(["GET"])
def search_indicators(request):
    def get_draft_estimate_id():
        vacancy = Estimate.objects.filter(status=1).first()

        if vacancy is None:
            return None

        return vacancy.pk

    query = request.GET.get("query", "")

    indicators = Indicator.objects.filter(status=1).filter(name__icontains=query)

    serializer = IndicatorSerializer(indicators, many=True)

    resp = {
        "indicators": serializer.data,
        "draft_estimate": get_draft_estimate_id()
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
    indicator.status = 2
    indicator.save()

    indicators = Indicator.objects.filter(status=1)
    serializer = IndicatorSerializer(indicators, many=True)

    return Response(serializer.data)


@api_view(["POST"])
def add_indicator_to_estimate(request, indicator_id):
    if not Indicator.objects.filter(pk=indicator_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    indicator = Indicator.objects.get(pk=indicator_id)

    estimate = Estimate.objects.filter(status=1).last()

    if estimate is None:
        estimate = Estimate.objects.create()

    estimate.indicators.add(indicator)
    estimate.save()

    serializer = IndicatorSerializer(estimate.indicators, many=True)

    return Response(serializer.data)


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
def get_estimates(request):
    estimates = Estimate.objects.all()
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
    if not Estimate.objects.filter(pk=estimate_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not Indicator.objects.filter(pk=indicator_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    estimate = Estimate.objects.get(pk=estimate_id)
    estimate.indicators.remove(Indicator.objects.get(pk=indicator_id))
    estimate.save()

    serializer = IndicatorSerializer(estimate.indicators, many=True)

    return Response(serializer.data)

