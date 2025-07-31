from PIL import Image
from api.res.models import MouthModel
import glob

class Mouth():
    ''' pick a mouth un mouths/* '''
    def __init__(self, size:int, data: MouthModel):
        self.data = data
        self.size = size

    def get(self):
        self.f = sorted(glob.glob('./api/res/mouths/*.png'))[ self.data.model_number % len(glob.glob('./api/res/mouths/*.png')) ]
        self.im = Image.open(self.f)
        
        self.im = self.im.resize( (int(self.size * self.data.ratio),int(self.size * self.data.ratio)) )
        self.im = self.im.rotate( self.data.rotation, Image.Resampling.NEAREST, expand = 1 )
        if self.data.flip: self.im = self.im.transpose( method=Image.Transpose.FLIP_LEFT_RIGHT )

        return self.im