from django.urls import path
from . import views

# NO LEADING SLASHES
urlpatterns = [
    path('', views.index),
    path('register',views.register),
    path('login',views.login),
    path('wall',views.wall),
    path('logout',views.logout),
    path('post_message',views.post_message),
    path('comment/<int:id>',views.comment),
    path('wall/<int:id>/delete',views.delete),
    path('wall/<int:id>/delete',views.delete),
    path('wall/<int:id>/deletemsg',views.deletemsg),
]
