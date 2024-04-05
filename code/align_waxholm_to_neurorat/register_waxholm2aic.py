import os, sys
from collections import namedtuple, Mapping

sys.path.append(r"E:\Develop\Scripts\RegistrationScripts")
import ants


def namedtuple_with_defaults(typename, field_names, default_values=()):
    T = namedtuple(typename, field_names)
    T.__new__.__defaults__ = (None,) * len(T._fields)
    if isinstance(default_values, Mapping):
        prototype = T(**default_values)
    else:
        prototype = T(*default_values)
    T.__new__.__defaults__ = tuple(prototype)
    return T


# -------------------------------------------------------------------------------
Parameters = namedtuple_with_defaults(
    "Parameters",
    "moving fixed moving2 fixed2 transforms output_prefix working_dir gradient_step",
)

param = Parameters(
    moving=r"F:\Data\oSPARC\RatVagus\WaxholmAtlas\prealigned\WHS_T2star_prealigned.nii.gz",
    fixed=r"F:\Data\oSPARC\RatVagus\WaxholmAtlas\oSPARC_space\aic_t1_cropped_350_336_162.nii.gz",
    working_dir=r"F:\Data\oSPARC\RatVagus\WaxholmAtlas\whs2osparc",
    gradient_step=0.05,
)

moving_mask = "NULL"
moving_mask = (
    r"F:\Data\oSPARC\RatVagus\WaxholmAtlas\prealigned\WHS_mask3_prealigned.nii.gz"
)
fixed_mask = r"F:\Data\oSPARC\RatVagus\WaxholmAtlas\oSPARC_space\mask_cortex.nii.gz"

moving_labels = (
    r"F:\Data\oSPARC\RatVagus\WaxholmAtlas\prealigned\WHS_atlas_prealigned.nii.gz"
)
fixed_labels = r"F:\Data\oSPARC\RatVagus\WaxholmAtlas\oSPARC_space\aic_labels_cropped_350_336_162.nii.gz"

# -------------------------------------------------------------------------------
working_dir = param.working_dir
if not os.path.exists(working_dir):
    os.mkdir(working_dir)

# create registration driver
reg = ants.Registration()
reg.init_transform_off()
reg.output_prefix = os.path.join(working_dir, "whs2osparc_bsyn_msb3_")
reg.working_dir = working_dir

# add rigid stage
stage0 = ants.Stage()
stage0.set_pyramid_options(3, [80, 40, 20], [4, 2, 1], [2, 1, 0])
stage0.set_transform("Translation", param.gradient_step)
stage0.add_metric_MI(param.moving, param.fixed, histogram_bins=50, percent=50)
stage0.set_masks(moving_mask=moving_mask)
reg.add_stage(stage0)

stage1 = ants.Stage()
stage1.set_pyramid_options(3, [80, 40, 20], [4, 2, 1], [2, 1, 0])
stage1.set_transform("Rigid", param.gradient_step)
stage1.add_metric_MI(param.moving, param.fixed, histogram_bins=50, percent=50)
stage1.set_masks(moving_mask=moving_mask)
reg.add_stage(stage1)

stage2 = ants.Stage()
stage2.set_pyramid_options(3, [80, 40, 20], [4, 2, 1], [2, 1, 0])
stage2.set_transform("Affine", param.gradient_step)
stage2.add_metric_MI(param.moving, param.fixed, histogram_bins=50, percent=50)
stage2.set_masks(moving_mask=moving_mask)
reg.add_stage(stage2)

stage_syn = ants.Stage()
stage_syn.set_pyramid_options(3, [80, 80, 80], [8, 4, 2], [3, 2, 1])
stage_syn.set_transform("BSplineSyN", param.gradient_step, mesh_size_at_base_level=[3])
stage_syn.add_metric_MI(param.moving, param.fixed, histogram_bins=50, percent=50)
reg.add_stage(stage_syn)

with open(reg.output_prefix + ".log", "w") as logfile:

    for name, value in param._asdict().items():
        logfile.write("%s = %s\n" % (name, str(value)))

    try:
        logfile.write("\n\nStarting registration\n\n")
        logfile.flush()

        if True:  # reg.run(logfile):

            logfile.write("\n\nStarting transform\n\n")
            logfile.flush()
            # reg.apply_transform(param.moving, param.fixed, False, output=None, logfile=logfile)

            ofile = reg.output_prefix + "whs_atlas_aligned_osparcratwears.nii.gz"
            fixed_labels = r"F:\Data\oSPARC\RatVagus\WaxholmAtlas\whs2osparc\Rat_oSPARC_1-2300_20200810ears_labels.nii.gz"
            reg.apply_transform(
                moving_labels, fixed_labels, True, output=ofile, logfile=logfile
            )
            # reg.apply_transform(moving_labels, fixed_labels, True, output=None, logfile=logfile)

        else:
            logfile.write("Registration return FAILURE\n\n")
    except:
        logfile.write("Exception when trying to run ants.Registration\n")
        for e in sys.exc_info():
            logfile.write("\t%s\n" % (e))
