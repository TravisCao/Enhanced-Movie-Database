#!/usr/bin/env ipython
import os
import sqlite3 as sql
from os.path import dirname, join

import numpy as np
import pandas.io.sql as psql

from bokeh.io import curdoc
from bokeh.layouts import column, layout
from bokeh.models import (
    Panel,
    ColumnDataSource,
    Div,
    Select,
    Slider,
    TextInput,
    RangeSlider,
)
from bokeh.plotting import figure


def explorer_tab(conn):
    conn = sql.connect("../../database/movies.db")
    query = open(join(os.getcwd(), "explorer.sql")).read()

    movies = psql.read_sql(query, conn)
    source = ColumnDataSource(movies)

    # data processing
    movies.fillna(0, inplace=True)  # just replace missing values with zero
    movies["color"] = np.where(movies["Rating"] >= 6, "green", "grey")
    movies["color"] = np.where(movies["Rating"] >= 7, "orange", movies["color"])
    movies["color"] = np.where(movies["Rating"] >= 8, "purple", movies["color"])
    movies["color"] = np.where(movies["Rating"] >= 9, "red", movies["color"])

    movies["alpha"] = np.where(movies["Rating"] >= 8, 0.7, 0.25)
    movies["alpha"] = np.where(movies["Rating"] >= 9, 0.9, movies["alpha"])

    movies["Box_Office"] = movies.Box_Office.apply(lambda x: 10000 * x)
    movies["revenue"] = movies.Box_Office.apply(lambda x: "{:,d}".format(int(x)))

    movies["Duration"] = movies.Duration.apply(lambda x: int(float(x)))

    axis_map = {
        "Numeric Rating": "Rating",
        "Number of Reviews": "Reviewer",
        "Box Office (dollars)": "Box_Office",
        "Length (minutes)": "Duration",
        "Year": "Year",
    }

    # style of website
    desc = Div(
        text=open(join(os.getcwd(), "description.html")).read(),
        sizing_mode="stretch_width",
    )

    # Create Input controls

    rating = RangeSlider(
        title="Numeric rating",
        value=(6.0, 10.0),
        start=2.0,
        end=10.0,
        step=0.1,
        format="0,0",
    )

    BoxOffice = RangeSlider(
        title="Revenue",
        value=(2407000, 4418010000),
        start=10000,
        end=5682000000,
        step=1000000,
        format="0.0",
    )

    Length = RangeSlider(
        title="Length (minutes)",
        value=(90, 160),
        start=0,
        end=220,
        step=5,
        format="0.0",
    )

    reviews = RangeSlider(
        title="Number of reviews",
        value=(1175, 930036),
        start=36,
        end=1058032,
        step=10000,
    )
    genre = Select(
        title="Genre",
        value="All",
        options=open(join(os.getcwd(), "genres.txt")).read().split(),
    )
    title = TextInput(title="Movie title contains")
    x_axis = Select(
        title="X Axis", options=sorted(axis_map.keys()), value="Numeric Rating"
    )
    y_axis = Select(
        title="Y Axis", options=sorted(axis_map.keys()), value="Number of Reviews"
    )

    source = ColumnDataSource(
        data=dict(
            x=[],
            y=[],
            color=[],
            title=[],
            year=[],
            revenue=[],
            alpha=[],
            rating=[],
            link=[],
        )
    )

    TOOLTIPS = [
        ("Title", "@title"),
        ("link", "@link"),
        ("Year", "@year"),
        ("$", "@revenue"),
    ]
    p = figure(
        plot_height=500,
        plot_width=1000,
        title="",
        toolbar_location=None,
        tooltips=TOOLTIPS,
        sizing_mode="fixed",
    )

    p.circle(
        x="x",
        y="y",
        source=source,
        size=10,
        color="color",
        line_color=None,
        fill_alpha="alpha",
    )

    def select_movies():
        genre_val = genre.value
        title_val = title.value
        selected = movies[
            (movies.Reviewer >= reviews.value[0])
            & (movies.Reviewer <= reviews.value[1])
        ]
        selected = selected[
            (selected.Box_Office >= BoxOffice.value[0])
            & (selected.Box_Office <= BoxOffice.value[1])
        ]
        selected = selected[
            (selected.Box_Office >= BoxOffice.value[0])
            & (selected.Box_Office <= BoxOffice.value[1])
        ]
        selected = selected[
            (selected.Duration >= Length.value[0])
            & (selected.Duration <= Length.value[1])
        ]
        selected = selected[
            (selected.Rating >= rating.value[0]) & (selected.Rating <= rating.value[1])
        ]
        if genre_val != "All":
            selected = selected[selected.Genre.str.contains(genre_val) == True]
        if title_val != "":
            selected = selected[selected.Title.str.contains(title_val) == True]
        return selected

    def update():
        df = select_movies()
        x_name = axis_map[x_axis.value]
        y_name = axis_map[y_axis.value]

        p.xaxis.axis_label = x_axis.value
        p.yaxis.axis_label = y_axis.value
        p.title.text = "%d movies selected" % len(df)
        source.data = dict(
            x=df[x_name],
            y=df[y_name],
            color=df["color"],
            title=df["Title"],
            year=df["Year"],
            revenue=df["revenue"],
            alpha=df["alpha"],
            rating=df["Rating"],
            link=df["link"],
        )

    controls = [
        rating,
        BoxOffice,
        Length,
        reviews,
        genre,
        title,
        x_axis,
        y_axis,
    ]

    for control in controls:
        control.on_change("value", lambda attr, old, new: update())
    inputs = column(*controls, width=320, height=1000)
    inputs.sizing_mode = "fixed"
    l = layout([[desc], [inputs, p],], sizing_mode="scale_both")
    tab = Panel(child=l, title="Interactive Explorer")
    update()  # initial load of the data
    return tab


# curdoc().add_root(l)
# curdoc().title = "Movies"
