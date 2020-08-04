from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.core.window import Window
import kivy.utils

class Node:
    def __init__(self,row,col,width,rows):
        self.row = row
        self.col = col

        #these are the absolute values:
        self.x = row * width
        self.y = col * width
        self.center = (self.x + width/2, self.y + width/2)

        self.colour = '#EBECED'
        self.width = width
        self.rows = rows

    def get_pos(self):
        return self.row, self.col

    def check_closed(self):
        return self.colour == '#4C586F'

    def check_open(self):
        return self.colour == '#A2AABO'

    def check_obs(self):
        return self.colour == '#3E3E3B'

    def check_start(self):
        return self.colour == '#BEC6C3'

    def check_end(self):
        return self.colour == '#626670'

    def make_closed(self):
        self.colour = '#4C586F'

    def make_open(self):
        self.colour = 'A2AABO'

    def make_obs(self):
        self.colour = '#3E3E3B'

    def make_start(self):
        self.colour = '#BEC6C3'

    def make_end(self):
        self.colour = '#626670'

    def make_path(self):
        self.colour = '#CBC5C1'

    def draw(self):
        RectWidget(colour_scheme=self.colour,center=self.center,width=self.width)

class RectWidget(Widget):
    def __init__(self,**kwargs):
        super(RectWidget,self).__init__()

        with self.canvas.before:
            Color(rgb=(kivy.utils.get_color_from_hex(kwargs['colour_scheme'])))
            self.rect = Rectangle(center=kwargs['center'],width=kwargs['width'])
        self.root.ids['game_screen'].ids['rect_widget'].add_widget(self.rect)

class LineWidget(Widget):
    def __init__(self,**kwargs):
        super(LineWidget,self).__init__()

        with self.canvas.before:
            Color(rgb=(kivy.utils.get_color_from_hex('#000000')))
            self.line = Line(points=kwargs['points'])
        self.root.ids['game_screen'].ids['line_widget'].add_widget(self.line)

class GameScreen(Widget):

    rows = 50

    def new_game(self,uLat,uLon,bLat,bLon):
        grid = make_grid(self.rows)

        start = Node(uLat,uLon,Window.width,self.rows) 
        end = Node(bLat,bLon,Window.width,self.rows)
        start.make_start()
        end.make_end()

        barriers = [[20,60,90],[45,78,64],[30,89,78]]

        while True:
            draw(grid,self.rows)

            #making barriers
            for counter, i in enumerate(barriers):
                for j in i:
                    barrier = Node(counter,j,Window.width,self.rows)
                    barrier.make_obs()

def draw(grid,rows):
    for row in grid:
        for rect_node in row:
            rect_node.draw()
    make_lines(rows)

def make_grid(rows):
    grid = []
    nodeWidth = Window.width//rows
    for r in range(rows):
        grid.append([])
        for c in range(rows):
            node = Node(r,c,nodeWidth,rows)
            grid[r].append(node)
    return grid

def make_lines(rows):
    nodeWidth = Window.width//rows
    #for every row, draw horizontal lines.
    for everyR in range(rows):
        LineWidget(points=[0,everyR*nodeWidth,Window.width,everyR*nodeWidth])
        for everyC in range(rows):
            #drawing vertical lines now
            LineWidget(points=[everyC*nodeWidth,0,Window.width,everyC*nodeWidth])

class GameApp(App):
    def on_start(self):
        self.root.new_game(0,0,50,29)

if __name__ == '__main__':
    GameApp().run()
