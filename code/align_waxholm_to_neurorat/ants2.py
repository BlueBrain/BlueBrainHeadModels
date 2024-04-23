import os
import subprocess
import tempfile
import config

# some tips: http://www.neuro.polymtl.ca/tips_and_tricks/how_to_use_ants


# transforms:
#  SyN[gradientStep, updateFieldVarianceInVoxelSpace, totalFieldVarianceInVoxelSpace]
#    gradientStep: the higher, the more high frequency deformations (and less stable)
#    updateFieldVarianceInVoxelSpace (default=3) -> the higher, the less high frequency deformations
#
#  BSplineSyN[gradientStep, updateFieldMeshSizeAtBaseLevel, totalFieldMeshSizeAtBaseLevel, <splineOrder=3>]
#    gradientStep: 0.5 -> the smaller, the smaller the distortion
#    totalFieldMeshSizeAtBaseLevel: The larger, the larger the deform
#    splineOrder=3
#
#  GaussianDisplacementField[gradientStep, updateFieldVarianceInVoxelSpace, totalFieldVarianceInVoxelSpace]

# metrics:
#  CC[fixedImage, movingImage, metricWeight, radius, <samplingStrategy={None, Regular, Random}>, <samplingPercentage=[0, 1]>]
#  MI[fixedImage, movingImage, metricWeight, numberOfBins, <samplingStrategy={None, Regular, Random}>, <samplingPercentage=[0, 1]>]

# ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=16


def compute_distance(input, output, foreground_value, working_dir, logfile=None):
    exe = config.antsImageMath
    args = [exe, "3", output, "MaurerDistance", input, "%d" % (foreground_value)]

    if logfile:
        logfile.write(" ".join(args) + "\n")
    prog = subprocess.Popen(args, stdout=logfile, stderr=logfile, cwd=working_dir)
    prog.communicate()
    return True if prog.returncode == 0 else False


def comput_jacobian(
    transform, reference, output, index_displacementfield, logfile=None
):
    exe = config.antsTransformCommand
    working_dir = os.path.dirname(output)
    output_disp = os.path.join(working_dir, "displacementfield.nii.gz")
    args = [
        exe,
        "-d",
        "3",
        "-t",
        transform,
        "-r",
        reference,
        "-o",
        "[%s,%d]" % (output_disp, index_displacementfield),
    ]

    if logfile:
        logfile.write(" ".join(args) + "\n")
    prog = subprocess.Popen(args, stdout=logfile, stderr=logfile, cwd=working_dir)
    prog.communicate()

    if prog.returncode == 0:
        exe = config.antsJacobianCommand
        args = [exe, "3", output_disp, output]

        if logfile:
            logfile.write(" ".join(args) + "\n")
        prog = subprocess.Popen(args, stdout=logfile, stderr=logfile, cwd=working_dir)
        prog.communicate()

    return True if prog.returncode == 0 else False


def n4bias_correct(input, output, shrink_factor=2, working_dir=None, logfile=None):
    exe = config.antsN4BiasCorrect
    args = [exe, "-d", "3", "-s", "%d" % shrink_factor, "-i", input, "-o", output]

    if logfile:
        logfile.write(" ".join(args) + "\n")
    prog = subprocess.Popen(args, stdout=logfile, stderr=logfile, cwd=working_dir)
    prog.communicate()
    return True if prog.returncode == 0 else False


def compute_overlap(source, target, csvFile, working_dir, logfile):
    exe = config.antsOverlapCommand
    args = [exe, "3", source, target, csvFile]

    logfile.write(" ".join(args) + "\n")
    prog = subprocess.Popen(args, stdout=logfile, stderr=logfile, cwd=working_dir)
    prog.communicate()
    return True if prog.returncode == 0 else False


def compute_similarity(source, target, csvFile, working_dir, logfile, metric):
    exe = config.antsSimilarityCommand
    if metric == "CC":
        args = [exe, "3", "1", source, target, csvFile]
    elif metric == "MI":
        args = [exe, "3", "2", source, target, csvFile]

    logfile.write(" ".join(args) + "\n")
    prog = subprocess.Popen(args, stdout=logfile, stderr=logfile, cwd=working_dir)
    prog.communicate()
    return True if prog.returncode == 0 else False


