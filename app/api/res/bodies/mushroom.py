from PIL import Image, ImageDraw, ImageFilter
from api.res.models import FrogBodyModel
import munch

class MushroomBody:
    '''
        generate a shape with the position of other elements
    '''
    def __init__(self, size, data):
        self.data = data
        self.size = size
        self.im = Image.new("RGBA", (size,size), "#0000")
        self.draw = ImageDraw.Draw(self.im)

        self.width, self.height = size,size


        self.left_eye_position = munch.Munch({
            "x": self.width*(45/100 + self.data.left_eye_position.x/50),
            "y": self.height*(50/100 + self.data.left_eye_position.y/60)
        })
        self.right_eye_position = munch.Munch({
            "x": self.width*(55/100 + self.data.right_eye_position.x/50),
            "y": self.height*(50/100 + self.data.right_eye_position.y/60)
        })
    
        self.left_eye_shape = munch.Munch({
            "width": self.width*(.07 + self.data.left_eye_shape.width/50),
            "height": self.height*(.07 + self.data.left_eye_shape.height/50)
        })
        self.right_eye_shape = munch.Munch({
            "width": self.width*(.07 + self.data.right_eye_shape.width/50),
            "height": self.height*(.07 + self.data.right_eye_shape.height/50)
        })

        self.mouth_position = munch.Munch({
            "x": self.width*(1/2 + self.data.mouth_position.x/80),
            "y": self.height*(60/100 + self.data.mouth_position.y/20)
        })
        
        self.nose_position = munch.Munch({
            "x": self.width*(1/2   + self.data.nose_position.x/80),
            "y": self.height*(54/100 + self.data.nose_position.y/50)
        })

        self.left_cheek_position = munch.Munch({
            "x": self.width*(4/10 + self.data.right_cheek_position.x/30),
            "y": self.height*(60/100 + self.data.right_cheek_position.y/20)
        })
        self.right_cheek_position = munch.Munch({
            "x": self.width*(6/10 + self.data.left_cheek_position.x/30),
            "y": self.height*(60/100 + self.data.left_cheek_position.y/20)
        })

        self.hat_position = munch.Munch({
            "x": self.width*(1/2 + self.data.hat_position.x/20),
            "y": self.height*(1/5 + self.data.hat_position.y/40)
        })


        self.shape = [
                        (self.width*(4/10 + self.data.shape.width/25),
                            self.height*(1/3 + self.data.shape.height/20),
                            self.width*(5/10 - self.data.shape.width/25),
                            self.height*4/6 + self.height/10
                        ),
                        (self.width*(5/10 + self.data.shape.width/25),
                            self.height*(1/3 + self.data.shape.height/20),
                            self.width*(6/10 - self.data.shape.width/25),
                            self.height*4/6 + self.height/10
                        )
                    ]

        self.mushroom_hat_shape = [
                        (self.width*(1/8 + self.data.mushroom_hat_shape.width/20),
                            self.height*(1/6 + self.data.mushroom_hat_shape.height/20),
                            self.width*(7/8 - self.data.mushroom_hat_shape.width/20),
                            self.height/2
                        ),
                        (self.width*(1/8 + self.data.mushroom_hat_shape.width/20),
                            self.height*(1/3 + self.data.mushroom_hat_shape.height/40) - self.height/10,
                            self.width*(7/8 - self.data.mushroom_hat_shape.width/20),
                            self.height*(1/3 + self.data.mushroom_hat_shape.height/40) + self.height/10
                        )
                    ]

    def get(self):

        # hat shape generation

        self.imht = Image.new("RGBA", (self.width,self.height), "#0000")
        self.drawht = ImageDraw.Draw(self.imht)
        self.imhb = Image.new("RGBA", (self.width,self.height), "#0000")
        self.drawhb = ImageDraw.Draw(self.imhb)
        self.imh = Image.new("RGBA", (self.width,self.height), "#0000")

        self.drawht.ellipse(self.mushroom_hat_shape[0], fill=self.data.mushroom_hat_color.as_rgb_tuple(), outline=self.data.outline_color.as_rgb_tuple(), width=self.width//300)
        self.drawht.rectangle((0,(self.mushroom_hat_shape[1][1]+self.mushroom_hat_shape[1][3])/2+1,self.width,self.height), fill="#0000")
        
        self.drawhb.ellipse(self.mushroom_hat_shape[1], fill=self.data.mushroom_hat_color.as_rgb_tuple(), outline=self.data.outline_color.as_rgb_tuple(), width=self.width//300)
        self.drawhb.rectangle((0,0,self.width,(self.mushroom_hat_shape[1][1]+self.mushroom_hat_shape[1][3])/2-1), fill="#0000")

        self.imh.paste(self.imht, mask=self.imht)
        self.imh.paste(self.imhb, mask=self.imhb)

        # body shape generation

        self.draw.ellipse(self.shape[1], fill=self.data.color.as_rgb_tuple())
        self.draw.ellipse(self.shape[0], fill=self.data.color.as_rgb_tuple())
        self.draw.ellipse((    
            (self.shape[0][0] + self.shape[0][2])/2,
            (self.shape[0][3] - self.height/100),
            (self.shape[1][0] + self.shape[1][2])/2,
            (self.shape[0][3] + self.height/100) )
            , fill=self.data.color.as_rgb_tuple())
        self.draw.rectangle((
           (self.shape[0][0] + self.shape[0][2])/2,
           (self.shape[0][1]),
           (self.shape[1][0] + self.shape[1][2])/2,
           (self.shape[0][3])),
           fill=self.data.color.as_rgb_tuple())

        
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
        # radius = self.width *(1/15 - self.data["cheeks"]["radius"]/20)
        # color_cheek = tuple(self.data["cheeks"]["color"])
        # width_outline_cheek = self.data["cheeks"]["outline_width"]

        # bg = Image.new("RGBA", self.im.size, (color_cheek[0], color_cheek[1], color_cheek[2], 0))
        # bg_draw = ImageDraw.Draw(bg)

        # for posX,posY in self.posCheeks:
        #     bbox =  (posX - radius/2, posY - radius/2, posX + radius/2, posY + radius/2)
        #     bg_draw.ellipse(bbox, fill=color_cheek)

        # bg = bg.filter(ImageFilter.GaussianBlur(radius = width_outline_cheek))
        # self.im.alpha_composite(bg)
        
        new_im = Image.new("RGBA", self.im.size, "#0000")
        new_im.paste(self.im, mask=mask)
        self.im = new_im

        self.im.paste(self.imh, mask=self.imh)

        return self.im
