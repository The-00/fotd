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

        self.shape = [
                        (self.width*(1/6 + self.data.shape.width/20),
                            self.height*(1/3 + self.data.shape.height/20),
                            self.width*(5/6 - self.data.shape.width/20),
                            self.height
                        ),
                        (self.width*(1/6 + self.data.shape.width/20),
                            self.height*4/6 - self.height/10,
                            self.width*(5/6 - self.data.shape.width/20),
                            self.height*4/6 + self.height/10
                            )
                        ]

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
        
        new_im = Image.new("RGBA", self.im.size, "#0000")
        new_im.paste(self.im, mask=mask)
        self.im = new_im

        return self.im


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

        self.left_cheek_position = munch.Munch({
            "x": self.width*(1/3 + self.data.right_cheek_position.x/30),
            "y": self.dy + self.height*(1/3 + self.data.right_cheek_position.y/20)
        })
        self.right_cheek_position = munch.Munch({
            "x": self.width*(2/3 + self.data.left_cheek_position.x/30),
            "y": self.dy + self.height*(1/3 + self.data.left_cheek_position.y/20)
        })
        self.hat_position = munch.Munch({
            "x": self.width*(1/2 + self.data.hat_position.x/40),
            "y": self.dy + self.height*(4/20 + self.data.hat_position.y/80)
        })

        self.shape = [
                            (self.width*(5/20 + self.data.shape.width/20),
                             self.dy + self.height*(4/20 + self.data.shape.height/20),
                             self.width*(15/20 - self.data.shape.width/20),
                             self.dy + self.height*1.2
                            )
                        ]
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


