from datetime import datetime
from os import stat
from django.shortcuts import render

# Create your views here.
from .models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.hashers import make_password,get_hasher
from rest_framework import serializers

class LoaderTask(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

@api_view(['post'])
def Register(r):
    user = r.POST['username']
    password = r.POST['password']
    client = Client.objects.create(username=user,date=datetime.today())
    client.set_password(password)
    client.save()
    key = Token.objects.create(user=client)
    return Response({"username":user,"password":client.password,"key":str(key)})

@api_view(["get",'post'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Task_View(r):
    user = r.user
    if r.method == 'GET':
        return Response(LoaderTask(Task.objects.filter(user=user),many=True).data)
    elif r.method == 'POST':
        title = r.POST['title']
        date = r.POST['date']
        task = Task.objects.create(user=user,title=title,date=date)
        return Response(LoaderTask(task).data)

@api_view(["get",'post'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def One_Task_View(r,pk):
    user = r.user
    if r.method == 'GET':
        try:
            return Response(LoaderTask(Task.objects.get(user=user,id=pk)).data)
        except:
            return Response(status=404)
    elif r.method == 'POST':
        try:
            data = Task.objects.get(user=user,id=pk)
            if data.is_check == False:
                data.is_check=True
            else:
                data.is_check=False
            data.save()
            return Response(LoaderTask(data).data)
        except:
            return Response(status=404)

@api_view(["get"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Filter_Task_View(r):
    user = r.user
    typee = r.GET['type']
    if typee.casefold() == 'false':
        return Response(LoaderTask(Task.objects.filter(user=user,is_check=False),many=True).data)
    elif typee.casefold() == 'true':
        return Response(LoaderTask(Task.objects.filter(user=user,is_check=True),many=True).data)
    else:
        return Response(status=400)

@api_view(["post"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Update_Task_View(r,pk):
    user = r.user
    title = None
    date = None
    task = Task.objects.filter(user=user,id=pk)
    if len(task) > 0:    
        task = task[0]
        if 'title' in r.POST:
            title = r.POST['title']
        if 'date' in r.POST:
            date =  r.POST['date']
        if title != None:
            task.title = title
        if date != None:
            task.date = date
        task.save()
        if date == None and title == None:
            return Response(status=400)
        else:
            return Response(LoaderTask(task).data)
    else:
        return Response(status=404)

@api_view(['post'])
def Login(r):
    user = r.POST['username']
    password = r.POST['password']
    client = Client.objects.filter(username=user)
    if len(client) > 0:
        client = client[0]
        if client.check_password(password):    
            key = Token.objects.get(user=client)
            return Response({"ok":True,"username":user,"password":client.password,"key":str(key)})
        else:
            return Response({"ok":False})     
    else:
        return Response({"ok":False})
