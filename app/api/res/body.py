from PIL import Image, ImageDraw, ImageFilter

'''
data is a dictionnary:
    eye["left"]["position"]["x"]
    eye["left"]["position"]["y"]
    eye["right"]["position"]["x"]
    eye["right"]["position"]["y"]
    eye["shape"]["width"]
    eye["shape"]["height"]
    mouth["position"]["x"]
    mouth["position"]["y"]
    nose["position"]["x"]
    nose["position"]["y"]
    cheeks["color"]
    cheeks["radius"]
    cheeks["right"]["position"]["x"]
    cheeks["right"]["position"]["y"]
    cheeks["left"]["position"]["x"]
    cheeks["left"]["position"]["y"]
    hat["position"]["x"]
    hat["position"]["y"]
    body["shape"]["height"]
    body["shape"]["width"]
    body["color"]
'''


class FrogBody:
    '''
        generate a shape with the position of other elements
    '''
    def __init__(self, size, data):
        self.data = data
        self.im = Image.new("RGBA", (size,size), "#0000")
        self.draw = ImageDraw.Draw(self.im)
        self.x, self.y = self.im.size


        self.posEyes   = [
                            (self.x*(7/24 + self.data["eye"]["left"]["position"]["x"]/40),
                             self.y*(10/24 + self.data["eye"]["left"]["position"]["y"]/60)
                            ),
                            (self.x*(17/24 - self.data["eye"]["right"]["position"]["x"]/40),
                             self.y*(10/24 + self.data["eye"]["right"]["position"]["y"]/60)
                            )
                        ]
        self.shapeEyes = [
                            self.x*(.17 + self.data["eye"]["shape"]["width"]/50),
                            self.y*(.17 + self.data["eye"]["shape"]["height"]/50),
                            self.x*(.17 + min(self.data["eye"]["shape"]["width"], self.data["eye"]["shape"]["height"])/50)
                        ]
        self.posMouth = [
                            self.x*(1/2 + self.data["mouth"]["position"]["x"]/40),
                            self.y*(1/2 + self.data["mouth"]["position"]["y"]/20)
                        ]
        self.posNose = [
                            self.x*(1/2   + self.data["nose"]["position"]["x"]/40),
                            self.y*(19/48 + self.data["nose"]["position"]["y"]/50)
                        ]
        self.posCheeks = [
                            (self.x*(1/3 + self.data["cheeks"]["right"]["position"]["x"]/30),
                             self.y*(1/2 + self.data["cheeks"]["right"]["position"]["y"]/20)
                            ),
                            (self.x*(2/3 + self.data["cheeks"]["left"]["position"]["x"]/30),
                             self.y*(1/2 + self.data["cheeks"]["left"]["position"]["y"]/20)
                            )
                        ]
        self.posHat = [
                            self.x*(1/2 + self.data["hat"]["position"]["x"]/20),
                            self.y*(1/3 + self.data["hat"]["position"]["y"]/40)
                        ]
        self.shapeBody = [
                            (self.x*(1/6 + self.data["body"]["shape"]["width"]/20),
                             self.y*(1/3 + self.data["body"]["shape"]["height"]/20),
                             self.x*(5/6 - self.data["body"]["shape"]["width"]/20),
                             self.y
                            ),
                            (self.x*(1/6 + self.data["body"]["shape"]["width"]/20),
                             self.y*4/6 - self.y/10,
                             self.x*(5/6 - self.data["body"]["shape"]["width"]/20),
                             self.y*4/6 + self.y/10
                            )
                        ]

    def get(self, debug=False):

        # body shape generation
        self.draw.ellipse(self.shapeBody[0], fill="#f00" if debug else tuple(self.data["body"]["color"]))
        self.draw.rectangle((0,(self.shapeBody[1][1]+self.shapeBody[1][3])/2,self.x,self.y), fill="#0000")
        self.draw.ellipse(self.shapeBody[1], fill="#f00" if debug else tuple(self.data["body"]["color"]))

        # eyes
        for posX,posY in self.posEyes:
            bbox =  (posX - self.shapeEyes[0]/2, posY - self.shapeEyes[1]/2, posX + self.shapeEyes[0]/2, posY + self.shapeEyes[1]/2)
            self.draw.ellipse(bbox, fill="#0f0" if debug else tuple(self.data["body"]["color"]))

        mask = self.im.copy()
        
        # cheeks
        radius = self.x *(1/10 - self.data["cheeks"]["radius"]/20)
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

        if debug:
            eX, eY = .05*self.x, .05*self.y
            bbox =  (self.posMouth[0] - eX/2, self.posMouth[1] - eY/2, self.posMouth[0] + eX/2, self.posMouth[1] + eY/2)
            self.draw.ellipse(bbox, fill="#00f")
            eX, eY = .05*self.x, .05*self.y
            bbox =  (self.posNose[0] - eX/2, self.posNose[1] - eY/2, self.posNose[0] + eX/2, self.posNose[1] + eY/2)
            self.draw.ellipse(bbox, fill="#00f")

        return self.im


