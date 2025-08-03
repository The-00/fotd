from PIL import Image, ImageDraw, ImageFilter
from api.res.models import FrogBodyModel
import munch

class FrogBody:
    '''
        generate a shape with the position of other elements
    '''
    def __init__(self, size:int, data:FrogBodyModel):
        self.data = data
        self.im = Image.new("RGBA", (size,size), "#0000")
        self.draw = ImageDraw.Draw(self.im)
        self.width, self.height = self.im.size

        self.left_eye_position = munch.Munch({
            "x": self.width*(7/24 + self.data.left_eye_position.x/40),
            "y": self.height*(10/24 + self.data.left_eye_position.y/60)
        })
        self.right_eye_position = munch.Munch({
            "x": self.width*(17/24 + self.data.right_eye_position.x/40),
            "y": self.height*(10/24 + self.data.right_eye_position.y/60)
        })
        
        self.left_eye_shape = munch.Munch({
            "width": self.width*(.17 + self.data.left_eye_shape.width/50),
            "height": self.height*(.17 + self.data.left_eye_shape.height/50)
        })
        self.right_eye_shape = munch.Munch({
            "width": self.width*(.17 + self.data.right_eye_shape.width/50),
            "height": self.height*(.17 + self.data.right_eye_shape.height/50)
        })

        self.mouth_position = munch.Munch({
            "x": self.width*(1/2 + self.data.mouth_position.x/40),
            "y": self.height*(1/2 + self.data.mouth_position.y/20)
        })

        self.nose_position = munch.Munch({
            "x": self.width*(1/2   + self.data.nose_position.x/40),
            "y": self.height*(19/48 + self.data.nose_position.y/50)
        })

        self.left_cheek_position = munch.Munch({
            "x": self.width*(1/3 + self.data.right_cheek_position.x/30),
            "y": self.height*(1/2 + self.data.right_cheek_position.y/20)
        })
        self.right_cheek_position = munch.Munch({
            "x": self.width*(2/3 + self.data.left_cheek_position.x/30),
            "y": self.height*(1/2 + self.data.left_cheek_position.y/20)
        })

        self.hat_position = munch.Munch({
            "x": self.width*(1/2 + self.data.hat_position.x/20),
            "y": self.height*(1/3 + self.data.hat_position.y/40)
        })

        self.shape = [(
            self.width*(1/6 + self.data.shape.width/20),
            self.height*(1/3 + self.data.shape.height/20),
            self.width*(5/6 - self.data.shape.width/20),
            self.height
            ),(
            self.width*(1/6 + self.data.shape.width/20),
            self.height*4/6 - self.height/10,
            self.width*(5/6 - self.data.shape.width/20),
            self.height*4/6 + self.height/10
        )]
        
        self.belly_shape = (
            self.width*(1/6 + self.data.belly_shape.width/20),
            self.mouth_position.y + self.height*(self.data.belly_shape.height/10),
            self.width*(5/6 - self.data.belly_shape.width/20),
            self.height
            )

    def get(self):

        # body shape generation
        self.draw.ellipse(self.shape[0], fill=self.data.color.as_rgb_tuple())
        self.draw.rectangle((0,(self.shape[1][1]+self.shape[1][3])/2,self.width,self.height), fill="#0000")
        self.draw.ellipse(self.shape[1], fill=self.data.color.as_rgb_tuple())

        # eyes
        for eye_position, eye_shape in [(self.left_eye_position, self.left_eye_shape), (self.right_eye_position,self.right_eye_shape)]:
            eye_bbox = (
                eye_position.x - eye_shape.width/2,
                eye_position.y - eye_shape.height/2,
                eye_position.x + eye_shape.width/2,   
                eye_position.y + eye_shape.height/2
            )
            self.draw.ellipse(eye_bbox, fill=self.data.color.as_rgb_tuple())

        mask = self.im.copy()
        
        # cheeks
        # radius = self.width *(1/10 - self.data["cheeks"]["radius"]/20)
        # color_cheek = tuple(self.data["cheeks"]["color"])
        # width_outline_cheek = self.data["cheeks"]["outline_width"]

        # bg = Image.new("RGBA", self.im.size, (color_cheek[0], color_cheek[1], color_cheek[2], 0))
        # bg_draw = ImageDraw.Draw(bg)

        # for posX,posY in self.posCheeks:
        #     bbox =  (posX - radius/2, posY - radius/2, posX + radius/2, posY + radius/2)
        #     bg_draw.ellipse(bbox, fill=color_cheek)

        # bg = bg.filter(ImageFilter.GaussianBlur(radius = width_outline_cheek))
        # self.im.alpha_composite(bg)
        

        self.draw.ellipse(self.belly_shape, fill=self.data.belly_color.as_rgb_tuple())

        new_im = Image.new("RGBA", self.im.size, "#0000")
        new_im.paste(self.im, mask=mask)
        self.im = new_im

        return self.im
