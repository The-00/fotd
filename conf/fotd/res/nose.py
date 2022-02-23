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
        self.size = int(size/15)
        self.data = data
        self.color = tuple(self.data["nose"]["color"])
        
        self.im = Image.new("RGBA", (self.size,self.size//2), "#0000")
        self.draw = ImageDraw.Draw(self.im)
        self.width = self.size//15

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

    def get(self):
        if self.data["nose"]["model"] == "blush":
            self.draw_blush()
        elif self.data["nose"]["model"] == "small":
            self.draw_small()
        else:
            self.draw_small()
        
        return self.im