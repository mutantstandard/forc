


reqMetricNames =  [ "unitsPerEm"
                  , "lowestRecPPEM"

                  , "width"
                  , "height"

                  , "xMin"
                  , "xMax"
                  , "yMin"
                  , "yMax"

                  , "horiAscent"
                  , "horiDescent"
                  , "vertAscent"
                  , "vertDescent"

                  , "spaceHLength"
                  , "spaceVLength"
                  , "normalWidth"
                  , "normalLSB"
                  , "normalHeight"
                  , "normalTSB"

                  , "OS2ySubscriptXSize"
                  , "OS2ySubscriptYSize"

                  , "OS2ySubscriptXOffset"
                  , "OS2ySubscriptYOffset"

                  , "OS2ySuperscriptXSize"
                  , "OS2ySuperscriptYSize"

                  , "OS2ySuperscriptXOffset"
                  , "OS2ySuperscriptYOffset"

                  , "OS2yStrikeoutSize"
                  , "OS2yStrikeoutPosition"
                  ]


def checkTransformMetrics(metrics):

    # METRICS
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------

    # make sure there are no excess unchecked values.
    if not len(metrics) == len(reqMetricNames):
        raise ValueError(f"You have more values than the required values than your metrics. {checkDocMsg}")

    # check for appropriate names.
    for reqName in reqMetricNames:
        if not reqName in metrics:
            raise ValueError(f"metric.{reqName} is missing from your manifest. {checkDocMsg}")

    # make sure all the values are ints.
    for name, value in metrics.items():
        if type(value) is not int:
            raise ValueError(f"metric.{name} is not an int (it's '{value}'). All of your metrics need to be formatted as ints.")
