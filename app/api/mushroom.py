from PIL import Image, ImageDraw, ImageFilter
from api.res.body import MushroomBody
from api.res.hat import Hat
from api.res.eyes import Eyes
from api.res.mouth import Mouth
from api.res.nose import Nose
from numpy import random
import glob
import os


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


class Mushroom():
    '''
        Generate the full mushroom
    '''

    def __init__(self, size=1000, seed=None, name=None, data={}):
        self.size = size
        self.data = data
        self.name = name if name else (seed if seed else "random")

        self.rdg = random.default_rng()
        self.data = self.generate_data( self.data, seed )

        self.shape = MushroomBody(size, data=self.data)
        self.eyes = Eyes(self.shape.shapeEyes[2], data=self.data)
        self.nose = Nose(size, data=self.data)
        self.mouth = Mouth(size, data=self.data)
        self.hat = Hat(size, data=self.data)


    def rd(self):
        return (self.rdg.random() * 2) -1

    def rd_color(self, around, force):
        return tuple([min(255, max(0, around+self.rdg.integers(0,force)-force//2)) for _ in range(3)])

    def generate_data(self, data={}, seed=None):
        if type(seed) == str and len(seed) > 0:
            seed = int("".join([str(ord(c)) for c in seed]))
            self.rdg = random.default_rng( seed % (2**32-1) )

        ge = [">>","<<","oo","OO","..","--","xx","♥♥","  ","><","-o","o-","♥-","-♥","oO","Oo",".o","o.",".O","O.","o<",">o","O<",">O","-O","O-",".-",
                "-.", "x.","xo","xO","Ox","ox",".x","uu","nn","((","))","^^","vv","**","*<",">*","*♥", "♥*","*-","-*",".*","*.","^-","-^"]
        eyes = self.rdg.choice( ge )
        eye_color_front = self.rd_color(255//3, 100)
        eye_color_back = self.rd_color(4* 255//5, 30)
        body_color = self.rd_color(255//2, 255)
        body_outline_color = self.rd_color(255//2, 255)
        cheeks_color = tuple( [ min(255 ,max(0 ,x+self.rdg.integers(-40, 40))) for x in body_color ] )
        nose_color = tuple( [ min(255 ,max(0 ,x+self.rdg.integers(30, 60)*self.rdg.choice([-1, 1]))) for x in body_color ] )

        eye_x, eye_y= self.rd(), self.rd()
        cheeck_x, cheeck_y= self.rd(), self.rd()
        turn = self.rd()* 1.5

        mouth = self.rdg.choice( sorted(glob.glob('./api/res/mouths/*.png')) )
        hat = self.rdg.choice( sorted(glob.glob('./api/res/hats/*.png')) )
        nose = self.rdg.choice(["blush", "small", "nostril", "triangle", "none"])
 
        arms_angle = self.rdg.integers(20, 45) if self.rd() > 0 else self.rdg.integers(-45, 10)
        arms_length = self.rd()
        arms_width  = self.rd()

        new_data = {
            "special": [self.rd() for _ in range(20)],
            "eye":{
                "left":{
                    "position": {
                        "x":eye_x,
                        "y":eye_y
                    },
                    "model":eyes[0],
                    "color":{
                        "front":eye_color_front,
                        "back":eye_color_back
                    }
                },
                "right":{
                    "position": {
                        "x":eye_x,
                        "y":eye_y
                    },
                    "model":eyes[1],
                    "color":{
                        "front":eye_color_front,
                        "back":eye_color_back
                    }
                },
                "shape": {
                    "width":self.rd()*1.5,
                    "height":self.rd()
                    }
            },
            "mouth":{
                "position":{
                    "x":turn,
                    "y":self.rd()/3
                },
                "model":mouth,
                "ratio":self.rd() / 5 - 2
            },
            "nose":{
                "position":{
                    "x":turn,
                    "y":self.rd()/3
                },
                "model":nose,
                "rotation":self.rd()/2,
                "color":nose_color
            },
            "cheeks":{
                "left":{
                    "position": {
                        "x":-cheeck_x,
                        "y":cheeck_y
                    },
                },
                "right":{
                    "position": {
                        "x":cheeck_x,
                        "y":cheeck_y
                    },
                },
                "radius":self.rd(),
                "color":cheeks_color,
                "outline_width":(self.rd()+3)*3,
            },
            "hat":{
                "position":{
                    "x":self.rd(),
                    "y":self.rd()
                },
                "model":hat,
                "rotation":self.rd()/4,
                "flip":self.rd() < 0,
            },
            "body":{
                "shape":{
                    "height":self.rd(),
                    "width":self.rd()
                },
                "hat":{
                    "shape":{
                        "height":self.rd()-1,
                        "width":self.rd()
                    },
                    "color": body_color
                },
                "arms":{
                    "left": {
                        "angle": arms_angle,
                        "length": arms_length,
                        "width": arms_width,
                    },
                    "right": {
                        "angle": -arms_angle,
                        "length": arms_length,
                        "width": arms_width,
                    }
                },
                "color":body_color,
                "outline_color":body_outline_color
            }
        }
        
        use_data = new_data
        if data != {}:
            use_data = _merge_dictionaries(new_data,data)

        return use_data


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

        im.paste(noseim,  nPos,   noseim)
        im.paste(leim,    lePos,  leim)
        im.paste(reim,    rePos,  reim)
        #im.paste(mouthim, mPos,   mouthim)
        #im.paste(hatim,   hPos,   hatim)
        
        #im.alpha_composite(leim,    lePos)
        #im.alpha_composite(reim,    rePos)
        #im.alpha_composite(noseim,  nPos)
        im.alpha_composite(mouthim, mPos)
        im.alpha_composite(hatim,   hPos)


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



def _merge_dictionaries(dict1, dict2):
    """
    Recursive merge dictionaries.

    :param dict1: Base dictionary to merge.
    :param dict2: Dictionary to merge on top of base dictionary.
    :return: Merged dictionary
    """
    for key, val in dict1.items():
        if isinstance(val, dict):
            dict2_node = dict2.setdefault(key, {})
            _merge_dictionaries(val, dict2_node)
        else:
            if key not in dict2:
                dict2[key] = val
    return dict2
