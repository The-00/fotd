# fotd
FrogOfThDay Website

# HOW TO USE

```
git clone https://github.com/The-00/fotd
cd fotd
docker build . -t fotd
docker run -p 8080:8080 fotd
```
# quick documentation

can be find in `localhost:8080/help`

# custom api

You can use this json to create your own frog (missing values will be set random). To ask for a frog : you will have to base64 the json and use it on `/custom/<base64>` 

Values indication : 
```
[-1,1]     : real value value in range [-1,1]    (ex: 0.3)
["a","b"]  : choose between "a" or "b"           (ex: "a")
(r,g,b)    : color in RGB format                 (ex: [200,10,45])
file(type) : file among /fotd/res/[type]/*.png   (ex: "/fotd/res/mouths/bouche1.png")
```

```
{
    "eye":{
        "left":{
            "position": {
                "x":[-3,3],
                "y":[-1,1]
            },
            "model":[">","<","o","O",".","-","x","♥"," "],
            "color":{
                "front":(r,g,b),
                "back":(r,g,b)
            }
        },
        "right":{
            "position": {
                "x":[-3,3],
                "y":[-1,1]
            },
            "model":[">","<","o","O",".","-","x","♥"," "],
            "color":{
                "front":(r,g,b),
                "back":(r,g,b)
            }
        },
        "shape": {
            "width":[-1.5,1.5],
            "height":[-1,1]
            }
    },
    "mouth":{
        "position":{
            "x":[-1.5,1.5],
            "y":[-1,1]
        },
        "model":file(mouths),
        "ratio":[-1/3,1/3]
    },
    "nose":{
        "position":{
            "x":[-1.5,1.5],
            "y":[-1,1]
        },
        "model":["blush", "small"],
        "color":(r,g,b)
    },
    "cheeks":{
        "left":{
            "position": {
                "x":[-1,1],
                "y":[-1,1]
            },
        },
        "right":{
            "position": {
                "x":[-1,1],
                "y":[-1,1]
            },
        },
        "radius":[-1,1],
        "color":(r,g,b)
    },
    "hat":{
        "position":{
            "x":[-1,1],
            "y":[-1,1]
        },
        "model":file(hats),
        "rotation":[-1,1]
    },
    "body":{
        "shape":{
            "height":[-1,1],
            "width":[-1,1]
        },
        "color":(r,g,b),
        "outline_color":(r,g,b)
    }
}
```

exemple
```
json : {"eye":{"left":{"model":"♥"},"right":{"model":"♥"},"shape":{"width":1.5,"height":1}},"nose":{"model":"small"},"cheeks":{"color":[100,0,0]},"body":{"shape":{"height":1,"width":1},"outline_color":[200,200,0]}}

base64 : eyJleWUiOnsibGVmdCI6eyJtb2RlbCI6IuKZpSJ9LCJyaWdodCI6eyJtb2RlbCI6IuKZpSJ9LCJzaGFwZSI6eyJ3aWR0aCI6MS41LCJoZWlnaHQiOjF9fSwibm9zZSI6eyJtb2RlbCI6InNtYWxsIn0sImNoZWVrcyI6eyJjb2xvciI6WzEwMCwwLDBdfSwiYm9keSI6eyJzaGFwZSI6eyJoZWlnaHQiOjEsIndpZHRoIjoxfSwib3V0bGluZV9jb2xvciI6WzIwMCwyMDAsMF19fQo=

request : localhost:8080/custom/eyJleWUiOnsibGVmdCI6eyJtb2RlbCI6IuKZpSJ9LCJyaWdodCI6eyJtb2RlbCI6IuKZpSJ9LCJzaGFwZSI6eyJ3aWR0aCI6MS41LCJoZWlnaHQiOjF9fSwibm9zZSI6eyJtb2RlbCI6InNtYWxsIn0sImNoZWVrcyI6eyJjb2xvciI6WzEwMCwwLDBdfSwiYm9keSI6eyJzaGFwZSI6eyJoZWlnaHQiOjEsIndpZHRoIjoxfSwib3V0bGluZV9jb2xvciI6WzIwMCwyMDAsMF19fQo=
```