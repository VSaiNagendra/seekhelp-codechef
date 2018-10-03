"""seekhelp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from div import views

urlpatterns = [
    path(r'',views.home_view,name='index'),
    path(r'admin/', admin.site.urls),
    path('index/',views.index_view,name='index'),
    path('home/',views.home_view,name='home'),
    path('login/',views.login_view,name='login'),
    path('homerequests/',views.request_view,name='requests'),
    path('homesuggestions/',views.suggestions_view,name="suggestions"),
    path('logout/',views.logout,name='logout'),
    path('home/submit_request/',views.submit_request,name='submit_request'),
    path('home/reply_to_request/',views.reply_to_request,name="reply_to_request"),
    path('home/update_question/',views.update_question,name="update_question"),
    path('homegraph/',views.graph_view,name='graph')
]
