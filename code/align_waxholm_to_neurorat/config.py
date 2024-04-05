import os

if os.sys.platform == "darwin":
    antsExeDir = "/Users/lloyd/Code/builds/ants/bin"
    suffix = ""
else:
    antsExeDir = r"F:\Data\Registration\ants\build\bin\Release"
    antsExeDir = r"F:\pack\ANTs-2.3.1\build\bin\RelWithDebInfo"
    antsExeDir = r"F:\pack\ANTS-master\build\ANTS-build\Examples\Release"
    elastixExeDir = r"F:\Data\Registration\elastix_windows64_v4.8"
    suffix = ".exe"

antsRegistrationCommand = os.path.join(antsExeDir, "antsRegistration" + suffix)
antsTransformCommand = os.path.join(antsExeDir, "antsApplyTransforms" + suffix)
antsJacobianCommand = os.path.join(antsExeDir, "CreateJabianDeterminantImage" + suffix)
antsSimilarityCommand = os.path.join(antsExeDir, "MeasureImageSimilarity" + suffix)
antsOverlapCommand = os.path.join(antsExeDir, "LabelOverlapMeasures" + suffix)
antsImageMath = os.path.join(antsExeDir, "ImageMath" + suffix)
antsN4BiasCorrect = os.path.join(antsExeDir, "N4BiasFieldCorrection" + suffix)

elastixRegistrationCommand = os.path.join(elastixExeDir, "elastix" + suffix)
elastixTransformCommand = os.path.join(elastixExeDir, "transformix" + suffix)
