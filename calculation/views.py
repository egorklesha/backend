from datetime import datetime

from django.contrib.auth import authenticate
from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .jwt_helper import *
from .permissions import *
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
@permission_classes([IsModerator])
def update_indicator(request, indicator_id):
    if not Indicator.objects.filter(pk=indicator_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    indicator = Indicator.objects.get(pk=indicator_id)
    serializer = IndicatorSerializer(indicator, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsModerator])
def create_indicator(request):
    Indicator.objects.create()

    indicators = Indicator.objects.filter(status=1)
    serializer = IndicatorSerializer(indicators, many=True)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsModerator])
def update_indicator_image(request, indicator_id):
    if not Indicator.objects.filter(pk=indicator_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    indicator = Indicator.objects.get(pk=indicator_id)
    serializer = IndicatorSerializer(indicator, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_estimates(request):
    token = get_access_token(request)
    payload = get_jwt_payload(token)
    user = CustomUser.objects.get(pk=payload["user_id"])

    status_id = int(request.GET.get("status", -1))
    date_start = int(request.GET.get("date_start", -1))
    date_end = int(request.GET.get("date_end", -1))

    estimates = Estimate.objects.exclude(status__in=[1, 5]) if user.is_moderator else Estimate.objects.filter(owner_id=user.pk)

    if status_id != -1:
        estimates = estimates.filter(status=status_id)

    if date_start != -1:
        estimates = estimates.filter(date_of_formation__gt=datetime.fromtimestamp(date_start).date())

    if date_end != -1:
        estimates = estimates.filter(date_of_formation__lt=datetime.fromtimestamp(date_end).date())
        
    serializer = EstimateSerializer(estimates, many=True)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_estimate_by_id(request, estimate_id):
    if not Estimate.objects.filter(pk=estimate_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    estimate = Estimate.objects.get(pk=estimate_id)
    serializer = EstimateSerializer(estimate, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def update_status_user(request, estimate_id):
    if not Estimate.objects.filter(pk=estimate_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    estimate = Estimate.objects.get(pk=estimate_id)

    if estimate.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    estimate.status = 2
    estimate.date_of_formation = timezone.now()
    estimate.save()

    serializer = EstimateSerializer(estimate, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsModerator])
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
    estimate.date_complete = timezone.now()
    estimate.save()

    serializer = EstimateSerializer(estimate, many=False)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def delete_indicator_from_estimate(request, estimate_id, indicator_id):
    if not IndicatorEstimate.objects.filter(indicator_id=indicator_id, estimate_id=estimate_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = IndicatorEstimate.objects.get(indicator_id=indicator_id, estimate_id=estimate_id)
    item.delete()

    estimate = Estimate.objects.get(pk=estimate_id)

    serializer = EstimateSerializer(estimate, many=False)

    return Response(serializer.data["indicators"])


@api_view(["PUT"])
@permission_classes([IsRemoteService])
def update_estimate_indicator(request, estimate_id, indicator_id):
    if not IndicatorEstimate.objects.filter(indicator_id=indicator_id, estimate_id=estimate_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = IndicatorEstimate.objects.get(indicator_id=indicator_id, estimate_id=estimate_id)

    serializer = IndicatorEstimateSerializer(item, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@swagger_auto_schema(method='post', request_body=UserLoginSerializer)
@api_view(["POST"])
def login(request):
    serializer = UserLoginSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    user = authenticate(**serializer.data)
    if user is None:
        message = {"message": "invalid credentials"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    access_token = create_access_token(user.id)

    user_data = {
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "is_moderator": user.is_moderator,
        "access_token": access_token
    }

    response = Response(user_data, status=status.HTTP_201_CREATED)

    response.set_cookie('access_token', access_token, httponly=False, expires=settings.JWT["ACCESS_TOKEN_LIFETIME"])

    return response


@api_view(["POST"])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    user = serializer.save()

    access_token = create_access_token(user.id)

    message = {
        'message': 'User registered successfully',
        'user_id': user.id,
        "access_token": access_token
    }

    response = Response(message, status=status.HTTP_201_CREATED)

    response.set_cookie('access_token', access_token, httponly=False, expires=settings.JWT["ACCESS_TOKEN_LIFETIME"])

    return response


@api_view(["POST"])
def check(request):
    token = get_access_token(request)

    if token is None:
        message = {"message": "Token is not found"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    if token in cache:
        message = {"message": "Token in blacklist"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    payload = get_jwt_payload(token)
    user_id = payload["user_id"]

    user = CustomUser.objects.get(pk=user_id)
    serializer = UserSerializer(user, many=False)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    access_token = get_access_token(request)

    if access_token not in cache:
        cache.set(access_token, settings.JWT["ACCESS_TOKEN_LIFETIME"])

    message = {"message": "Вы успешно вышли из аккаунта"}
    response = Response(message, status=status.HTTP_200_OK)

    response.delete_cookie('access_token')

    return response
