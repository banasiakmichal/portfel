from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from math import sin
from kivy_garden.graph import Graph, MeshLinePlot, SmoothLinePlot
from kivy.core.window import Window
Window.size = (375, 667)


class MyApp(MDApp):

     def build(self):
         return Content()


class Content(MDBoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.graph = Graph(xlabel='czas', ylabel='kwota',
                           y_ticks_major=100, x_ticks_major=1,
                           border_color=[0, 1, 1, 1],
                           tick_color=[0, 1, 1, 0.7],
                           label_options={'color': [1, 0, 0, 1], 'bold': False},
                           draw_border=False,
                           y_grid_label=True, x_grid_label=True,
                           xmin=0, xmax=10,
                           ymin=0, ymax=100)
        self.plot = SmoothLinePlot(color=[1, 0, 0, 1])
        self.plot.points = [(1, 1), (2, 5), (3, 1), (4, 3)]
        self.graph.add_plot(self.plot)
        self.add_widget(self.graph)


MyApp().run()