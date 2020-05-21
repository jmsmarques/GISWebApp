from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('register', views.register_view, name="register"),
    path('add_image', views.add_image, name="add_image"),
    path('remove_image', views.remove_image, name="remove_image"),
    path('download_image', views.download_image, name="download_image"),
]