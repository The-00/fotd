from PIL import Image
from api.res.models import HatModel
import glob

class Hat():
    ''' pick a hat un hats/* '''
    def __init__(self, size:int, data:HatModel):
        self.data = data
        self.size = size

    def get(self):
        self.f = sorted(glob.glob('./api/res/hats/*.png'))[ self.data.model_number % len(glob.glob('./api/res/hats/*.png')) ]
        self.im = Image.open(self.f)
        
        self.im = self.im.resize( (int(self.size * self.data.ratio), int(self.size * self.data.ratio)) )
        self.im = self.im.rotate( self.data.rotation, Image.Resampling.NEAREST, expand = 1 )
        if self.data.flip: self.im = self.im.transpose( method=Image.Transpose.FLIP_LEFT_RIGHT )

        return self.im