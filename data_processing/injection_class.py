import pandas as pd
import dateutil.parser as dparser
from dateutil.tz import tzutc,gettz
from abc import ABC, abstractmethod
from api.models import DataClass
from pathlib import Path
import os


class Loader(ABC):
	@abstractmethod
	def __call__(self):
		raise NotImplemneterError("You didn't realize it")


class ExcelLoader(Loader):
	'''
	self.name can be changed
	'''
	def __init__(self):
		self.root = ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
		self.name = 'testData.xlsx'
		self.excel = os.path.join(self.root, self.name)
		self.model = DataClass.objects
		self.db_columns = {
			'Rep_dt': 'rep_dt', 'Delta': 'delta'
		}

		with open(self.excel, 'rb') as file:
			self.df = pd.read_excel(file)
			self.columns = list(self.df.columns)
			self._check_columns()

	def __repr__(self):
		return f"{self.name} loader"

	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, var):
		self._name = var

	def _check_columns(self):
		if len(self.columns) != 2:
			raise ValueError("Incorrect number of columns")

	def __call__(self):
		ht ={}

		for col in self.columns:
			correct_col = self.db_columns.get(col)
			data = self.df[col]

			if correct_col == 'rep_dt':
				data = self._change_format(data)
			else:
				data = self._simple_convert(data)

			ht[correct_col] = data

		for i in self._yield_data(ht):
		
			self.model.create(
				rep_dt=i[0],
				delta=i[1],
			)

	def _yield_data(self, ht):
		for i in list(zip(ht['rep_dt'], ht['delta'])):
			yield i

	def _change_format(self, data):
		return list(dparser.parse(i,fuzzy=True).astimezone(gettz("CET")) for i in data.values)

	def _simple_convert(self, data):
		'''
		1. Retrieve data (values) from hashtable
		2. Check for ','
		3. Cast everything into float 
		'''
		result = list(map(lambda x: float(x.replace(',', '.'))
			if type(x) == str else float(x), data))

		return result
