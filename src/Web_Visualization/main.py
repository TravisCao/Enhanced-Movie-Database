import sqlite3 as sql

import pandas.io.sql as psql
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Tabs
from bokeh.plotting import curdoc


from Tabs.explorer_tab import explorer_tab
from Tabs.table_tab import table_tab

CONN = sql.connect("../../database/movies.db")
INIT_QUERY = "SELECT * from movie_basic_info"
MOVIES = psql.read_sql(INIT_QUERY, CONN)
SOURCE = ColumnDataSource(MOVIES)


tab1 = table_tab(MOVIES, CONN)
tab2 = explorer_tab(CONN)

tabs = Tabs(tabs=[tab1, tab2])


curdoc().add_root(tabs)
curdoc().title = "Movies"
