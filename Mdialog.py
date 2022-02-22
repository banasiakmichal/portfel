from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivymd.uix.list import ThreeLineListItem
from kivy_garden.graph import Graph, MeshLinePlot


class InfoDialog(MDDialog):
    """Basic dialog window"""

    dialog = None

    def __init__(self, text):
        self.text = text

    def dialog_(self, *args):
        if not self.dialog:
            self.dialog = MDDialog(
                text=self.text,
                radius=[20, 7, 20, 7],
            )
        self.dialog.open()

    """ section graph dialog window """


class Content(BoxLayout):
    """
    cls_content - Dialog window binded with ThreeLineAvatarItems - Cost in Project and Categories
        cost and time comes from app.open_graph_dialog """

    def __init__(self, cost, time, **kwargs):
        super().__init__(**kwargs)

        if cost and time:
            self.cost = cost
            self.time = time
            self.max = max(self.cost)
            Clock.schedule_once(self.graph, 0)
        else:
            self.cost = []
            self.time = []

    def graph(self, *args):
        """
        https://github.com/kivy-garden/graph/blob/27c93e044cdae041c3fd1c98548bce7494f61e9e/kivy_garden/graph/__init__.py#L159
            """
        l = [10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000]
        self.graph = Graph(xlabel='czas', ylabel='koszt',
                           y_ticks_major=list(filter(lambda x: x / 10 < self.max > x / 10, [x * 10 for x in l]))[0] / 10,
                           x_ticks_major=1,
                           border_color=[0.349, 0.349, 0.349, 1],
                           tick_color=[0.349, 0.349, 0.349, 1],
                           label_options={'color': [0.349, 0.349, 0.349, 1], 'bold': False},
                           draw_border=True,
                           y_grid_label=True, x_grid_label=True,
                           xmin=0, xmax=len(self.time),
                           ymin=0, ymax=self.max)
        self.plot = MeshLinePlot(color=[0.902, 0.494, 0.133, 1])
        self.plot.points = list(zip(range(len(self.time)), self.cost))
        self.graph.add_plot(self.plot)
        self.ids.graph.add_widget(self.graph)

        " scroll view with date and costs under graph "
        l = list(zip(self.time, self.cost))
        for i in l:
            self.ids.list.add_widget(ThreeLineListItem(text=f'{l.index(i)}',         #i[0]
                                                       secondary_text=f'{i[1]} zł',  #i[1]
                                                       tertiary_text=f'{i[0]}'))     #l.index(i) +1


class GraphDialog(MDDialog):
    dialog = None

    def __init__(self, cost, time, title, **kwargs):
        super().__init__(**kwargs)
        if cost and time:
            self.cost = cost
            self.time = time
            self.title = title
        else:
            self.cost = []
            self.time = []

    def show_graph(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title=f'{self.title}: ',
                type="custom",
                content_cls=Content(self.cost, self.time),
                buttons=[
                    MDFlatButton(
                        text="ZAMKNIJ",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda _: self.dialog.dismiss()
                    ),
                ],
            )
        self.dialog.open()