class GhostBody:
    '''
        generate a shape with the position of other elements
    '''
    def __init__(self, size, data):
        self.data = data
        self.im = Image.new("RGBA", (size,size), "#0000")
        self.draw = ImageDraw.Draw(self.im)
        self.x, self.y = self.im.size
        self.dy = 100


        self.posEyes   = [
                            (self.x*(4/10 + self.data["eye"]["left"]["position"]["x"]/60),
                             self.dy + self.y*(3/10 + self.data["eye"]["left"]["position"]["y"]/60)
                            ),
                            (self.x*(6/10 - self.data["eye"]["right"]["position"]["x"]/60),
                             self.dy + self.y*(3/10 + self.data["eye"]["right"]["position"]["y"]/60)
                            )
                        ]
        self.shapeEyes = [
                            self.x*(.1 + self.data["eye"]["shape"]["width"]/50),
                            self.dy + self.y*(.1 + self.data["eye"]["shape"]["height"]/50),
                            self.x*(.1 + min(self.data["eye"]["shape"]["width"], self.data["eye"]["shape"]["height"])/50)
                        ]
        self.posMouth = [
                            self.x*(1/2 + self.data["mouth"]["position"]["x"]/40),
                            self.dy + self.y*(1/3 + self.data["mouth"]["position"]["y"]/20)
                        ]
        self.posNose = [
                            self.x*(1/2   + self.data["nose"]["position"]["x"]/40),
                            self.dy + self.y*(15/48 + self.data["nose"]["position"]["y"]/50)
                        ]
        self.posCheeks = [
                            (self.x*(1/3 + self.data["cheeks"]["right"]["position"]["x"]/30),
                             self.dy + self.y*(1/3 + self.data["cheeks"]["right"]["position"]["y"]/20)
                            ),
                            (self.x*(2/3 + self.data["cheeks"]["left"]["position"]["x"]/30),
                             self.dy + self.y*(1/3 + self.data["cheeks"]["left"]["position"]["y"]/20)
                            )
                        ]
        self.posHat = [
                            self.x*(1/2 + self.data["hat"]["position"]["x"]/40),
                            self.dy + self.y*(4/20 + self.data["hat"]["position"]["y"]/80)
                        ]
        self.shapeBody = [
                            (self.x*(5/20 + self.data["body"]["shape"]["width"]/20),
                             self.dy + self.y*(4/20 + self.data["body"]["shape"]["height"]/20),
                             self.x*(15/20 - self.data["body"]["shape"]["width"]/20),
                             self.dy + self.y*1.2
                            )
                        ]
        self.numberBottom = round( (self.data["special"][0]+1)/2 * 10 ) + 5
        self.spaceBottom = round( self.data["special"][0] * self.numberBottom )
        

    def get(self, debug=False):

        # body shape generation
        self.draw.ellipse(self.shapeBody[0], fill="#f00" if debug else tuple(self.data["body"]["color"]))
        self.draw.rectangle((0,((self.shapeBody[0][3] - self.shapeBody[0][1]) / 2 + self.shapeBody[0][1]),self.x,self.dy + self.y), fill="#0000")
#        self.draw.ellipse(self.shapeBody[1], fill="#f00" if debug else tuple(self.data["body"]["color"]))

        # arms
        ll, lw, = round( (self.data["body"]["arms"]["left"]["length"] /20 +.3) * self.x), round( (self.data["body"]["arms"]["left"]["width"] /50 +.05) * self.x )
        rl, rw, = round( (self.data["body"]["arms"]["right"]["length"]/20 +.3) * self.x), round( (self.data["body"]["arms"]["right"]["width"]/50 +.05) * self.x ),
        d = self.shapeBody[0][0] * .2
        lx, rx = round(self.shapeBody[0][0]-lw-d), round(self.shapeBody[0][2]+rw+d)
        y = round( self.dy + self.y*4/10 )

        left_arm_im = Image.new("RGBA", (ll, lw), "#0000")
        left_arm_draw = ImageDraw.Draw(left_arm_im)
        left_arm_draw.ellipse((0, 0, ll, lw), fill="#f00" if debug else tuple(self.data["body"]["color"]))
        left_arm_im = left_arm_im.rotate( self.data["body"]["arms"]["left"]["angle"], expand=True)
        
        right_arm_im = Image.new("RGBA", (rl, rw), "#0000")
        right_arm_draw = ImageDraw.Draw(right_arm_im)
        right_arm_draw.ellipse((0, 0, rl, rw), fill="#f00" if debug else tuple(self.data["body"]["color"]))
        right_arm_im = right_arm_im.rotate(self.data["body"]["arms"]["right"]["angle"], expand=True)

        self.im.paste(left_arm_im, (lx, y), mask=left_arm_im)
        self.im.paste(right_arm_im, (rx - right_arm_im.size[0], y), mask=right_arm_im)

        # bottom
        w = self.shapeBody[0][2] - self.shapeBody[0][0] + self.spaceBottom
        n = self.numberBottom
        r = w / (2*n) - self.spaceBottom/2
        x0 = self.shapeBody[0][0]
        y = (self.shapeBody[0][3] - self.shapeBody[0][1]) / 2 + self.shapeBody[0][1]

        for i in range(n):
            x = x0 + 2*i*(r+self.spaceBottom/2) + r
            bbox = (x-r, y-r, x+r, y+r)
            self.draw.ellipse(bbox, fill="#f00" if debug else tuple(self.data["body"]["color"]))

        mask = self.im.copy()
        
        # cheeks
        radius = self.x *(1/10 - self.data["cheeks"]["radius"]/20)
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

        if debug:
            eX, eY = .05*self.x, .05*self.y
            bbox =  (self.posMouth[0] - eX/2, self.posMouth[1] - eY/2, self.posMouth[0] + eX/2, self.posMouth[1] + eY/2)
            self.draw.ellipse(bbox, fill="#00f")
            eX, eY = .05*self.x, .05*self.y
            bbox =  (self.posNose[0] - eX/2, self.posNose[1] - eY/2, self.posNose[0] + eX/2, self.posNose[1] + eY/2)
            self.draw.ellipse(bbox, fill="#00f")

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
