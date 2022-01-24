"""
Definition of views.
"""

from __future__ import barry_as_FLUFL
from distutils.sysconfig import get_makefile_filename
from errno import EEXIST
import os
from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.shortcuts import render,redirect
from app.forms import ImageForm
from app.models import Game, GameTile, PlayImage, Tile
from python_webapp_django.settings import MEDIA_ROOT, MEDIA_URL
from app.slicer import check_swap, mix_array, validate_game 

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
    success = False
    if request.method == 'POST':
        game_id = request.POST.get('validate')
        if game_id:
            game = Game.objects.get(id = game_id)
            success = validate_game(game)
            if success:
                return render(request, 'play.html', { 'images' : game.play_image, 'success' : success})
        
        game_tile_id = request.POST.get('gt_id')
        game_tile = GameTile.objects.get(id = game_tile_id)
        game_info = check_swap(game_tile)        
        return render(request, 'play.html', { 'images' : game_info.game_tiles, 'parent' : game_info.game, 'success' : success, 'media_root': MEDIA_ROOT, 'media_url': MEDIA_URL})

    elif request.method == 'GET':
        if id is None:
            all_imgs = PlayImage.objects.all()
            imgs = all_imgs[len(all_imgs)-1]
        else:
            imgs = PlayImage.objects.get(id = id)
        
        game_info = mix_array(request, imgs)
        return render(request, 'play.html', { 'images' : game_info.game_tiles, 'parent' : game_info.game, 'success' : False, 'media_root': MEDIA_ROOT, 'media_url': MEDIA_URL})


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