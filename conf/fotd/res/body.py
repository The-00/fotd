from PIL import Image, ImageDraw

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


class Body:
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
                            (self.x*(17/24 - self.data["eye"]["right"]["position"]["y"]/40),
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
        self.draw.ellipse(self.shapeBody[0], fill="#f00" if debug else self.data["body"]["color"])
        self.draw.rectangle((0,(self.shapeBody[1][1]+self.shapeBody[1][3])/2,self.x,self.y), fill="#0000")
        self.draw.ellipse(self.shapeBody[1], fill="#f00" if debug else self.data["body"]["color"])

        # eyes
        for posX,posY in self.posEyes:
            bbox =  (posX - self.shapeEyes[0]/2, posY - self.shapeEyes[1]/2, posX + self.shapeEyes[0]/2, posY + self.shapeEyes[1]/2)
            self.draw.ellipse(bbox, fill="#0f0" if debug else self.data["body"]["color"])

        # cheeks
        radius = self.x *(1/10 - self.data["cheeks"]["radius"]/20)
        color_cheek = self.data["cheeks"]["color"]

        for posX,posY in self.posCheeks:
            bbox =  (posX - radius/2, posY - radius/2, posX + radius/2, posY + radius/2)
            self.draw.ellipse(bbox, fill=color_cheek)

        if debug:
            eX, eY = .05*self.x, .05*self.y
            bbox =  (self.posMouth[0] - eX/2, self.posMouth[1] - eY/2, self.posMouth[0] + eX/2, self.posMouth[1] + eY/2)
            self.draw.ellipse(bbox, fill="#00f")
            eX, eY = .05*self.x, .05*self.y
            bbox =  (self.posNose[0] - eX/2, self.posNose[1] - eY/2, self.posNose[0] + eX/2, self.posNose[1] + eY/2)
            self.draw.ellipse(bbox, fill="#00f")

        return self.im