def apply_transform(
    moving, ref, output, transforms, is_labelfield, working_dir, logfile=None
):
    # documentation: http://manpages.org/antsapplytransforms
    exe = config.antsTransformCommand
    # NearestNeighbor
    # GenericLabel
    args = [
        exe,
        "-v",
        "1",
        "-d",
        "3",
        "-e",
        "0",
        "-i",
        moving,
        "-r",
        ref,
        "-o",
        output,
        "--interpolation",
        "NearestNeighbor" if is_labelfield else "BSpline",
    ]

    # allow to pass either list of transforms, or single transform file path
    if isinstance(transforms, str):
        transforms = [transforms]
    for tr in transforms:
        args.extend(["-t", tr])

    if logfile:
        logfile.write(" ".join(args) + "\n")
    prog = subprocess.Popen(args, stdout=logfile, stderr=logfile, cwd=working_dir)
    prog.communicate()
    return True if prog.returncode == 0 else False


class Stage(object):
    def __init__(self):
        self.set_pyramid_options(3, [50, 50, 50], [4, 2, 1], [4, 2, 1])
        self.convergenceThreshold = 1e-6
        self.convergenceWindowSize = 10
        self.metrics = []
        self.fixed_mask = "NULL"
        self.moving_mask = "NULL"

    def set_pyramid_options(self, num_levels, iterations, shrink_factos, sigmas):
        self.number_of_levels = num_levels
        self.iterations = iterations
        self.shrink_factos = shrink_factos
        self.smoothing_sigmas = sigmas

    @property
    def transforms(self):
        return [
            "Rigid",
            "Affine",
            "Similarity",
            "Translation",
            "BSpline",
            "BSplineSyN",
            "SyN",
            "GaussianDisplacementField",
            "BSplineDisplacementField",
        ]

    def set_transform(
        self,
        transform_type="Rigid",
        gradient_step=0.1,
        mesh_size_at_base_level=[5, 5, 5],
        update_field_variance_voxel_space=3,
        total_field_variance_voxel_space=0,
    ):
        """
			gradient_step: 0.5 -> the smaller, the smaller the distortion
			mesh_size_at_base_level: The larger, the larger the deform
		"""
        assert (
            transform_type in self.transforms
        ), "Transform not found in valid transform names"

        self.transform_type = transform_type
        self.gradient_step = gradient_step
        self.mesh_size_at_base_level = mesh_size_at_base_level
        self.update_field_variance_voxel_space = update_field_variance_voxel_space
        self.total_field_variance_voxel_space = total_field_variance_voxel_space

    def set_masks(self, fixed_mask="NULL", moving_mask="NULL"):
        self.fixed_mask = fixed_mask
        self.moving_mask = moving_mask

    def add_metric_MI(
        self,
        moving,
        fixed,
        histogram_bins=32,
        percent=100,
        random=False,
        use_mattes=True,
        weight=1.0,
    ):
        metric = "Mattes" if use_mattes else "MI"
        self.__add_metric(
            metric, moving, fixed, histogram_bins, percent, random, weight
        )

    def add_metric_CC(
        self, moving, fixed, radius=1, percent=100, random=False, weight=1.0
    ):
        self.__add_metric("CC", moving, fixed, radius, percent, random, weight)

    def add_metric_MSQ(
        self, moving, fixed, radius=1, percent=100, random=False, weight=1.0
    ):
        self.__add_metric("MeanSquares", moving, fixed, radius, percent, random, weight)

    def add_metric_MatchingLandmarks(self, moving_xyz, fixed_xyz, weight=1.0):
        moving_pointset_file = os.path.join(tempfile.gettempdir(), "_moving.txt")
        fixed_pointset_file = os.path.join(tempfile.gettempdir(), "_fixed.txt")
        self.__write_pointset(moving_xyz, 1, moving_pointset_file)
        self.__write_pointset(fixed_xyz, 1, fixed_pointset_file)
        self.metrics.append(
            "ICP[%s,%s,%f]" % (fixed_pointset_file, moving_pointset_file, weight)
        )

    def __write_pointset(self, xyz, label, file_path):
        with open(file_path, "w") as f:
            f.write("%g %g %g %d\n" % (xyz[0], xyz[1], xyz[2], label))

    def __add_metric(
        self, metric, moving, fixed, radius_or_bin, percent, random, weight
    ):
        if percent == 100:
            sampling = "None"
        elif random:
            sampling = "Random"
        else:
            sampling = "Regular"

        percent = percent / 100.0

        self.metrics.append(
            "%s[%s,%s,%f,%d,%s,%g]"
            % (metric, fixed, moving, weight, radius_or_bin, sampling, percent)
        )

    def get_args(self):

        args = []

        # add metrics
        for m in self.metrics:
            args.extend(["-m", m])

        # add transform
        args.append("-t")
        if self.transform_type == "BSpline":
            meshSize = "x".join(str(x) for x in self.mesh_size_at_base_level)
            args.append(
                "%s[%g,%s]" % (self.transform_type, self.gradient_step, meshSize)
            )
        elif self.transform_type in ["BSplineSyN", "BSplineDisplacementField"]:
            meshSize = "x".join(str(x) for x in self.mesh_size_at_base_level)
            args.append(
                "%s[%g,%s,%g]"
                % (
                    self.transform_type,
                    self.gradient_step,
                    meshSize,
                    self.total_field_variance_voxel_space,
                )
            )
        elif self.transform_type in ["SyN", "GaussianDisplacementField"]:
            args.append(
                "%s[%g,%g,%g]"
                % (
                    self.transform_type,
                    self.gradient_step,
                    self.update_field_variance_voxel_space,
                    self.total_field_variance_voxel_space,
                )
            )
        else:
            args.append("%s[%g]" % (self.transform_type, self.gradient_step))

        # add pyramid options
        iterations = "x".join(str(x) for x in self.iterations)
        args.extend(
            [
                "-c",
                "[%s,%g,%g]"
                % (iterations, self.convergenceThreshold, self.convergenceWindowSize),
            ]
        )

        smoothing_sigmas = "x".join(str(x) for x in self.smoothing_sigmas) + "vox"
        args.extend(["-s", "%s" % smoothing_sigmas])

        shrink_factos = "x".join(str(x) for x in self.shrink_factos)
        args.extend(["-f", "%s" % shrink_factos])

        # add mask options
        if self.fixed_mask != "NULL" or self.moving_mask != "NULL":
            args.extend(["-x", "[%s,%s]" % (self.fixed_mask, self.moving_mask)])

        return args


