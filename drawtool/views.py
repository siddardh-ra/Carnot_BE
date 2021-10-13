from django.shortcuts import render
from rest_framework.authtoken.models import Token
from Users.models import UserProfile
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from .models import AOI
from .models import Measure

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth.models import User,Group

from rest_framework.authtoken.models import Token

from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.permissions import IsAuthenticated
import json
# Create your views here.

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([])
def save_aoi(request,proj_name,date):
    try:
        data = request.data
        project_data = AOI()
        project_data.project = proj_name+"_"+date
        project_data.label = data.get('label')
        project_data.description = data.get('description')
        project_data.polygon = data.get('polygon')
        project_data.save()
        return Response({"status":"success"})
    except Exception as e:
        return Response({"status": "failed", "Exception": str(e)})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([])
def save_measure(request,proj_name,date):
    try:
        data = request.data
        project_data = Measure()
        project_data.project = proj_name+"_"+date
        project_data.label = data.get('label')
        project_data.type = data.get('type')
        project_data.description = data.get('description')
        project_data.measurements = data.get('measurements')
        project_data.polygon = data.get('polygon')
        project_data.save()
        return Response({"status":"success"})
    except Exception as e:
        return Response({"status": "failed", "Exception": str(e)})