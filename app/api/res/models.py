from pydantic import BaseModel, Field, Json, model_validator, ValidationError, TypeAdapter
from enum import Enum
from pydantic.color import Color
from typing import Union, get_origin
import glob
import json
from api.lib.models import recursive_model_validate, cast_model

from pydantic.json_schema import JsonSchemaValue

class RGBColor(Color):
    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler) -> JsonSchemaValue:
        return {
            "type": "string",
            "pattern": "^#?[0-9A-Fa-f]{6}|[a-z]+$",
            "description": "RGB hex color string (#RRGGBB) or color name"
        }

# definition
class PartModel(BaseModel):
    ratio:        float | None = Field(description='increment or decrement in size', gt=0, default=None, examples=[1])
    rotation:     float | None = Field(description='rotation in degrees', ge=-180, le=180, default=None, examples=[0])
    flip:         bool  | None = Field(description='is the part fipped', default=None, examples=[False])
    stroke_width: float | None = Field(description='stroke in percent of size', ge=0, le=1, default=None, examples=[1/100])

class PartPosition(BaseModel):
    x: float = Field(description="horizontal position", default=0, examples=[0])
    y: float = Field(description="vertical position", default=0, examples=[0])

class PartShape(BaseModel):
    width:  float = Field(description="width in percent of size", default=0, examples=[0])
    height: float = Field(description="height in percent of size", default=0, examples=[0])

class EyeModelList(Enum):
    pleated_right = ">"
    pleated_left  = "<"
    pleated_up    = "^"
    pleated_down  = "v"
    normal        = "o"
    big           = "O"
    small         = "."
    closed        = "-"
    dead          = "x"
    love          = "♥"
    none          = " "
    moon_right    = ")"
    moon_left     = "("
    moon_down     = "u"
    moon_up       = "n"
    star          = "*"

class NoseModelList(Enum):
    blush    = "blush"
    small    = "small"
    nostril  = "nostril"
    triangle = "triangle"
    none     = "none"


# models
class HatModel(PartModel):
    model_number: int | None = Field(description='model of hat to use', ge=0, le=len(glob.glob('./api/res/hats/*.png')), default=None, examples=[0])

class MouthModel(PartModel):
    model_number: int | None = Field(description='model of mouth to use', ge=0, le=len(glob.glob('./api/res/mouths/*.png')), default=None, examples=[0])

class NoseModel(PartModel):
    model_name: NoseModelList | None = Field(description='model of hat to use', default=None, examples=["none"])
    color:      RGBColor | None      = Field(description='nose color', default=None)

class EyeModel(PartModel):
    model_name:  EyeModelList | None = Field(description='model of eye to use', default=None, examples=['o'])
    pupil_color: RGBColor | None     = Field(description='pupil color', default=None)
    back_color:  RGBColor | None     = Field(description='back of the eye color', default=None)

class GhostArmModel(BaseModel):
    rotation:  float | None = Field(description='rotation in degrees', ge=-180, le=180, default=None, examples=[0])
    length:    float        = Field(description="height in percent of size", default=0.5, examples=[0.5])
    thickness: float        = Field(description="width in percent of size", default=0.5, examples=[0.5])

class FrogCheekModel(BaseModel):
    radius:        float | None    = Field(description='radius of the cheek', ge=0, default=None)
    color:         RGBColor | None = Field(description='color of the cheek', default=None)
    outline_width: float | None    = Field(description='outline width of the cheek', ge=0, default=None)

class CharacterBodyModel(BaseModel):
    left_eye_position:    PartPosition | None = Field(description='position of the left eye', default=None)
    right_eye_position:   PartPosition | None = Field(description='position of the right eye', default=None)
    nose_position:        PartPosition | None = Field(description='position of the nose', default=None)
    mouth_position:       PartPosition | None = Field(description='position of the mouse', default=None)
    hat_position:         PartPosition | None = Field(description='position of the hat', default=None)
    shape:                PartShape | None    = Field(description='shape of the body', default=None)
    color:                RGBColor | None     = Field(description='color of the body', default=None)
    outline_color:        RGBColor | None     = Field(description='color of the outline of the body', default=None)

