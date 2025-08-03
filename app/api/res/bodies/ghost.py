from PIL import Image, ImageDraw, ImageFilter
from api.res.models import FrogBodyModel
import munch

class GhostBody:
    '''
        generate a shape with the position of other elements
    '''
    def __init__(self, size, data):
        self.data = data
        self.im = Image.new("RGBA", (size,size), "#0000")
        self.draw = ImageDraw.Draw(self.im)
        self.width, self.height = self.im.size
        self.dy = 100


        self.left_eye_position = munch.Munch({
            "x": self.width*(4/10 + self.data.left_eye_position.x/60),
            "y": self.dy + self.height*(3/10 + self.data.left_eye_position.y/60)
        })
        self.right_eye_position = munch.Munch({
            "x": self.width*(6/10 + self.data.right_eye_position.x/60),
            "y": self.dy + self.height*(3/10 + self.data.right_eye_position.y/60)
        })

        self.left_arm = munch.Munch({
            "length": round( (self.data.left_arm.length /20 +.3) * self.width),
            "thickness": round( (self.data.left_arm.thickness /50 +.05) * self.width ),
            "rotation": self.data.left_arm.rotation
        })
        self.right_arm = munch.Munch({
            "length": round( (self.data.right_arm.length /20 +.3) * self.width),
            "thickness": round( (self.data.right_arm.thickness /50 +.05) * self.width ),
            "rotation": self.data.right_arm.rotation
        })

        self.mouth_position = munch.Munch({
            "x": self.width*(1/2 + self.data.mouth_position.x/40),
            "y": self.dy + self.height*(1/3 + self.data.mouth_position.y/60)
        })

        self.nose_position = munch.Munch({
            "x": self.width*(1/2   + self.data.nose_position.x/40),
            "y": self.dy + self.height*(15/48 + self.data.nose_position.y/150)
        })

        self.hat_position = munch.Munch({
            "x": self.width*(1/2 + self.data.hat_position.x/40),
            "y": self.dy + self.height*(4/20 + self.data.hat_position.y/80)
        })

        self.shape = [(
            self.width*(5/20 + self.data.shape.width/20),
            self.dy + self.height*(4/20 + self.data.shape.height/20),
            self.width*(15/20 - self.data.shape.width/20),
            self.dy + self.height*1.2
        )]

        self.leaf_number = self.data.leaf_number
        self.leaf_space = round(self.data.leaf_space * self.leaf_number)
        

    def get(self):

        # body shape generation
        self.draw.ellipse(self.shape[0], fill=self.data.color.as_rgb_tuple())
        self.draw.rectangle((0,((self.shape[0][3] - self.shape[0][1]) / 2 + self.shape[0][1]),self.width,self.dy + self.height), fill="#0000")
#        self.draw.ellipse(self.shapeBody[1], fill="#f00" if debug else tuple(self.data["body"]["color"]))

        # arms
        d = self.shape[0][0] * .2
        left_arm_x, right_arm_x = round(self.shape[0][0]-self.left_arm.thickness-d), round(self.shape[0][2]+self.right_arm.thickness+d)
        arm_y = round( self.dy + self.height*4/10 )
        for arm, arm_x, is_right_arm in [(self.left_arm, left_arm_x, False), (self.right_arm, right_arm_x, True)]:
            arm_im = Image.new("RGBA", (arm.length, arm.thickness), "#0000")
            arm_draw = ImageDraw.Draw(arm_im)
            arm_draw.ellipse((0, 0, arm.length, arm.thickness), fill=self.data.color.as_rgb_tuple())
            arm_im = arm_im.rotate( arm.rotation, expand=True)

            if is_right_arm: arm_x-=arm_im.width
            self.im.paste(arm_im, (arm_x, arm_y), mask=arm_im)

        # bottom
        w = self.shape[0][2] - self.shape[0][0] + self.leaf_space
        n = self.leaf_number
        r = w / (2*n) - self.leaf_space/2
        x0 = self.shape[0][0]
        y = (self.shape[0][3] - self.shape[0][1]) / 2 + self.shape[0][1]

        for i in range(n):
            x = x0 + 2*i*(r+self.leaf_space/2) + r
            bbox = (x-r, y-r, x+r, y+r)
            self.draw.ellipse(bbox, fill=self.data.color.as_rgb_tuple())

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
        
        new_im = Image.new("RGBA", self.im.size, "#0000")
        new_im.paste(self.im, mask=mask)
        self.im = new_im

        return self.im