class Registration(object):
    def __init__(self, use_float=False, verbose=False):
        self.stages = []
        self.output_prefix = None
        self.histogramMatching = False
        self.estimateLearningRateOnce = False
        self.transformInit = None
        self.working_dir = os.getcwd()
        self.use_float = use_float
        self.input_state = None
        self.output_state = None
        self.verbose = verbose

    def init_transform_off(self):
        self.transformInit = None

    def init_transform_from_file(self, mat_file_path, inverse=0):
        self.transformInit = "[%s,%d]" % (mat_file_path, inverse)

    def init_transform_by_image_center(self, fixed, moving):
        self.transformInit = "[%s,%s,%d]" % (fixed, moving, 0)

    def init_transform_by_intensity_center(self, fixed, moving):
        self.transformInit = "[%s,%s,%d]" % (fixed, moving, 1)

    def init_transform_by_image_origin(self, fixed, moving):
        self.transformInit = "[%s,%s,%d]" % (fixed, moving, 2)

    def add_stage(self, stage):
        self.stages.append(stage)

    def get_args(self):
        # star building generic params
        args = ["-d", "3"]

        # verbose output
        if self.verbose:
            args.extend(["-v", "1"])

        # float or double?
        if self.use_float:
            args.extend(["--float"])

        # histgram matching
        if self.histogramMatching:
            args.extend(["-u", "1"])

        # estimate learning rate once
        if self.estimateLearningRateOnce:
            args.extend(["-l", "1"])

        # collapse output transforms.
        args.extend(["-z", "0"])

        # write output
        args.extend(["-o", "[%s]" % self.output_prefix])

        # write-composite-transform
        args.extend(["-a", "1"])

        # restore state
        if self.input_state:
            args.extend(["-k", "%s" % self.input_state])

        # write state
        if self.output_state:
            args.extend(["-j", "%s" % self.output_state])

        # transform init
        if self.transformInit:
            args.extend(["-r", self.transformInit])

        # add all stage params
        for stage in self.stages:
            args.extend(stage.get_args())

        return args

    def get_transform(self):
        return self.output_prefix + "Composite.h5"

    def run(self, logfile):
        args = [config.antsRegistrationCommand]
        args.extend(self.get_args())

        logfile.write(" ".join(args) + "\n\n")
        logfile.flush()

        prog = subprocess.Popen(
            args
        )
        prog.communicate()
        
        if prog.returncode != 0:
            raise Exception()
        #return True if prog.returncode == 0 else False

    def apply_transform(
        self, moving, fixed, is_labelfield=False, output=None, logfile=None
    ):
        """
		moving: 		the source image, will transformed
		fixed:  		the target image, defines spacing, origin, orientation
		is_labelfield: 	True/False, defines choice of interpolation method
		output: 		name of transformed output image
		logfile: 		log info, warnings, errors
		"""
        # automatically set output file name
        _, name = os.path.split(moving)
        output_file = self.output_prefix + name if output is None else output

        # run command
        return apply_transform(
            moving,
            fixed,
            output_file,
            self.get_transform(),
            is_labelfield,
            self.working_dir,
            logfile,
        )
