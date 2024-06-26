"""
URL configuration for SA_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib import admin
from django.urls import path


urlpatterns = [
    # path('', index),
    # path('search/', PublisherDocumentView.as_view({'get': 'list'})),
    path('api/user/', include(('user.urls', 'user'))),
    path('api/Administrator/', include(('Administrator.urls', 'Administrator'))),
    path('api/browhistory/',include(('Browhistory.urls', 'Browhistory'))),
    path('api/academia/', include(('Academia.urls', 'Academia'))),
    path('api/message/', include(('message.urls', 'message'))),
    # path('api/Academia/', include(('Academia.urls', 'Academia'))),
]
