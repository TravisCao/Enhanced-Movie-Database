#!/Users/travis/opt/anaconda3/bin/python
import sqlite3 as sql
from bokeh.models import ColumnDataSource, DataTable, TableColumn, TextInput, Panel
import pandas.io.sql as psql  # type: ignore
import pandas as pd

from bokeh.io import show, output_file  # type: ignore
from bokeh.layouts import column, gridplot, row, layout  # type: ignore
from bokeh.plotting import curdoc, figure  # type: ignore


def table_tab(data, conn):

    init_query = "SELECT * from movie_basic_info"
    movies = psql.read_sql(init_query, conn).head(2000)
    source = ColumnDataSource(movies)
    textInput = TextInput(value=init_query, title="SQL query:")

    def make_columns(data):
        df_columns = list(data.columns)
        columns = [TableColumn(field=i, title=i) for i in df_columns]
        return columns

    def textInput_handler(attr, old_query, new_query):
        print("New label: " + new_query)
        query = new_query
        data = psql.read_sql(new_query, conn).head(2000)

        columns = make_columns(data)

        movie_table.source.data = data
        movie_table.columns = columns

    init_columns = make_columns(movies)

    textInput.on_change("value", textInput_handler)

    movie_table = DataTable(source=source, columns=init_columns, width=1000)

    layout = row(textInput, movie_table)

    tab = Panel(child=layout, title="Movie Table")

    return tab


# # curdoc().add_root(data_table, textInput)
# curdoc().add_root(layout)
# curdoc().title = "Movies"
