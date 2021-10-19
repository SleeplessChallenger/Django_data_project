import sqlite3


class SQL_Manager:
	def __init__(self, name):
		self.db = sqlite3.connect(name,
			check_same_thread=False)

	def _execute(self, data, values):
		with self.db:
			connect = self.db.cursor()
			connect.execute(data, values or [])
			return connect.fetchall()

	def select_data(self, table, criteria=None):
		criteria = criteria or {}
		statement = f'''SELECT * FROM {table}'''

		if criteria:
			placeholder = [f"{col}=?" for col in criteria.keys()]
			optional = ' AND '.join(placeholder)
			statement += f' WHERE {optional}'

		return self._execute(statement,
			list(criteria.values()))
