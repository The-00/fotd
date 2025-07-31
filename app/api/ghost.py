from PIL import Image, ImageDraw, ImageFilter
from api.res.body import GhostBody
from api.res.hat import Hat
from api.res.eyes import Eye
from api.res.mouth import Mouth
from api.res.nose import Nose
from numpy import random
import glob
import os
import api.character
from api.res.models import *


class Ghost(api.character.Character):
    '''
        Generate the full ghost
    '''

    def __init__(self, size=1000, seed=None, name=None, data:GhostModel=GhostModel()):
        super().__init__(size=size, data=data, name=name, seed=seed)

        self.generate()

        self.shape     = GhostBody(size=self.size, data=self.data.body)
        self.left_eye  = Eye(size=self.size//10, data=self.data.left_eye)
        self.right_eye = Eye(size=self.size//10, data=self.data.right_eye)
        self.nose      = Nose(size=self.size//10, data=self.data.nose)
        self.mouth     = Mouth(size=self.size//2, data=self.data.mouth)
        self.hat       = Hat(size=self.size, data=self.data.hat)

    def generate(self):
        super().generate()
        arms_rotation = self.rdg.integers(20, 45) if self.rd() > 0 else self.rdg.integers(-45, 10)
        arms_length = self.rd()
        arms_thickness  = self.rd()

        seeded_data = GhostModel(
            body=GhostBodyModel(
                left_arm=GhostArmModel(
                    rotation=arms_rotation,
                    length=arms_length,
                    thickness=arms_thickness
                ),
                right_arm=GhostArmModel(
                    rotation=-arms_rotation,
                    length=arms_length,
                    thickness=arms_thickness
                ),
                leaf_number=self.rdg.integers(5,20),
                leaf_space=self.rd(0,1)
            )
        )

        seeded_data = self._merge_models(primary=seeded_data, secondary=self.data)
        self.data = self._merge_models(primary=self.input_data, secondary=seeded_data)


    def get(self, size=None):
        if not size:
            size = self.size

        body_image      = self.shape.get()
        left_eye_image  = self.left_eye.get()
        right_eye_image = self.right_eye.get()
        nose_image      = self.nose.get()
        mouth_image     = self.mouth.get()
        hat_image       = self.hat.get()

        left_eye_position  = (
            int(self.shape.left_eye_position.x-left_eye_image.width/2),
            int(self.shape.left_eye_position.y-left_eye_image.height/2)
        )
        right_eye_position = (
            int(self.shape.right_eye_position.x-right_eye_image.width/2),
            int(self.shape.right_eye_position.y-right_eye_image.height/2)
        )
        nose_position = (
            int(self.shape.nose_position.x-nose_image.width/2),
            int(self.shape.nose_position.y-nose_image.height/2)
        )
        mouth_position = (
            int(self.shape.mouth_position.x-mouth_image.width/2),
            int(self.shape.mouth_position.y-mouth_image.height/2)
        )
        hat_position = (
            int(self.shape.hat_position.x-hat_image.width/2),
            int(self.shape.hat_position.y-hat_image.height/2)
        )

        body_image = self._generate_image(
            part_list = [
                (left_eye_image,  left_eye_position),
                (right_eye_image, right_eye_position),
                (mouth_image,     mouth_position),
                (nose_image,      nose_position),
                (hat_image,       hat_position)
            ],
            outline_color=self.data.body.color.as_rgb_tuple()
        )

        return body_image.resize((size,size))
