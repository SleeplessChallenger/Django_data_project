from . import views
from django.urls import include, path
from rest_framework import routers
from django.contrib.auth.models import User


urlpatterns = [
	path('<int:server>/import/xlsx', views.DataLoader.as_view(), name='data-import'),
	path('<int:server>/export/sql', views.DataExtractSQL.as_view(), name='data-export-sql'),
	path('<int:server>/export/pandas', views.DataExtractPandas.as_view(), name='data-export-pandas'),
]