class FrogBodyModel(CharacterBodyModel):
    left_eye_shape:       PartShape | None      = Field(description='shape of the left eye', default=None)
    right_eye_shape:      PartShape | None      = Field(description='shape of the right eye', default=None)
    belly_shape:          PartShape | None      = Field(description='shape of the belly', default=None)
    belly_color:          RGBColor | None       = Field(description='color of the belly', default=None)
    left_cheek_position:  PartPosition | None   = Field(description='position of the left cheek', default=None)
    right_cheek_position: PartPosition | None   = Field(description='position of the right cheek', default=None)
    left_cheek:           FrogCheekModel | None = Field(description='left cheek', default=None)
    right_cheek:          FrogCheekModel | None = Field(description='right cheek', default=None)

class GhostBodyModel(CharacterBodyModel):
    leaf_number: int | None           = Field(description='number of small leaf at the bottom', ge=1, default=None)
    leaf_space:  float | None         = Field(description='size of gap between leafs', ge=0, default=None)
    left_arm:    GhostArmModel | None = Field(description='description of the left arm', default=None)
    right_arm:   GhostArmModel | None = Field(description='description of the right arm', default=None)

class MushroomBodyModel(CharacterBodyModel):
    mushroom_hat_shape: PartShape | None = Field(description='shape of the mushroom hat', default=None)
    mushroom_hat_color: RGBColor | None  = Field(description='color of the mushroom hat color', default=None)
    left_eye_shape:     PartShape | None = Field(description='shape of the left eye', default=None)
    right_eye_shape:    PartShape | None = Field(description='shape of the right eye', default=None)

class CharacterModel(BaseModel):
    body:        CharacterBodyModel | None = Field(description='the body description', default=None)
    left_eye:    EyeModel | None           = Field(description='the left eye description', default=None)
    right_eye:   EyeModel | None           = Field(description='the right eye description', default=None)
    nose:        NoseModel | None          = Field(description='the nose description', default=None)
    mouth:       MouthModel | None         = Field(description='the mouth description', default=None)
    hat:         HatModel | None           = Field(description='the hat description', default=None)

    def __hash__(self) -> int:
        return self.model_dump_json().__hash__()
    
    @model_validator(mode='before')
    def parse_json(cls, v):
        if isinstance(v, str):
            try:
                vv = json.loads(v)
                return cls.model_validate(vv)
            except json.JSONDecodeError:
                pass
        return v
class FrogModel(CharacterModel):
    body: FrogBodyModel | None = Field(description='the frog body description', default=None)

class GhostModel(CharacterModel):
    body: GhostBodyModel | None = Field(description='the ghost body description', default=None)

class MushroomModel(CharacterModel):
    body: MushroomBodyModel | None = Field(description='the mushroom body description', default=None)

AllCharacterModel = Union[
    FrogModel,
    GhostModel,
    MushroomModel
] | None

class DiffModel(BaseModel):
    @classmethod
    def diff(cls, obj1, obj2):
        data = {}
        for field, field_info in obj1.model_fields.items():
            v1 = getattr(obj1, field)
            v2 = getattr(obj2, field)

            if v1 == v2:
                continue

            # Si c'est un sous-modèle Pydantic → diff récursif
            if isinstance(v1, BaseModel) and isinstance(v2, BaseModel):
                sub_diff = DiffModel.diff(v1, v2)
                if sub_diff:
                    data[field] = sub_diff
                continue

            # Si c'est une liste de modèles
            if isinstance(v1, list) and isinstance(v2, list):
                list_diff = []
                for i in range(min(len(v1), len(v2))):
                    if isinstance(v1[i], BaseModel) and isinstance(v2[i], BaseModel):
                        sub_diff = DiffModel.diff(v1[i], v2[i])
                        if sub_diff:
                            list_diff.append(sub_diff)
                    elif v1[i] != v2[i]:
                        list_diff.append(v2[i])
                if list_diff or len(v1) != len(v2):
                    data[field] = list_diff or v2
                continue

            # Valeur simple différente
            data[field] = v2
        return obj1.__class__(**data)