<h2>Django-data project</h2>

In this project I implemented various actions with data by Django

<ul>
	<li>Load from Excel to DB</li>
	<li>Exporting from DB with SQL-RAW actions</li>
	<li>Exporting from DB with Pandas actions</li>
</ul>

<h3>Data loading steps</h3>

 - `data_processing` folder you can find `view` which in-turn triggers
 	`Injector` to load data from Excel to DB

 	<article>Actions considering loading</article>

	<ol>
		<li>Read data from Excel via Pandas</li>
		<li>Map correct columns from Pandas to model in DB</li>
		<li>If col. is <ins>datetime</ins>, then change format to **not naive timezone**</li>
		<li>If col. is <ins>delta</ins>, then, depending on the cell format, convert to float and replace ',' if exists</li>
		<li>Use `generator` with `zip` to fill two cols. of DB simultaneously</li>
	</ol>

<h3>CRUD methods</h3>

1. If **POST** is sent => load from Excel will be done + if DB isn't empty -> `clear()` at first
2. Depending on the URL, **GET** will retrieve and do actions with data either via SQL or Pandas

<h3>Further remarks</h3>

1. when putting data from `db` to pandas `DataFrame`, at first use same columns in df
2. How to figure out SQL table name in db?
	- https://docs.djangoproject.com/en/3.2/topics/db/sql/#executing-custom-sql-directly
	- look at folder where model is, take it lower case + _ + lower case of the model
