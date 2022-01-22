"""
Definition of urls for python_webapp_django.
"""

from datetime import datetime
from django.urls import path
import django.contrib.auth.views
from django.views.static import serve
from django.conf import settings
import app.forms
import app.views as a_v
from app.views import signup_view

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    path('', app.views.home, name='home'),
    path('contact', app.views.contact, name='contact'),
    path('about', app.views.about, name='about'),
    path('play', app.views.about, name='play'),
    path('login/',
        django.contrib.auth.views.LoginView.as_view(),
        {
            'template_name': 'login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout',
        django.contrib.auth.views.LogoutView.as_view(),
        {
            'next_page': '/',
        },
        name='logout'),
    path('static/(<path>.*)', serve,{'document_root': settings.STATIC_ROOT}),

    # Uncomment the admin/doc line below to enable admin documentation:
    # path(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #path(r'^admin/', include(admin.site.urls)),
]
