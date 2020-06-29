from django.contrib import admin
from django.urls import path
from .views import (
                banter_view,
                post_create,
                post_view,
                update_view,
                delete_view,
                share_view,
                )
#app name was indicated in urls.py since not part of main application urls.py
app_name = 'banter'

urlpatterns = [
    path('', banter_view, name="banter"),
    path('create/', post_create, name="create"),
    path('<slug>/update/', update_view, name="update"),
    path('<slug>/delete/', delete_view, name="delete"),
    path('<slug>/share', share_view, name="share"),
    path('<slug>/', post_view, name="detail"),
]
