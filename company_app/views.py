from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from user_app.models import *
from main_app.models import *
from rest_framework.authtoken.models import Token
from rest_framework import routers, serializers, viewsets
# Create your views here.

