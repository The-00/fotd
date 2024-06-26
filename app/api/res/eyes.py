from PIL import Image, ImageDraw
import math

'''
data is a dictionnary :
    eye.right.model
    eye.right.color.front
    eye.righ.color.back
    
    eye.left.model
    eye.left.color.front
    eye.left.color.back
'''

class Eyes:
    '''
        Generation of eyes
        different eye shape possible (9 yet)
    '''
    def __init__(self, size, data):
        self.data = data
        self.size = int(size)

        self.width = self.size//15

    def draw_circle(self):
        self.draw.ellipse((self.size/5,self.size/5,4/5*self.size,4/5*self.size),fill=self.bg_color)

    def draw_right(self):
        self.draw_circle()
        x1, x2 = self.size/3, self.size*2/3
        y1,y2,y3 = self.size/3, self.size/2, self.size*2/3
        self.draw.line( ((x1,y1),(x2,y2),(x1,y3)) ,fill=self.fg_color, width=self.width, joint='curve')

    def draw_line(self):
        self.draw_circle()
        x1, x2 = self.size/3, self.size*2/3
        y1, y2 = self.size/2, self.size/2
        self.draw.line( ((x1,y1),(x2,y2)) ,fill=self.fg_color, width=self.width, joint='curve')

    def draw_cross(self):
        self.draw_circle()
        x1, x2 = self.size/3, self.size*2/3
        y1, y2 = self.size/3, self.size*2/3
        self.draw.line( ((x1,y1),(x2,y2)) ,fill=self.fg_color, width=self.width, joint='curve')
        self.draw.line( ((x1,y2),(x2,y1)) ,fill=self.fg_color, width=self.width, joint='curve')

    def draw_left(self):
        self.draw_circle()
        x1, x2 = self.size*2/3, self.size*1/3
        y1,y2,y3 = self.size/3, self.size/2, self.size*2/3
        self.draw.line( ((x1,y1),(x2,y2),(x1,y3)) ,fill=self.fg_color, width=self.width, joint='curve')
    
    def draw_up(self):
        self.draw_circle()
        x1,x2,x3 = self.size/3, self.size/2, self.size*2/3
        y1, y2 = self.size*1/2, self.size*1/3  
        self.draw.line( ((x1,y1),(x2,y2),(x3,y1)) ,fill=self.fg_color, width=self.width, joint='curve')
    
    def draw_down(self):
        self.draw_circle()
        x1,x2,x3 = self.size/3, self.size/2, self.size*2/3
        y1, y2 = self.size*1/2, self.size*2/3  
        self.draw.line( ((x1,y1),(x2,y2),(x3,y1)) ,fill=self.fg_color, width=self.width, joint='curve')

    def draw_small(self):
        self.draw_circle()
        self.draw.ellipse((self.size*2/5,self.size*2/5,3/5*self.size,3/5*self.size),fill=self.fg_color)

    def draw_simple(self):
        self.draw_circle()
        self.draw.ellipse((self.size/3,self.size/3,2/3*self.size,2/3*self.size),fill=self.fg_color)

    def draw_heart(self):
        self.draw_circle()
        l = [ (self.size/3, self.size/2), (self.size/2, self.size*2/3), (self.size*2/3, self.size/2), (self.size/2, self.size/3)]
        self.draw.polygon( l ,fill=self.fg_color)

        centers = [((l[0][0]+l[3][0])/2, (l[0][1]+l[3][1])/2), ((l[2][0]+l[3][0])/2, (l[2][1]+l[3][1])/2)]
        r = self.size/12 * 2**.5
        for c in centers:
            self.draw.ellipse( [c[0]-r, c[1]-r, c[0]+r, c[1]+r] ,fill=self.fg_color)

    def draw_down_moon(self):
        self.draw_circle()
        self.draw.ellipse((self.size*3/12,self.size*3/12,9/12*self.size,9/12*self.size),fill=self.fg_color)
        self.draw.ellipse((self.size*4/12,self.size*1/2,8/12*self.size,9/12*self.size),fill=self.bg_color)

    def draw_up_moon(self):
        self.draw_circle()
        self.draw.ellipse((self.size*3/12,self.size*3/12,9/12*self.size,9/12*self.size),fill=self.fg_color)
        self.draw.ellipse((self.size*4/12,self.size*1/4,8/12*self.size,1/2*self.size),fill=self.bg_color)

    def draw_left_moon(self):
        self.draw_circle()
        self.draw.ellipse((self.size*3/12,self.size*3/12,9/12*self.size,9/12*self.size),fill=self.fg_color)
        self.draw.ellipse((self.size*1/4,self.size*4/12,1/2*self.size,8/12*self.size),fill=self.bg_color)

    def draw_right_moon(self):
        self.draw_circle()
        self.draw.ellipse((self.size*3/12,self.size*3/12,9/12*self.size,9/12*self.size),fill=self.fg_color)
        self.draw.ellipse((self.size*1/2,self.size*4/12,3/4*self.size,8/12*self.size),fill=self.bg_color)

    def draw_big(self):
        self.draw_circle()
        self.draw.ellipse((self.size*3/12,self.size*3/12,9/12*self.size,9/12*self.size),fill=self.fg_color)

    def draw_star(self):
        self.draw_circle()
        x_coords = [math.cos(2*math.pi * (i/2) / 5 - math.pi/10)/(5+7*(i%2)) + 1/2 for i in range(10)]
        y_coords = [math.sin(2*math.pi * (i/2) / 5 - math.pi/10)/(5+7*(i%2)) + 1/2 for i in range(10)]
        coords = list(zip([v*self.size for v in x_coords], [v*self.size for v in y_coords]))
        self.draw.polygon(coords ,fill=self.fg_color, width=self.width)

    def get(self):
        
        imgs = []
        
        for side in ["left", "right"]:
                    
            self.im = Image.new("RGBA", (self.size,self.size), "#0000")
            self.draw = ImageDraw.Draw(self.im)
            
            self.model = self.data["eye"][side]['model']
            self.models = [">","<","o","O",".","-","x","♥"," ","n","u","(",")","^","v","*"]
            if self.model not in self.models:
                self.model = rd.choice( self.models )
            
            self.fg_color = tuple(self.data["eye"][side]["color"]["front"])
            self.bg_color = tuple(self.data["eye"][side]["color"]["back"])
            
            if self.model == ">":
                self.draw_right()
            elif self.model == "<":
                self.draw_left()
            elif self.model == "o":
                self.draw_simple()
            elif self.model == "O":
                self.draw_big()
            elif self.model == ".":
                self.draw_small()
            elif self.model == "-":
                self.draw_line()
            elif self.model == "x":
                self.draw_cross()
            elif self.model == "♥":
                self.draw_heart()
            elif self.model == " ":
                self.draw_circle()
            elif self.model == "(":
                self.draw_left_moon()
            elif self.model == ")":
                self.draw_right_moon()
            elif self.model == "n":
                self.draw_down_moon()
            elif self.model == "u":
                self.draw_up_moon()
            elif self.model == "^":
                self.draw_up()
            elif self.model == "v":
                self.draw_down()
            elif self.model == "*":
                self.draw_star()
            
            imgs.append(self.im)

        return imgs