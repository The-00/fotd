from PIL import Image, ImageDraw

'''
data is a dictionnary :
    mouth.model
    mouth.ratio
'''

class Mouth():
    ''' pick a mouth un mouths/* '''
    def __init__(self, size, data):
        self.data = data
        self.size = int(size * (self.data["mouth"]["ratio"]/2 + 1.5))
        self.f = self.data["mouth"]["model"]

    def get(self):
        self.im = Image.open(self.f)
        self.im = self.im.resize( (self.size,self.size) )
        return self.im