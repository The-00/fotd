from PIL import Image, ImageDraw

'''
data is a dictionnary :
    hat.model
    hat.rotation
'''

class Hat():
    ''' pick a hat un hats/* '''
    def __init__(self, size, data):
        self.data = data
        self.size = int(size)
        self.f = self.data["hat"]["model"]
        self.rotation = self.data["hat"]["rotation"]*5

    def get(self):
        self.im = Image.open(self.f)
        self.im = self.im.resize( (self.size,self.size) )
        self.im = self.im.rotate( self.rotation, Image.NEAREST, expand = 1 )

        self.im2 = Image.new("RGBA", self.im.size, "#0000")
        self.im2.paste(self.im, (int(-self.rotation/150 * self.size),0))
        
        return self.im2