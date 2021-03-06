from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import DataSerializer
from .models import DataClass
from rest_framework import status
import dateutil.parser as dparser
from data_processing.injection_class import ExcelLoader
from data_processing.sql_actions import SQL_Manager
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

loader = ExcelLoader()
db_manager = SQL_Manager(BASE_DIR / 'db.sqlite3')
table_name = 'api_dataclass'


class DataLoader(APIView):
	serializer_class = DataSerializer

	def get(self, request, server=None):
		'''
		To see all data
		'''
		if not server:
			return Response(
				{'message': "No server is provided"},
				status=status.HTTP_406_NOT_ACCEPTABLE)

		all_data = DataClass.objects.all()
		serializer = self.serializer_class(all_data, many=True)
		return Response({'message': serializer.data},
			status=status.HTTP_200_OK)

	def post(self, request, server=None):
		'''
		We don't have any data in request,
		hence no need to use serializer.data
		'''
		if not server:
			return Response(
				{'message': "No server is provided"},
				status=status.HTTP_406_NOT_ACCEPTABLE)

		isData = DataClass.objects.all()

		if not isData:

			# empty => dump data
			self._insert_data(request)
		else:
		# clean
			self._delete_data(DataClass)
			self._insert_data(request)

		return Response({'message': 'OK'},
			status=status.HTTP_200_OK)

	def _delete_data(self, table):
		table.objects.all().delete()

	def _insert_data(self, request):
		loader()


class DataExtractSQL(APIView):
	def get(self, request, server=None):
		if not server:
			return Response(
				{'message': 'No server is provided'},
				status=status.HTTP_406_NOT_ACCEPTABLE)

		result = db_manager.select_data(table_name)

		return Response({'message': result},
			status=status.HTTP_200_OK)

		
class DataExtractPandas(APIView):
	serializer_class = DataSerializer

	def get(self, request, server=None):
		if not server:
			return Response(
				{'message': 'No server is provided'},
				status=status.HTTP_406_NOT_ACCEPTABLE)

		data = DataClass.objects.all()
		if not data:
			return Response({'message': 'No data in db'},
				status=status.HTTP_400_BAD_REQUEST)

		serializer = self.serializer_class(data, many=True)
		
		# place name of cols same to one in db
		df = pd.DataFrame(serializer.data, columns=['pk', 'rep_dt', 'delta'])
		df = df.rename(columns={'rep_dt': 'data', 'pk': 'id'})

		return Response({'message': df},
			status=status.HTTP_200_OK)
