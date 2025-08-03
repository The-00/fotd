from PIL import Image, ImageDraw
import math
from api.res.models import EyeModel, EyeModelList

class Eye:
    '''
        Generation of eyes
        different eye shape possible (9 yet)
    '''
    def __init__(self, size:int, data:EyeModel):
        self.data = data
        self.size = size

    def draw_circle(self):
        self.draw.ellipse((self.size/5,self.size/5,4/5*self.size,4/5*self.size),fill=self.data.back_color.as_rgb_tuple())

    def draw_right(self):
        self.draw_circle()
        x1, x2 = self.size/3, self.size*2/3
        y1,y2,y3 = self.size/3, self.size/2, self.size*2/3
        self.draw.line( ((x1,y1),(x2,y2),(x1,y3)) ,fill=self.data.pupil_color.as_rgb_tuple(), width=int(self.data.stroke_width * self.size), joint='curve')

    def draw_line(self):
        self.draw_circle()
        x1, x2 = self.size/3, self.size*2/3
        y1, y2 = self.size/2, self.size/2
        self.draw.line( ((x1,y1),(x2,y2)) ,fill=self.data.pupil_color.as_rgb_tuple(), width=int(self.data.stroke_width * self.size), joint='curve')

    def draw_cross(self):
        self.draw_circle()
        x1, x2 = self.size/3, self.size*2/3
        y1, y2 = self.size/3, self.size*2/3
        self.draw.line( ((x1,y1),(x2,y2)) ,fill=self.data.pupil_color.as_rgb_tuple(), width=int(self.data.stroke_width * self.size), joint='curve')
        self.draw.line( ((x1,y2),(x2,y1)) ,fill=self.data.pupil_color.as_rgb_tuple(), width=int(self.data.stroke_width * self.size), joint='curve')

    def draw_left(self):
        self.draw_circle()
        x1, x2 = self.size*2/3, self.size*1/3
        y1,y2,y3 = self.size/3, self.size/2, self.size*2/3
        self.draw.line( ((x1,y1),(x2,y2),(x1,y3)) ,fill=self.data.pupil_color.as_rgb_tuple(), width=int(self.data.stroke_width * self.size), joint='curve')
    
    def draw_up(self):
        self.draw_circle()
        x1,x2,x3 = self.size/3, self.size/2, self.size*2/3
        y1, y2 = self.size*1/2, self.size*1/3  
        self.draw.line( ((x1,y1),(x2,y2),(x3,y1)) ,fill=self.data.pupil_color.as_rgb_tuple(), width=int(self.data.stroke_width * self.size), joint='curve')
    
    def draw_down(self):
        self.draw_circle()
        x1,x2,x3 = self.size/3, self.size/2, self.size*2/3
        y1, y2 = self.size*1/2, self.size*2/3  
        self.draw.line( ((x1,y1),(x2,y2),(x3,y1)) ,fill=self.data.pupil_color.as_rgb_tuple(), width=int(self.data.stroke_width * self.size), joint='curve')

    def draw_small(self):
        self.draw_circle()
        self.draw.ellipse((self.size*2/5,self.size*2/5,3/5*self.size,3/5*self.size),fill=self.data.pupil_color.as_rgb_tuple())

    def draw_simple(self):
        self.draw_circle()
        self.draw.ellipse((self.size/3,self.size/3,2/3*self.size,2/3*self.size),fill=self.data.pupil_color.as_rgb_tuple())

    def draw_heart(self):
        self.draw_circle()
        l = [ (self.size/3, self.size/2), (self.size/2, self.size*2/3), (self.size*2/3, self.size/2), (self.size/2, self.size/3)]
        self.draw.polygon( l ,fill=self.data.pupil_color.as_rgb_tuple())

        centers = [((l[0][0]+l[3][0])/2, (l[0][1]+l[3][1])/2), ((l[2][0]+l[3][0])/2, (l[2][1]+l[3][1])/2)]
        r = self.size/12 * 2**.5
        for c in centers:
            self.draw.ellipse( [c[0]-r, c[1]-r, c[0]+r, c[1]+r] ,fill=self.data.pupil_color.as_rgb_tuple())

    def draw_down_moon(self):
        self.draw_circle()
        self.draw.ellipse((self.size*3/12,self.size*3/12,9/12*self.size,9/12*self.size),fill=self.data.pupil_color.as_rgb_tuple())
        self.draw.ellipse((self.size*4/12,self.size*1/2,8/12*self.size,9/12*self.size),fill=self.data.back_color.as_rgb_tuple())

    def draw_up_moon(self):
        self.draw_circle()
        self.draw.ellipse((self.size*3/12,self.size*3/12,9/12*self.size,9/12*self.size),fill=self.data.pupil_color.as_rgb_tuple())
        self.draw.ellipse((self.size*4/12,self.size*1/4,8/12*self.size,1/2*self.size),fill=self.data.back_color.as_rgb_tuple())

    def draw_left_moon(self):
        self.draw_circle()
        self.draw.ellipse((self.size*3/12,self.size*3/12,9/12*self.size,9/12*self.size),fill=self.data.pupil_color.as_rgb_tuple())
        self.draw.ellipse((self.size*1/4,self.size*4/12,1/2*self.size,8/12*self.size),fill=self.data.back_color.as_rgb_tuple())

    def draw_right_moon(self):
        self.draw_circle()
        self.draw.ellipse((self.size*3/12,self.size*3/12,9/12*self.size,9/12*self.size),fill=self.data.pupil_color.as_rgb_tuple())
        self.draw.ellipse((self.size*1/2,self.size*4/12,3/4*self.size,8/12*self.size),fill=self.data.back_color.as_rgb_tuple())

    def draw_big(self):
        self.draw_circle()
        self.draw.ellipse((self.size*3/12,self.size*3/12,9/12*self.size,9/12*self.size),fill=self.data.pupil_color.as_rgb_tuple())

    def draw_star(self):
        self.draw_circle()
        x_coords = [math.cos(2*math.pi * (i/2) / 5 - math.pi/10)/(5+7*(i%2)) + 1/2 for i in range(10)]
        y_coords = [math.sin(2*math.pi * (i/2) / 5 - math.pi/10)/(5+7*(i%2)) + 1/2 for i in range(10)]
        coords = list(zip([v*self.size for v in x_coords], [v*self.size for v in y_coords]))
        self.draw.polygon(coords ,fill=self.data.pupil_color.as_rgb_tuple(), width=int(self.data.stroke_width * self.size))

    def get(self):
        self.im = Image.new("RGBA", (self.size,self.size), "#0000")
        self.draw = ImageDraw.Draw(self.im)
        
        if self.data.model_name == EyeModelList.pleated_right:
            self.draw_right()
        elif self.data.model_name == EyeModelList.pleated_left:
            self.draw_left()
        elif self.data.model_name == EyeModelList.pleated_up:
            self.draw_up()
        elif self.data.model_name == EyeModelList.pleated_down:
            self.draw_down()
        elif self.data.model_name == EyeModelList.normal:
            self.draw_simple()
        elif self.data.model_name == EyeModelList.big:
            self.draw_big()
        elif self.data.model_name == EyeModelList.small:
            self.draw_small()
        elif self.data.model_name == EyeModelList.closed:
            self.draw_line()
        elif self.data.model_name == EyeModelList.dead:
            self.draw_cross()
        elif self.data.model_name == EyeModelList.love:
            self.draw_heart()
        elif self.data.model_name == EyeModelList.none:
            self.draw_circle()
        elif self.data.model_name == EyeModelList.moon_left:
            self.draw_left_moon()
        elif self.data.model_name == EyeModelList.moon_right:
            self.draw_right_moon()
        elif self.data.model_name == EyeModelList.moon_up:
            self.draw_down_moon()
        elif self.data.model_name == EyeModelList.moon_down:
            self.draw_up_moon()
        elif self.data.model_name == EyeModelList.star:
            self.draw_star()
        
        self.im = self.im.resize( (int(self.size * self.data.ratio),int(self.size * self.data.ratio)) )
        self.im = self.im.rotate( self.data.rotation, Image.Resampling.NEAREST, expand = 1 )
        if self.data.flip: self.im = self.im.transpose( method=Image.Transpose.FLIP_LEFT_RIGHT )

        return self.im