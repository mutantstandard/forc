

# A static data structure that contains all of the formats that
# forc can export to, what their names and what their properties are.



formats = {"SVGinOT":
             {"name": "SVGinOT"
             ,"imageFormat": "svg"
             ,"imageTables": "SVG"
             ,"ligatureFormat": "OpenType"
             ,"extension": ".otf"
             ,"iOSCompile": False
             }
         ,"sbixTT":
              {"name": "sbixTT"
              ,"imageFormat": "png"
              ,"imageTables": "sbix"
              ,"ligatureFormat": "TrueType"
              ,"extension": ".otf"
              ,"iOSCompile": False
              }
         ,"sbixOT":
              {"name": "sbixOT"
              ,"imageFormat": "png"
              ,"imageTables": "sbix"
              ,"ligatureFormat": "OpenType"
              ,"extension": ".ttf"
              ,"iOSCompile": False
              }
         ,"sbixTTiOS":
              {"name": "sbixTTiOS"
              ,"imageFormat": "png"
              ,"imageTables": "sbix"
              ,"ligatureFormat": "TrueType"
              ,"extension": ".ttf"
              ,"iOSCompile": True
              }
        ,"sbixOTiOS":
             {"name": "sbixOTiOS"
             ,"imageFormat": "png"
             ,"imageTables": "sbix"
             ,"ligatureFormat": "OpenType"
             ,"extension": ".ttf"
             ,"iOSCompile": True
             }
        ,"CBx":
             {"name": "CBx"
             ,"imageFormat": "png"
             ,"imageTables": "CBx"
             ,"ligatureFormat": "OpenType"
             ,"extension": ".ttf"
             ,"iOSCompile": False
             }
         }


compilers = ["ttx", "forc"]
