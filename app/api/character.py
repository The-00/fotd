from PIL import Image, ImageDraw, ImageFilter
from api.res.body import FrogBody
from api.res.hat import Hat
from api.res.eyes import Eye
from api.res.mouth import Mouth
from api.res.nose import Nose
from numpy import random
import glob
import os
from pydantic import BaseModel
from deepmerge import always_merger
from api.res.models import *

class Character():
    '''
        Generate a character (tooling class)
    '''

    def __init__(self, name=None, size=1000, seed=None, data:CharacterModel=CharacterBaseModel()):
        if type(seed) == str and len(seed) > 0 and seed != "random":
            seed = int("".join([str(ord(c)) for c in seed]))
            self.rdg = random.default_rng( seed % (2**32-1) )
        else:
            self.rdg = random.default_rng()

        self.size = size
        self.input_data = data
        self.name = name
        self.seed = seed

    def rd(self, min=-1, max=1):
        return (self.rdg.random() * (max-min)) + min

    def rd_color(self, around, force):
        return tuple([min(255, max(0, around+self.rdg.integers(0,force)-force//2)) for _ in range(3)])

    def generate(self):
        eyes_pair = [">>","<<","oo","OO","..","--","xx","♥♥","  ","><","-o","o-","♥-","-♥","oO","Oo",".o","o.",".O","O.","o<",">o","O<",">O","-O","O-",
                     ".-","-.","x.","xo","xO","Ox","ox",".x","uu","nn","((","))","^^","vv","**","*<",">*","*♥","♥*","*-","-*",".*","*.","^-","-^"]
        
        body_turn = self.rd()

        eyes_model_name = self.rdg.choice( eyes_pair )
        eyes_stroke_width = self.rd(0.05, 0.15)
        eyes_color_front = self.rd_color(255//3, 100)
        eyes_color_back = self.rd_color(4* 255//5, 30)

        eyes_x, eyes_y= self.rd(-2, 2), self.rd(-2, 2)

        body_color = self.rd_color(255//2, 255)
        body_outline_color = self.rd_color(255//2, 255)
        cheeks_color = tuple( [ min(255 ,max(0 ,x+self.rdg.integers(-40, 40))) for x in body_color ] )
        nose_color = tuple( [ min(255 ,max(0 ,x+self.rdg.integers(30, 60)*self.rdg.choice([-1, 1]))) for x in body_color ] )
        nose_stroke_width = self.rd(0.05, 0.1)

        cheecks_x, cheecks_y = self.rd(), self.rd()
        cheeks_outline_width = self.rd(0, 1)

        mouth = self.rdg.integers(0, len(glob.glob('./api/res/mouths/*.png')))
        hat = self.rdg.integers(0, len(glob.glob('./api/res/hats/*.png')))
        nose = self.rdg.choice(NoseModelList)
 
        seeded_data = CharacterBaseModel(
            body=CharacterBodyModel(
                left_eye_position=PartPosition(x=eyes_x, y=eyes_y),
                right_eye_position=PartPosition(x=-eyes_x, y=eyes_y),
                left_cheek_position=PartPosition(x=cheecks_x, y=cheecks_y),
                right_cheek_position=PartPosition(x=-cheecks_x, y=cheecks_y),
                nose_position=PartPosition(x=0, y=self.rd()),
                mouth_position=PartPosition(x=0, y=self.rd()),
                hat_position=PartPosition(x=self.rd(), y=self.rd()),
                shape=PartShape(width=self.rd(), height=self.rd()),
                color=Color(value=body_color),
                outline_color=Color(value=body_outline_color)
            ),
            left_eye=EyeModel(
                model_name=EyeModelList(eyes_model_name[0]),
                stroke_width=eyes_stroke_width,
                pupil_color=eyes_color_front,
                back_color=eyes_color_back,
                ratio=1,
                rotation=0,
                flip=False,
            ),
            right_eye=EyeModel(
                model_name=EyeModelList(eyes_model_name[1]),
                stroke_width=eyes_stroke_width,
                pupil_color=eyes_color_front,
                back_color=eyes_color_back,
                ratio=1,
                rotation=0,
                flip=False,
            ),
            left_cheek=CheekModel(
                color=cheeks_color,
                outline_width=cheeks_outline_width,
                ratio=1,
                rotation=0,
                flip=False,
                stroke_width=1/100
            ),
            right_cheek=CheekModel(
                color=cheeks_color,
                outline_width=cheeks_outline_width,
                ratio=1,
                rotation=0,
                flip=False,
                stroke_width=1/100
            ),
            mouth=MouthModel(
                model_number=mouth,
                ratio=self.rd(0.7, 1.7),
                rotation=0,
                flip=False,
                stroke_width=1/100
            ),
            nose=NoseModel(
                model_name=nose,
                rotation=self.rd(-5, 5),
                color=Color(nose_color),
                stroke_width=nose_stroke_width,
                ratio=1,
                flip=False,
            ),
            hat=HatModel(
                model_number=hat,
                rotation=self.rd(-10, 10),
                flip=self.rd() < 0,
                ratio=1,
                stroke_width=1/100
            )
        )

        self.data = self._merge_models(primary=self.input_data, secondary=seeded_data)

    def _generate_image(self, part_list, outline_color):
        shape_image = self.shape.get()
        for part in part_list:
            shape_image.alpha_composite(part[0],  part[1])
        return self._apply_outline(shape_image, outline_color)

    def _apply_outline(self, image, outline_color):
        outline_image = Image.new("RGBA", image.size, tuple( [x for x in outline_color] + [200]))
        new_image = Image.new("RGBA", image.size, (255, 255, 255, 0))
        new_image.paste(outline_image, mask=image.split()[3])
        new_image = image.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.GaussianBlur(radius = image.size[0]//150))
        for _ in range(7):
            new_image.paste(outline_image, mask=new_image.split()[3])
        new_image.paste(image, mask=image)
        return new_image

    def _merge_dictionaries(self, dict1, dict2):
        """
        Recursive merge dictionaries.

        :param dict1: Base dictionary to merge.
        :param dict2: Dictionary to merge on top of base dictionary.
        :return: Merged dictionary
        """
        for key, val in dict1.items():
            if isinstance(val, dict):
                dict2_node = dict2.setdefault(key, {})
                self._merge_dictionaries(val, dict2_node)
            else:
                if key not in dict2:
                    dict2[key] = val
        return dict2

    def _merge_models(self, primary, secondary):
        primary_data = primary.model_dump(exclude_unset=True, exclude_none=True)
        secondary_data = secondary.model_dump(exclude_unset=True, exclude_none=True)

        # print("-----------------------------------")
        # print(primary_data)
        # print(secondary_data)
        # print("-----------------------------------")
        merged_data = always_merger.merge(secondary_data, primary_data)
        return primary.model_validate(merged_data)