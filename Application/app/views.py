"""
Definition of views.
"""

from __future__ import barry_as_FLUFL
import os
from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.shortcuts import render,redirect
from numpy import full_like
from app.play import PlayForm
from app.forms import ImageForm
from app.models import PlayImage
from python_webapp_django.settings import MEDIA_ROOT, MEDIA_URL 

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def play_view(request, id:int = None):  
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        if id is None:
            pass
        else:
            imgs = PlayImage.objects.all()
            return render(request, 'play.html', {'images': imgs, 'media_root': MEDIA_ROOT, 'media_url': MEDIA_URL})

def signup_view(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'registration/signup.html', {'form': form})

def upload_image_view(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            # Get the current instance object to display in the template
            img_obj = form.instance
            return redirect('play', img_obj.id)
    else:
        form = ImageForm()
    return render(request, 'upload.html', {'form': form})