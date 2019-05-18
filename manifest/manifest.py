from manifest.metrics import checkTransformMetrics
from manifest.encoding import checkTransformEncoding
from manifest.metadata import checkTransformMetadata

checkDocMsg = "Check the documentation to make sure you're doing the manifest right'."



def checkTransformManifest(outputFormats, m):
    """
    Validates manifest data, both at a structural and value level.
    Will compile some manifest data into a structure for use in font table assembly.

    Will raise a ValueError if anything critically incorrect has been entered by the user.
    """

    if 'metrics' not in m:
        raise ValueError(f"No metrics data found in the manifest. {checkDocMsg}")
    if 'encoding' not in m:
        raise ValueError(f"No encoding data found in the manifest. {checkDocMsg}")
    if 'metadata' not in m:
        raise ValueError(f"No metadata data found in the manifest. {checkDocMsg}")

    checkTransformMetrics(m['metrics'])
    checkTransformEncoding(m['encoding'])
    checkTransformMetadata(m['metadata'], outputFormats)
