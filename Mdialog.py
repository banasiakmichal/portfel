from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivymd.uix.list import ThreeLineListItem
from kivy_garden.graph import Graph, MeshLinePlot
from kivymd.uix.label import MDLabel


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

        if len(cost) and len(time) > 1:
            self.cost = cost
            self.time = time
            self.max = max(self.cost)
            Clock.schedule_once(self.graph, 0)
        else:
            self.cost = []
            self.time = []
            self.l = MDLabel(text='Nie masz jeszcze kosztów do wyświetlenia.')
            self.ids.graph.add_widget(self.l)

    def graph(self, *args):
        """
        https://github.com/kivy-garden/graph/blob/27c93e044cdae041c3fd1c98548bce7494f61e9e/kivy_garden/graph/__init__.py#L159

            y_ticks_major:
                if max(cost) in range(0,1)
                    y_t_m = max(cost)
                else:
                    y_t_m = max(cost) / 10
        """
        m = int(max(self.cost))
        def f(x): return x / 10 if (x in range(0, 1)) else(x)

        self.graph = Graph(xlabel='czas', ylabel='koszt',
                           y_ticks_major=f(m),
                           x_ticks_major=1,
                           border_color=[0.349, 0.349, 0.349, 1],
                           tick_color=[0.349, 0.349, 0.349, 1],
                           label_options={'color': [1, 0.647, 0], 'bold': False},
                           draw_border=True,
                           y_grid_label=True, x_grid_label=True,
                           xmin=0, xmax=len(self.time),
                           ymin=0, ymax=self.max)
        self.plot = MeshLinePlot(color=[1, 0.647, 0])
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