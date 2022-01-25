"""
Definition of views.
"""

from __future__ import barry_as_FLUFL
from distutils.sysconfig import get_makefile_filename
from django.shortcuts import render
from django.http import HttpRequest
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.shortcuts import render,redirect
from app.forms import ImageForm
from app.models import PlayImage
from app.play import do_one_move, validate
from app.preparer import start_game
from app.cache_info import clear_cache, get_cached_game, get_cached_tiles
from app.common import get_2d_array
 
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
    message = ''
    if request.method == 'POST':
        game_id = request.POST.get('validate')
        if game_id:
            if validate(game_id):
                success = True
                return render(request, 'play.html', { 'success' : success })
            else:
                message = 'Too bad. Keep trying!'
                game = get_cached_game()
                tiles = get_2d_array(get_cached_tiles(), game.play_image.level)
                return render(request, 'play.html', { 'images' : tiles, 'parent' : game, 'success' : success, 'message' : message})
        else:
            tile_id = request.POST.get('tile_id')
            if tile_id:
                game_info = do_one_move(int(tile_id))
        return render(request, 'play.html', { 'images' : game_info.tiles, 'parent' : game_info.game, 'success' : success, 'message' : message})

    elif request.method == 'GET':
        clear_cache()
        if id is None:
            all_imgs = PlayImage.objects.all()
            imgs = all_imgs[len(all_imgs)-1]
        else:
            imgs = PlayImage.objects.get(id = id)
        
        game_info = start_game(request, imgs)
        return render(request, 'play.html', { 'images' : game_info.tiles, 'parent' : game_info.game, 'success' : success, 'message' : message})


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