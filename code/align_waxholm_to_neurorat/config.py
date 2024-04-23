import os

antsExeDir = '/gpfs/bbp.cscs.ch/project/proj85/bin/' # Path to ANTs installation
suffix = ""

antsRegistrationCommand = os.path.join(antsExeDir, "antsRegistration" + suffix)
antsTransformCommand = os.path.join(antsExeDir, "antsApplyTransforms" + suffix)
antsJacobianCommand = os.path.join(antsExeDir, "CreateJabianDeterminantImage" + suffix)
antsSimilarityCommand = os.path.join(antsExeDir, "MeasureImageSimilarity" + suffix)
antsOverlapCommand = os.path.join(antsExeDir, "LabelOverlapMeasures" + suffix)
antsImageMath = os.path.join(antsExeDir, "ImageMath" + suffix)
antsN4BiasCorrect = os.path.join(antsExeDir, "N4BiasFieldCorrection" + suffix)

