from .UserSerializer import ListAllUsersSerializer
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from .UserSerializer import UserSerializer
from .UserSerializer import UpdateUserSerializer
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authentication import authenticate
from rest_framework.authentication import get_user_model
from .models import UserProfile
from rest_framework.generics import UpdateAPIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from .models import UserProfile
from rest_framework.decorators import api_view

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth.models import User,Group


from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.permissions import IsAuthenticated
import json


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def home(request):
    try:
        print("got yy", request.data['username'])
        # data = json.loads(request.body)
        username = request.data['username']
        password = request.data['password']

        if username == "" or password == "":
            return Response({"status": "failure"})
        if username is not None or password is not None:
            try:
                User = get_user_model()
                user = authenticate(username=User.objects.get(email=username), password=password)
            except:
                user = authenticate(username=username, password=password)
            print("yooooo",user)
            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                userProfile = UserProfile.objects.get(user=user)
                response = Response({"status": "success", "user": username, "token": token.key ,"firstname": user.first_name,"lastname": user.last_name,"email": user.email,"privilege":userProfile.priviledge})
                response.set_cookie(key="token", value=token, max_age=900)
                return response
            else:
                return Response({"status": "failure"})
        else:
            return Response({"status": "Enter User name and password"})
    except json.decoder.JSONDecodeError as e:
        return Response({"status": "failed", "exception": str(e)})
    except Exception as e:
        return Response({"status": "failed", "exception": str(e)})


# def create_group(getuser):


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def create(request):
    try:
        data = request.data
        if authenticate(username=data['username'], password=data['password']) is None:
            print(data)
            try:
                print(data['username'], data['email'], True)
                User = get_user_model()
                user = User.objects.create_user(username=data['username'], email=data['email'], is_staff=True)
                print("where is pwd", data['password'])
                user.set_password(data['password'])
                user.first_name = data['first_name']
                user.last_name = data['last_name']
                user.save()
                token, _ = Token.objects.get_or_create(user=user)
                profile = UserProfile()
                profile.user = user
                profile.mobile_number = data['mobile_number']
                profile.email =data['email']
                profile.company = data['company']
                profile.priviledge = "admin"
                profile.profile_pic = data["profile_pic"]
                mygroup, created = Group.objects.get_or_create(name=data['company'])
                mygroup.save()
                myuser = User.objects.get(username=data['username'])
                myuser.groups.add(mygroup)
                profile.save()
            except Exception as e:
                print("Exception is ", e)
                return Response({"status": "User Already "})

            return Response({"status": "success"}, status=HTTP_200_OK)
        else:
            return Response({"status": "User Already exists"})

    except Exception as e:
        print("Exception is ", e)
        return Response({"status": "failed", "Exception": str(e)})




@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([])
def add_subuser(request):
    try:
        print(request.user)
        data = request.data
        if authenticate(username=data['username'], password=data['password']) is None:
            print(data)
            try:
                print(data['username'], data['email'], True)
                User = get_user_model()
                user = User.objects.create_user(username=data['username'], email=data['email'], is_staff=True)
                print("where is pwd", data['password'])
                user.set_password(data['password'])
                user.first_name = data['first_name']
                user.last_name = data['last_name']
                user.save()
                token, _ = Token.objects.get_or_create(user=user)
                profile = UserProfile()
                profile.user = user
                profile.mobile_number = data['mobile_number']
                profile.email =data['email']
                userProfile = UserProfile.objects.get(user=request.user)
                profile.company = userProfile.company
                profile.priviledge = "user"
                profile.profile_pic = data["profile_pic"]
                myuser = User.objects.get(username=data['username'])
                mygroup = Group.objects.get(name=userProfile.company)
                myuser.groups.add(mygroup)
                profile.save()
            except Exception as e:
                print("Exception is ", e)
                return Response({"status": "User Already "})

            return Response({"status": "success"}, status=HTTP_200_OK)
        else:
            return Response({"status": "User Already exists"})

    except Exception as e:
        print("Exception is ", e)
        return Response({"status": "failed", "Exception": str(e)})



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([])
def update_profile(request):
    pass
