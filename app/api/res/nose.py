from PIL import Image, ImageDraw

'''
data is a dictionnary :
    nose.color
    nose.model
'''

class Nose():
    '''
        generate a nose
        different noses possible (2 yet)
    '''
    def __init__(self, size, data):
        self.size = int(size/10)
        self.data = data
        self.color = tuple(self.data["nose"]["color"])
        self.rotation = self.data["nose"]["rotation"] * 5
        
        self.im = Image.new("RGBA", (self.size,self.size//2), "#0000")
        self.draw = ImageDraw.Draw(self.im)
        self.width = self.size//20

    def draw_small(self):
        self.draw.line( ((self.size*4/20, self.size*3/20),(self.size*5/20, self.size*5/20)), fill=self.color, width=self.width)
        self.draw.line( ((self.size*16/20, self.size*3/20),(self.size*15/20, self.size*5/20)), fill=self.color, width=self.width)

    def draw_blush(self):
        self.draw.line( ((self.size*4/20, self.size*3/20),(self.size*5/20, self.size*5/20)), fill=self.color, width=self.width)
        self.draw.line( ((self.size*6/20, self.size*3/20),(self.size*7/20, self.size*5/20)), fill=self.color, width=self.width)
        self.draw.line( ((self.size*2/20, self.size*3/20),(self.size*3/20, self.size*5/20)), fill=self.color, width=self.width)

        self.draw.line( ((self.size*16/20, self.size*3/20),(self.size*15/20, self.size*5/20)), fill=self.color, width=self.width)
        self.draw.line( ((self.size*14/20, self.size*3/20),(self.size*13/20, self.size*5/20)), fill=self.color, width=self.width)
        self.draw.line( ((self.size*18/20, self.size*3/20),(self.size*17/20, self.size*5/20)), fill=self.color, width=self.width)

    def draw_nostril(self):
        poss = [(self.size/5,self.size/4), (self.size*4/5,self.size/4)]
        r = self.size/20
        for p in poss:
            self.draw.ellipse(((p[0]-r, p[1]-r), (p[0]+r, p[1]+r)), fill=self.color)

    def draw_triangle(self):
        x1,x2,x3 = self.size/6, self.size/2, self.size*5/6
        y1, y2 = self.size*5/6, self.size*1/6
        self.draw.polygon( ((x1,y1),(x2,y2),(x3,y1)) ,fill=self.color, width=self.width, outline=tuple([min(c+35,255) for c in self.color]))

    def get(self):
        if self.data["nose"]["model"] == "blush":
            self.draw_blush()
        elif self.data["nose"]["model"] == "small":
            self.draw_small()
        elif self.data["nose"]["model"] == "nostril":
            self.draw_nostril()
        elif self.data["nose"]["model"] == "triangle":
            self.draw_triangle()
        
        self.im = self.im.rotate( self.rotation, Image.Resampling.NEAREST, expand = 1 )

        return self.im