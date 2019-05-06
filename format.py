

# A static data structure that contains all of the formats that
# forc can export to, what their names and what their properties are.



formats = {"SVGinOT":
             {"imageFormat": "svg"
             ,"imageTables": "SVG"
             ,"ligatureFormat": "OpenType"
             ,"extension": ".otf"
             ,"iOSCompile": False
             }
         ,"sbixTT":
              {"imageFormat": "png"
              ,"imageTables": "sbix"
              ,"ligatureFormat": "TrueType"
              ,"extension": ".otf"
              ,"iOSCompile": False
              }
         ,"sbixOT":
              {"imageFormat": "png"
              ,"imageTables": "sbix"
              ,"ligatureFormat": "OpenType"
              ,"extension": ".ttf"
              ,"iOSCompile": False
              }
         ,"sbixTTiOS":
              {"imageFormat": "png"
              ,"imageTables": "sbix"
              ,"ligatureFormat": "TrueType"
              ,"extension": ".ttf"
              ,"iOSCompile": True
              }
        ,"sbixOTiOS":
             {"imageFormat": "png"
             ,"imageTables": "sbix"
             ,"ligatureFormat": "OpenType"
             ,"extension": ".ttf"
             ,"iOSCompile": True
             }
        ,"CBx":
             {"imageFormat": "png"
             ,"imageTables": "CBx"
             ,"ligatureFormat": "OpenType"
             ,"extension": ".ttf"
             ,"iOSCompile": False
             }
         }
