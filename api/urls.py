from . import views
from django.urls import include, path
from rest_framework import routers
from django.contrib.auth.models import User


urlpatterns = [
	path('<int:server>/import/xlsx', views.DataLoader.as_view(), name='data-import')

]