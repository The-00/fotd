from PIL import Image, ImageDraw
from api.res.models import NoseModel, NoseModelList

class Nose():
    '''
        generate a nose
    '''
    def __init__(self, size:int, data:NoseModel):
        self.size = size
        self.data = data

    def draw_small(self):
        self.draw.line( ((self.size*4/20, self.size*3/20),(self.size*5/20, self.size*5/20)), fill=self.data.color.as_rgb_tuple(), width=int(self.data.stroke_width * self.size))
        self.draw.line( ((self.size*16/20, self.size*3/20),(self.size*15/20, self.size*5/20)), fill=self.data.color.as_rgb_tuple(), width=int(self.data.stroke_width * self.size))

    def draw_blush(self):
        self.draw.line( ((self.size*4/20, self.size*3/20),(self.size*5/20, self.size*5/20)), fill=self.data.color.as_rgb_tuple(), width=int(self.data.stroke_width * self.size))
        self.draw.line( ((self.size*6/20, self.size*3/20),(self.size*7/20, self.size*5/20)), fill=self.data.color.as_rgb_tuple(), width=int(self.data.stroke_width * self.size))
        self.draw.line( ((self.size*2/20, self.size*3/20),(self.size*3/20, self.size*5/20)), fill=self.data.color.as_rgb_tuple(), width=int(self.data.stroke_width * self.size))

        self.draw.line( ((self.size*16/20, self.size*3/20),(self.size*15/20, self.size*5/20)), fill=self.data.color.as_rgb_tuple(), width=int(self.data.stroke_width * self.size))
        self.draw.line( ((self.size*14/20, self.size*3/20),(self.size*13/20, self.size*5/20)), fill=self.data.color.as_rgb_tuple(), width=int(self.data.stroke_width * self.size))
        self.draw.line( ((self.size*18/20, self.size*3/20),(self.size*17/20, self.size*5/20)), fill=self.data.color.as_rgb_tuple(), width=int(self.data.stroke_width * self.size))

    def draw_nostril(self):
        poss = [(self.size/5,self.size/4), (self.size*4/5,self.size/4)]
        r = self.size/20
        for p in poss:
            self.draw.ellipse(((p[0]-r, p[1]-r), (p[0]+r, p[1]+r)), fill=self.data.color.as_rgb_tuple())

    def draw_triangle(self):
        x1,x2,x3 = self.size/6, self.size/2, self.size*5/6
        y1, y2 = self.size*5/6, self.size*1/6
        self.draw.polygon( ((x1,y1),(x2,y2),(x3,y1)) ,fill=self.data.color.as_rgb_tuple(), width=int(self.data.stroke_width * self.size), outline=tuple([min(c+35,255) for c in self.data.color.as_rgb_tuple()]))

    def get(self):
        self.im = Image.new("RGBA", (self.size,self.size//2), "#0000")
        self.draw = ImageDraw.Draw(self.im)

        if self.data.model_name == NoseModelList.blush:
            self.draw_blush()
        elif self.data.model_name == NoseModelList.small:
            self.draw_small()
        elif self.data.model_name == NoseModelList.nostril:
            self.draw_nostril()
        elif self.data.model_name == NoseModelList.triangle:
            self.draw_triangle()
        
        self.im = self.im.resize( (int(self.size * self.data.ratio),int(self.size * self.data.ratio)) )
        self.im = self.im.rotate( self.data.rotation, Image.Resampling.NEAREST, expand = 1 )
        if self.data.flip: self.im = self.im.transpose( method=Image.Transpose.FLIP_LEFT_RIGHT )

        return self.im