class MushroomBody:
    '''
        generate a shape with the position of other elements
    '''
    def __init__(self, size, data):
        self.data = data
        self.size = size
        self.im = Image.new("RGBA", (size,size), "#0000")
        self.draw = ImageDraw.Draw(self.im)

        self.x, self.y = size,size


        self.posEyes   = [
                            (self.x*(45/100 + 2*self.data["eye"]["left"]["position"]["x"]/100),
                             self.y*(50/100 + self.data["eye"]["left"]["position"]["y"]/60)
                            ),
                            (self.x*(55/100 - 2*self.data["eye"]["right"]["position"]["x"]/100),
                             self.y*(50/100 + self.data["eye"]["right"]["position"]["y"]/60)
                            )
                        ]
        self.shapeEyes = [
                            self.x*(.07 + self.data["eye"]["shape"]["width"]/50),
                            self.y*(.07 + self.data["eye"]["shape"]["height"]/50),
                            self.x*(.09 + min(self.data["eye"]["shape"]["width"], self.data["eye"]["shape"]["height"])/50)
                        ]
        self.posMouth = [
                            self.x*(1/2 + self.data["mouth"]["position"]["x"]/80),
                            self.y*(60/100 + self.data["mouth"]["position"]["y"]/20)
                        ]
        self.posNose = [
                            self.x*(1/2   + self.data["nose"]["position"]["x"]/80),
                            self.y*(54/100 + self.data["nose"]["position"]["y"]/50)
                        ]
        self.posCheeks = [
                            (self.x*(4/10 + self.data["cheeks"]["right"]["position"]["x"]/30),
                             self.y*(60/100 + self.data["cheeks"]["right"]["position"]["y"]/20)
                            ),
                            (self.x*(6/10 + self.data["cheeks"]["left"]["position"]["x"]/30),
                             self.y*(60/100 + self.data["cheeks"]["left"]["position"]["y"]/20)
                            )
                        ]
        self.posHat = [
                            self.x*(1/2 + self.data["hat"]["position"]["x"]/20),
                            self.y*(1/5 + self.data["hat"]["position"]["y"]/40)
                        ]
        self.shapeBody = [
                            (self.x*(4/10 + self.data["body"]["shape"]["width"]/25),
                             self.y*(1/3 + self.data["body"]["shape"]["height"]/20),
                             self.x*(5/10 - self.data["body"]["shape"]["width"]/25),
                             self.y*4/6 + self.y/10
                            ),
                            (self.x*(5/10 + self.data["body"]["shape"]["width"]/25),
                             self.y*(1/3 + self.data["body"]["shape"]["height"]/20),
                             self.x*(6/10 - self.data["body"]["shape"]["width"]/25),
                             self.y*4/6 + self.y/10
                            ),
                        ]
        self.shapeBodyHat = [
                            (self.x*(1/8 + self.data["body"]["hat"]["shape"]["width"]/20),
                             self.y*(1/6 + self.data["body"]["hat"]["shape"]["height"]/20),
                             self.x*(7/8 - self.data["body"]["hat"]["shape"]["width"]/20),
                             self.y/2
                            ),
                            (self.x*(1/8 + self.data["body"]["hat"]["shape"]["width"]/20),
                             self.y*(1/3 + self.data["body"]["hat"]["shape"]["height"]/40) - self.y/10,
                             self.x*(7/8 - self.data["body"]["hat"]["shape"]["width"]/20),
                             self.y*(1/3 + self.data["body"]["hat"]["shape"]["height"]/40) + self.y/10
                            )
                        ]

    def get(self, debug=False):

        # hat shape generation

        self.imht = Image.new("RGBA", (self.x,self.y), "#0000")
        self.drawht = ImageDraw.Draw(self.imht)
        self.imhb = Image.new("RGBA", (self.x,self.y), "#0000")
        self.drawhb = ImageDraw.Draw(self.imhb)
        self.imh = Image.new("RGBA", (self.x,self.y), "#0000")

        self.drawht.ellipse(self.shapeBodyHat[0], fill="#f00" if debug else tuple(self.data["body"]["hat"]["color"]), outline=self.data['body']['outline_color'], width=self.x//300)
        self.drawht.rectangle((0,(self.shapeBodyHat[1][1]+self.shapeBodyHat[1][3])/2+1,self.x,self.y), fill="#0000")
        
        self.drawhb.ellipse(self.shapeBodyHat[1], fill="#f00" if debug else tuple(self.data["body"]["hat"]["color"]), outline=self.data['body']['outline_color'], width=self.x//300)
        self.drawhb.rectangle((0,0,self.x,(self.shapeBodyHat[1][1]+self.shapeBodyHat[1][3])/2-1), fill="#0000")

        self.imh.paste(self.imht, mask=self.imht)
        self.imh.paste(self.imhb, mask=self.imhb)

        # body shape generation
        self.data["body"]["color"]  = tuple( [ int(min(255 ,max(0 ,-25+x+40*(self.data['special'][i])))) for i,x in enumerate(self.data["body"]["color"]) ] )

        self.draw.ellipse(self.shapeBody[1], fill="#f00" if debug else tuple(self.data["body"]["color"]))
        self.draw.ellipse(self.shapeBody[0], fill="#f00" if debug else tuple(self.data["body"]["color"]))
        self.draw.ellipse((    
            (self.shapeBody[0][0] + self.shapeBody[0][2])/2,
            (self.shapeBody[0][3] - self.y/100),
            (self.shapeBody[1][0] + self.shapeBody[1][2])/2,
            (self.shapeBody[0][3] + self.y/100) )
            , fill="#f00" if debug else tuple(self.data["body"]["color"]))
        self.draw.rectangle((
           (self.shapeBody[0][0] + self.shapeBody[0][2])/2,
           (self.shapeBody[0][1]),
           (self.shapeBody[1][0] + self.shapeBody[1][2])/2,
           (self.shapeBody[0][3])),
           fill="#f00" if debug else tuple(self.data["body"]["color"]))

        
        # eyes
        for posX,posY in self.posEyes:
            bbox =  (posX - self.shapeEyes[0]/2, posY - self.shapeEyes[1]/2, posX + self.shapeEyes[0]/2, posY + self.shapeEyes[1]/2)
            self.draw.ellipse(bbox, fill="#0f0" if debug else tuple(self.data["body"]["color"]))

        mask = self.im.copy()
        
        # cheeks
        radius = self.x *(1/15 - self.data["cheeks"]["radius"]/20)
        color_cheek = tuple(self.data["cheeks"]["color"])
        width_outline_cheek = self.data["cheeks"]["outline_width"]

        bg = Image.new("RGBA", self.im.size, (color_cheek[0], color_cheek[1], color_cheek[2], 0))
        bg_draw = ImageDraw.Draw(bg)

        for posX,posY in self.posCheeks:
            bbox =  (posX - radius/2, posY - radius/2, posX + radius/2, posY + radius/2)
            bg_draw.ellipse(bbox, fill=color_cheek)

        bg = bg.filter(ImageFilter.GaussianBlur(radius = width_outline_cheek))
        self.im.alpha_composite(bg)
        
        new_im = Image.new("RGBA", self.im.size, "#0000")
        new_im.paste(self.im, mask=mask)
        self.im = new_im

        self.im.paste(self.imh, mask=self.imh)

        if debug:
            eX, eY = .05*self.x, .05*self.y
            bbox =  (self.posMouth[0] - eX/2, self.posMouth[1] - eY/2, self.posMouth[0] + eX/2, self.posMouth[1] + eY/2)
            self.draw.ellipse(bbox, fill="#00f")
            eX, eY = .05*self.x, .05*self.y
            bbox =  (self.posNose[0] - eX/2, self.posNose[1] - eY/2, self.posNose[0] + eX/2, self.posNose[1] + eY/2)
            self.draw.ellipse(bbox, fill="#00f")

        return self.im
