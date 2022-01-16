from PIL import Image, ImageDraw, ImageFilter
from res.body import Body
from res.hat import Hat
from res.eyes import Eyes
from res.mouth import Mouth
from res.nose import Nose
import random as rd
import time
import glob


'''
data is a dictionnary :
    eye.shape.width
    eye.shape.height
    eye.right.model
    eye.right.position.x
    eye.right.position.y
    eye.right.color.front
    eye.righ.color.back
    eye.left.model
    eye.left.position.x
    eye.left.position.y
    eye.left.color.front
    eye.left.color.back

    mouth.position.x
    mouth.position.y
    mouth.model
    mouth.ratio

    nose.position.x
    nose.position.y
    nose.color
    nose.model

    cheeks.color
    cheeks.radius
    cheeks.right.position.x
    cheeks.right.position.y
    cheeks.left.position.x
    cheeks.left.position.y

    hat.position.x
    hat.position.y
    hat.model
    hat.rotation

    body.shape.height
    body.shape.width
    body.color
    body.outline_color
'''


class Frog():
    '''
        Generate the full frog
    '''

    def __init__(self, size=1000, seed=None, data=None):
        self.size = size
        self.data = data

        if self.data == None:
            self.data = self.generate_data( seed )

        self.shape = Body(size, data=self.data)
        self.eyes = Eyes(self.shape.shapeEyes[2], data=self.data)
        self.nose = Nose(size, data=self.data)
        self.mouth = Mouth(size, data=self.data)
        self.hat = Hat(size, data=self.data)

    def rd(self):
        return (rd.random() * 2) -1
    
    def rd_color(self, around, force):
        return tuple([min(255, max(0, around+rd.randint(0,force)-force//2)) for _ in range(3)])

    def generate_data(self, seed=None):
        if seed == None:
            seed = time.time()
        rd.seed( seed )
        
        ge = [">>","<<","oo","OO","..","--","xx","♥♥","  ", "><", "-o", "o-","♥-","-♥", "oO", "Oo", ".o", "o." ,".O", "O.", "o<", ">o", "O<", ">O", "-O", "O-", ".-", "-.", "x.", "xo", "xO", "Ox", "ox", ".x"]
        eyes = rd.choice( ge )
        eye_color_front = self.rd_color(255//3, 100)
        eye_color_back = self.rd_color(4* 255//5, 30)
        nose_color = self.rd_color(255//2, 255)
        body_color = self.rd_color(255//2, 255)
        body_outline_color = self.rd_color(255//2, 255)
        cheeks_color = tuple( [ min(255 ,max(0 ,x+rd.randint(-20, 20))) for x in body_color ] )
        
        data = {
            "eye":{
                "left":{
                    "position": {
                        "x":self.rd(),
                        "y":self.rd()
                    },
                    "model":eyes[0],
                    "color":{
                        "front":eye_color_front,
                        "back":eye_color_back
                    }
                },
                "right":{
                    "position": {
                        "x":self.rd(),
                        "y":self.rd()
                    },
                    "model":eyes[1],
                    "color":{
                        "front":eye_color_front,
                        "back":eye_color_back
                    }
                },
                "shape": {
                    "width":self.rd(),
                    "height":self.rd()
                    }
            },
            "mouth":{
                "position":{
                    "x":self.rd(),
                    "y":self.rd()
                },
                "model":rd.choice( glob.glob("res/mouths/*.png") ),
                "ratio":self.rd()
            },
            "nose":{
                "position":{
                    "x":self.rd(),
                    "y":self.rd()
                },
                "model":rd.choice(["blush", "small"]),
                "color":nose_color
            },
            "cheeks":{
                "left":{
                    "position": {
                        "x":self.rd(),
                        "y":self.rd()
                    },
                },
                "right":{
                    "position": {
                        "x":self.rd(),
                        "y":self.rd()
                    },
                },
                "radius":self.rd(),
                "color":cheeks_color
            },
            "hat":{
                "position":{
                    "x":self.rd(),
                    "y":self.rd()
                },
                "model":rd.choice( glob.glob("res/hats/*.png") ),
                "rotation":self.rd()
            },
            "body":{
                "shape":{
                    "height":self.rd(),
                    "width":self.rd()
                },
                "color":body_color,
                "outline_color":body_outline_color
            }
        }
        
        return data


    def get(self, returnsize):
        im = self.shape.get(debug=False)

        leim, reim = self.eyes.get()
        noseim = self.nose.get()
        mouthim = self.mouth.get()
        hatim = self.hat.get()

        lePos = tuple(map(lambda x: int(x-self.shape.shapeEyes[2]/2),self.shape.posEyes[0]))
        rePos = tuple(map(lambda x: int(x-self.shape.shapeEyes[2]/2),self.shape.posEyes[1]))

        nPos = ( int(self.shape.posNose[0]-noseim.size[0]/2), int(self.shape.posNose[1]-noseim.size[1]/2) )
        mPos = ( int(self.shape.posMouth[0]-mouthim.size[0]/2), int(self.shape.posMouth[1]-mouthim.size[1]/2) )
        hPos = ( int(self.shape.posHat[0]-hatim.size[0]/2), int(self.shape.posHat[1]-hatim.size[1]/2) )

        im.paste(leim,    lePos,  leim)
        im.paste(reim,    rePos,  reim)
        im.paste(noseim,  nPos,   noseim)
        im.paste(mouthim, mPos,   mouthim)
        im.paste(hatim,   hPos,   hatim)


#outline
        # black = Image.new("RGB", im.size, (0, 0, 0))
        black = Image.new("RGBA", im.size, tuple( [x for x in self.data['body']['outline_color']] + [200]))
        bg = Image.new("RGBA", im.size, (255, 255, 255, 0))

        bg.paste(black, mask=im.split()[3])
        bg = im.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.GaussianBlur(radius = 3))

        for _ in range(7):
            bg.paste(black, mask=bg.split()[3])

        bg.paste(im, mask=im)

        return bg.resize((returnsize,returnsize))


