import pandas as pd
import xlrd
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import row, column
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.io import curdoc
import datetime


class TimeGraph:
    def __init__(self, name, graph_name):
        self.df = pd.read_csv(name, parse_dates=["Start", "End"])
        self.df["Start_string"] = self.df["Start"].dt.strftime("%H:%M:%S")
        self.df["End_string"] = self.df["End"].dt.strftime("%H:%M:%S")
        self.df["Times_string"] = self.df["Times"]

        self.cds = ColumnDataSource(self.df)

        self.f = figure(width=1500, height=600, x_axis_type="datetime", y_axis_type="datetime")

        self.f.title.text=f"{graph_name} {self.df['Date'][0]} {self.df['Day'][0]} {self.df['Start'][0]}"
        self.f.title.text_color="Black"
        self.f.title.text_font="times"
        self.f.title.text_font_style="bold"
        self.f.xaxis.minor_tick_line_color=None
        self.f.yaxis.minor_tick_line_color=None
        self.f.xaxis.axis_label="Time (Seconds)"

        hover = HoverTool(tooltips=[("Start", "@Start_string"), ("End", "@End_string"), ("Duration", "@Times_string")])
        self.f.add_tools(hover)

    def graph_quad(self):
        self.f.yaxis[0].ticker.desired_num_ticks = 1
        self.f.quad(left="Start", right="End", top=1, bottom=0, color="blue", alpha=0.5, source=self.cds)

    def graph_line(self):
        self.f.line(x="Start", y="Times", color="blue", alpha=0.5, source=self.cds)

    def graph_triangle(self):
        self.f.triangle(x="Start", y="End", color="blue", alpha=0.5, source=self.cds)

    def graph_circle(self):
        self.f.circle(x="Start", y="End", color="blue", alpha=0.5, source=self.cds)

    def graph_vbar(self):
        self.f.vbar(x="Start", top="Times", width=4, bottom=0, color="blue", alpha=0.5, source=self.cds)


output_file("Motion-graph.html")

move = TimeGraph("Times_movement.csv", "Motion Graph")


move.graph_line()


show(column(move.f))
