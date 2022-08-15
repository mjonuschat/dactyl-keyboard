#!/usr/bin/env python3
from __future__ import annotations

import typing as t
from pathlib import Path

from pydantic import BaseModel as PydanticBaseModel, Field, validator

from dactyl_manuform.types import (
    ControllerMount,
    KeyCapType,
    OledMount,
    RenderEngine,
    ScrewOffset,
    Side,
    ThumbStyle,
    XY,
    XYZ,
    Symmetry,
    ColumnStyle,
    PlateStyle,
)

PI = 3.14159
D2R = PI / 180
R2D = 180 / PI


class OledMountConfiguration(PydanticBaseModel):
    width: float = Field(alias="oled_mount_width")
    height: float = Field(alias="oled_mount_height")
    rim: float = Field(alias="oled_mount_rim")
    depth: float = Field(alias="oled_mount_depth")
    cut_depth: float = Field(alias="oled_mount_cut_depth")
    location_xyz: XYZ = Field(alias="oled_mount_location_xyz")
    rotation_xyz: XYZ = Field(alias="oled_mount_rotation_xyz")
    left_wall_x_offset_override: float = Field(alias="oled_left_wall_x_offset_override")
    left_wall_z_offset_override: float = Field(alias="oled_left_wall_z_offset_override")
    left_wall_lower_y_offset: float = Field(alias="oled_left_wall_lower_y_offset")
    left_wall_lower_z_offset: float = Field(alias="oled_left_wall_lower_z_offset")


class RenderConfiguration(PydanticBaseModel):
    engine: t.Optional[str] = None
    properties: t.Optional[str] = None

    model_builder: t.Optional[str] = None

    key_holes: t.Optional[str] = None
    connectors: t.Optional[str] = None
    plate_pcb_cutouts: t.Optional[str] = None
    thumb_cluster_properties: t.Optional[str] = None

    case_walls: t.Optional[str] = None
    back_wall: t.Optional[str] = None
    front_wall: t.Optional[str] = None
    left_wall: t.Optional[str] = None
    right_wall: t.Optional[str] = None
    base_plate: t.Optional[str] = None

    placement: t.Optional[str] = None
    single_plate: t.Optional[str] = None
    screw_inserts: t.Optional[str] = None
    controller_mount: t.Optional[str] = None
    oled_mount: t.Optional[str] = None
    key_caps: t.Optional[str] = None
    trackball_components: t.Optional[str] = None

    left_thumb_cluster: t.Optional[str] = None
    right_thumb_cluster: t.Optional[str] = None


class DactylManuformConfig(PydanticBaseModel):
    # The modelling engine to use for write out the CAD files
    engine: RenderEngine = Field(alias="ENGINE", default=RenderEngine.SOLID)

    ######################
    ## Shape parameters ##
    ######################
    save_dir: Path = Path(".")
    config_name: str = "DM"

    show_caps: KeyCapType = KeyCapType.MX
    show_pcbs: bool = False

    # number of key rows
    nrows: int = 5
    # number of key columns
    ncols: int = 6

    # curvature of the columns
    alpha: float = PI / 12.0
    # curvature of the rows
    beta: float = PI / 36.0

    # controls left_right tilt / tenting (higher number is more tenting)
    centercol: int = 3
    # rows from max, controls front_back tilt
    centerrow_offset: int = 3
    # or, change this for more precise tenting control
    tenting_angle: float = PI / 12.0

    # Symmetry states if it is a symmetric or asymmetric build.
    # If asymmetric it doubles the generation time.
    symmetry: Symmetry = Symmetry.SYMMETRIC

    column_style_gt5: ColumnStyle = ColumnStyle.ORTHOGRAPHIC
    column_style: ColumnStyle = ColumnStyle.DEFAULT
    # currently supports 0 or 2 due to thumb cluster attachment
    reduced_inner_cols: int = 2
    reduced_outer_cols: int = 0

    thumb_offsets: XYZ = (6, -3, 7)
    # controls overall height# original=9 with centercol=3
    # use 16 for centercol=2
    keyboard_z_offset: float = 11.0

    # extra space between the base of keys# original= 2
    extra_width: float = 2.5
    # original= 0.5
    extra_height: float = 1.0

    web_thickness: float = 4.0 + 1.1
    post_size: float = 0.1
    post_adj: float = 0.0

    #######################
    ##  THUMB PARAMETERS ##
    #######################
    thumb_style: ThumbStyle = ThumbStyle.DEFAULT
    # only used with default, makes top right thumb cluster key 1U
    default_1U_cluster: bool = True
    # Thumb key size.  May need slight oversizing, check w/ caps.
    # Additional spacing will be automatically added for larger keys.
    minidox_Usize: float = 1.6
    mini_index_key: bool = True

    # Screw locations and extra screw locations for separable thumb, all from thumb origin
    # Pulled out of hardcoding as drastic changes to the geometry may require fixes to the screw mounts.
    # First screw in separable should be similar to the standard location as it will receive the same modifiers.
    default_thumb_screw_xy_locations: t.Tuple[XY] = ((-21, -58),)
    default_separable_thumb_screw_xy_locations: t.Tuple[XY] = ((-21, -58),)
    mini_thumb_screw_xy_locations: t.Tuple[XY] = ((-29, -52),)
    mini_separable_thumb_screw_xy_locations: t.Tuple[XY, XY, XY] = (
        (-29, -52),
        (-62, 10),
        (12, -25),
    )
    minidox_thumb_screw_xy_locations: t.Tuple[XY] = ((-37, -34),)
    minidox_separable_thumb_screw_xy_locations: t.Tuple[XY, XY, XY] = (
        (-37, -34),
        (-62, 12),
        (10, -25),
    )
    carbonfet_thumb_screw_xy_locations: t.Tuple[XY] = ((-48, -37),)
    carbonfet_separable_thumb_screw_xy_locations: t.Tuple[XY, XY, XY] = (
        (-48, -37),
        (-52, 10),
        (12, -35),
    )
    orbyl_thumb_screw_xy_locations: t.Tuple[XY] = ((-53, -68),)
    orbyl_separable_thumb_screw_xy_locations: t.Tuple[XY, XY, XY] = (
        (-53, -68),
        (-66, 8),
        (10, -40),
    )
    tbcj_thumb_screw_xy_locations: t.Tuple[XY] = ((-40, -75),)
    tbcj_separable_thumb_screw_xy_locations: t.Tuple[XY, XY, XY] = (
        (-40, -75),
        (-63, 10),
        (15, -40),
    )

    # Thumb plate rotations, anything other than 90 degree increments WILL NOT WORK.
    # Top right plate rotation tweaks as thumb cluster is crowded for hot swap, etc.
    thumb_plate_tr_rotation: float = 0.0
    # Top left plate rotation tweaks as thumb cluster is crowded for hot swap, etc.
    thumb_plate_tl_rotation: float = 0.0
    # Mid right plate rotation tweaks as thumb cluster is crowded for hot swap, etc.
    thumb_plate_mr_rotation: float = 0.0
    # Mid left plate rotation tweaks as thumb cluster is crowded for hot swap, etc.
    thumb_plate_ml_rotation: float = 0.0
    # Bottom right plate rotation tweaks as thumb cluster is crowded for hot swap, etc.
    thumb_plate_br_rotation: float = 0.0
    # Bottom lef plate rotation tweaks as thumb cluster is crowded for hot swap, etc.
    thumb_plate_bl_rotation: float = 0.0

    ##################
    ## EXPERIMENTAL ##
    ##################

    # creates a separable thumb section with additional screws to hold it down.  Only attached at base.
    separable_thumb: bool = False

    ###################################
    ## Trackball in Wall             ##
    ###################################

    # Separate trackball option, placing it in the OLED area
    trackball_in_wall: bool = False
    # up from cornerrow instead of down from top
    tbiw_ball_center_row: float = 0.2
    tbiw_translational_offset: XYZ = (0.0, 0.0, 0.0)
    tbiw_rotation_offset: XYZ = (0.0, 0.0, 0.0)
    tbiw_left_wall_x_offset_override: float = 50.0
    tbiw_left_wall_z_offset_override: float = 0.0
    tbiw_left_wall_lower_x_offset: float = 0.0
    tbiw_left_wall_lower_y_offset: float = 0.0
    tbiw_left_wall_lower_z_offset: float = 0.0

    # not none, offsets are from this position
    tbiw_oled_center_row: float = 0.75
    # Z offset tweaks are expected depending on curvature and OLED mount choice.
    tbiw_oled_translation_offset: XYZ = (-3.5, 0, 1.5)
    tbiw_oled_rotation_offset: XYZ = (0.0, 0.0, 0.0)

    # TODO: This seems to overlap with TBIW / not have any reference in code
    ##############################
    ## Finger Trackball in Wall ##
    ##############################

    # Separate trackball option, placing it in the OLED area
    finger_trackball_in_wall: bool = False
    # up from cornerrow instead of down from top
    tbiw_ball_center_column: float = 0.2
    # TODO: The next two are redeclared ?
    tbiw_translational_offset: XYZ = (0.0, 0.0, 0.0)
    tbiw_rotation_offset: XYZ = (0.0, 0.0, 0.0)
    tbiw_top_wall_y_offset_override: float = 50.0
    tbiw_top_wall_z_offset_override: float = 0.0
    tbiw_top_wall_extension_cols: int = 4

    ########################################
    ## Trackball JS / ORBYL Thumb Cluster ##
    ########################################
    # cluster used for second thumb except if ball_side == 'both'
    other_thumb: ThumbStyle = ThumbStyle.DEFAULT
    tbjs_key_diameter: float = 70.0
    # size for inner key near trackball
    tbjs_Uwidth: float = 1.2
    # size for inner key near trackball
    tbjs_Uheight: float = 1.2

    # Offsets are per key and are applied before rotating into place around the ball
    # X and Y act like Tangential and Radial around the ball
    # applied to the whole assy
    tbjs_translation_offset: XYZ = (0, 0, 2)
    # applied to the whole assy
    tbjs_rotation_offset: XYZ = (0, -8, 0)
    tbjs_key_translation_offsets: t.Tuple[XYZ, XYZ, XYZ, XYZ] = (
        (0.0, 0.0, -3.0 - 5),
        (0.0, 0.0, -3.0 - 5),
        (0.0, 0.0, -3.0 - 5),
        (0.0, 0.0, -3.0 - 5),
    )
    tbjs_key_rotation_offsets: t.Tuple[XYZ, XYZ, XYZ, XYZ] = (
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
    )

    ###################################
    ## Trackball CJ Thumb Cluster    ##
    ###################################
    tbcj_inner_diameter: float = 42.0
    tbcj_thickness: float = 2.0
    tbcj_outer_diameter: float = 53.0

    ###################################
    ## Trackball General             ##
    ###################################
    # Added, creates a hole with space for the lip size listed below.
    trackball_modular: bool = False
    # width of lip cleared out in ring location
    trackball_modular_lip_width: float = 3.0
    # height of ball from ring , used to create identical position to fixed.
    trackball_modular_ball_height: float = 3.0
    # height mount ring down from ball height. Covers gap on elevated ball.
    trackball_modular_ring_height: float = 10.0
    # height of ball from ring, used to create identical position to fixed.
    trackball_modular_clearance: float = 0.5

    ball_side: Side = Side.BOTH
    ball_diameter: float = 34.0
    # should not be changed unless the import models are changed.
    ball_wall_thickness: float = 3.0
    ball_gap: float = 1.0
    trackball_hole_diameter: float = 36.5
    trackball_hole_height: float = 40.0
    trackball_plate_thickness: float = 2.0
    trackball_plate_width: float = 2.0
    # Removed trackball_rotation, ball_z_offset. and trackball_sensor_rotation and added more flexibility.
    # applied to the socket and sensor, large values will cause web/wall issues.
    tb_socket_translation_offset: XYZ = (0.0, 0.0, 2.0)
    # applied to the socket and sensor, large values will cause web/wall issues.
    tb_socket_rotation_offset: XYZ = (0.0, 0.0, 0.0)
    # deviation from socket offsets, for fixing generated geometry issues
    tb_sensor_translation_offset: XYZ = (0.0, 0.0, 0.0)
    # deviation from socket offsets, for changing the sensor roll orientation
    tb_sensor_rotation_offset: XYZ = (0.0, 0.0, 0.0)

    ##################
    ## EXPERIMENTAL ##
    ##################

    # LEAVE AS FALSE, CURRENTLY BROKEN
    pinky_1_5U: bool = False
    first_1_5U_row: float = 0.0
    last_1_5U_row: float = 5.0
    skeletal: bool = False

    ##################
    ## WALLS        ##
    ##################
    # length of the first downward_sloping part of the wall
    wall_z_offset: float = 15.0
    # offset in the x and/or y direction for the first downward_sloping part of the wall (negative)
    wall_x_offset: float = 5.0
    # offset in the x and/or y direction for the first downward_sloping part of the wall (negative)
    wall_y_offset: float = 6.0
    # specific values for the left side due to the minimal wall.
    left_wall_x_offset: float = 12.0
    # specific values for the left side due to the minimal wall.
    left_wall_z_offset: float = 3.0
    # specific values for the lower left corner.
    left_wall_lower_x_offset: float = 0.0
    left_wall_lower_y_offset: float = 0.0
    left_wall_lower_z_offset: float = 0.0
    # wall thickness parameter used on upper/mid stage of the wall
    wall_thickness: float = 4.5
    # wall thickness at the lower stage
    wall_base_y_thickness: float = 4.5
    wall_base_x_thickness: float = 4.5

    # wall thickness at the lower stage specifically in back for interface.
    wall_base_back_thickness: float = 4.5

    # Setting for Column Style: FIXED
    # The defaults roughly match Maltron settings
    #   http://patentimages.storage.googleapis.com/EP0219944A2/imgf0002.png
    ## fixed_z overrides the z portion of the column ofsets above.
    ## NOTE: THIS DOESN'T WORK QUITE LIKE I'D HOPED.
    fixed_angles: t.Tuple[float, float, float, float, float, float, float] = (
        D2R * 10,
        D2R * 10,
        0,
        0,
        0,
        D2R * -15,
        D2R * -15,
    )
    # relative to the middle finger
    fixed_x: t.Tuple[float, float, float, float, float, float, float] = (
        -41.5,
        -22.5,
        0,
        20.3,
        41.4,
        65.5,
        89.6,
    )
    fixed_z: t.Tuple[float, float, float, float, float, float, float] = (
        12.1,
        8.3,
        0,
        5,
        10.7,
        14.5,
        17.5,
    )
    fixed_tenting: float = D2R * 0.0

    #################
    ## Switch Hole ##
    #################
    plate_style: PlateStyle = PlateStyle.NOTCH

    hole_keyswitch_height: float = 14.0
    hole_keyswitch_width: float = 14.0

    nub_keyswitch_height: float = 14.4
    nub_keyswitch_width: float = 14.4

    undercut_keyswitch_height: float = 14.0
    undercut_keyswitch_width: float = 14.0
    # If using notch, it is identical to undecut, but only locally by the switch clip
    notch_width: float = 6.0

    sa_profile_key_height: float = 12.7
    sa_length: float = 18.5
    sa_double_length: float = 37.5
    plate_thickness: float = 4.0 + 1.1

    plate_rim: float = 1.5 + 0.5
    # Undercut style dimensions
    clip_thickness: float = 1.1
    clip_undercut: float = 1.0
    # NOT FUNCTIONAL WITH OPENSCAD, ONLY WORKS WITH CADQUERY
    undercut_transition: float = 0.2

    # Custom plate step file
    plate_file: t.Optional[str] = None
    plate_offset: float = 0.0

    #########################
    ## OLED Mount Location ##
    #########################
    oled_mount_type: OledMount = OledMount.CLIP
    # if not None, this will override the oled_mount_location_xyz and oled_mount_rotation_xyz settings
    oled_center_row: float = 1.25
    # Z offset tweaks are expected depending on curvature and OLED mount choice.
    oled_translation_offset: XYZ = (0.0, 0.0, 4.0)
    oled_rotation_offset: XYZ = (0.0, 0.0, 0.0)

    oled_configurations: t.Dict[OledMount, t.Dict[str, t.Union[float, XYZ]]] = {
        OledMount.UNDERCUT: {
            # Common parameters
            "oled_mount_width": 15.0,
            "oled_mount_height": 35.0,
            "oled_mount_rim": 3.0,
            "oled_mount_depth": 6.0,
            "oled_mount_cut_depth": 20.0,
            # will be overwritten if oled_center_row is not None
            "oled_mount_location_xyz": (
                -80.0,
                20.0,
                45.0,
            ),
            # will be overwritten if oled_center_row is not None
            "oled_mount_rotation_xyz": (
                13.0,
                0.0,
                -6.0,
            ),
            "oled_left_wall_x_offset_override": 28.0,
            "oled_left_wall_z_offset_override": 0.0,
            "oled_left_wall_lower_y_offset": 12.0,
            "oled_left_wall_lower_z_offset": 5.0,
            #########################
            ## UNDERCUT PARAMETERS ##
            #########################
            "oled_mount_undercut": 1.0,
            "oled_mount_undercut_thickness": 2.0,
        },
        OledMount.SLIDING: {
            # Common parameters
            # width of OLED, plus clearance
            "oled_mount_width": 12.5,
            # length of screen
            "oled_mount_height": 25.0,
            "oled_mount_rim": 2.5,
            "oled_mount_depth": 8.0,
            "oled_mount_cut_depth": 20.0,
            # will be overwritten if oled_center_row is not None
            "oled_mount_location_xyz": (-78.0, 10.0, 41.0),
            # will be overwritten if oled_center_row is not None
            "oled_mount_rotation_xyz": (6.0, 0.0, -3.0),
            "oled_left_wall_x_offset_override": 24.0,
            "oled_left_wall_z_offset_override": 0.0,
            "oled_left_wall_lower_y_offset": 12.0,
            "oled_left_wall_lower_z_offset": 5.0,
            ########################
            ## SLIDING PARAMETERS ##
            ########################
            # thickness of OLED, plus clearance.  Must include components
            "oled_thickness": 4.2,
            # length from end of viewable screen to end of PCB
            "oled_edge_overlap_end": 6.5,
            # length from end of viewable screen to end of PCB on connection side.
            "oled_edge_overlap_connector": 5.5,
            # thickness of material over edge of PCB
            "oled_edge_overlap_thickness": 2.5,
            # Clearance to insert PCB before laying down and sliding.
            "oled_edge_overlap_clearance": 2.5,
            "oled_edge_chamfer": 2.0,
        },
        OledMount.CLIP: {
            # Common parameters
            # whole OLED width
            "oled_mount_width": 12.5,
            # whole OLED length
            "oled_mount_height": 39.0,
            "oled_mount_rim": 2.0,
            "oled_mount_depth": 7.0,
            "oled_mount_cut_depth": 20.0,
            # will be overwritten if oled_center_row is not None
            "oled_mount_location_xyz": (-78.0, 20.0, 42.0),
            # will be overwritten if oled_center_row is not None
            "oled_mount_rotation_xyz": (12.0, 0.0, -6.0),
            "oled_left_wall_x_offset_override": 24.0,
            "oled_left_wall_z_offset_override": 0.0,
            "oled_left_wall_lower_y_offset": 12.0,
            "oled_left_wall_lower_z_offset": 5.0,
            #####################
            ## CLIP PARAMETERS ##
            #####################
            # thickness of OLED, plus clearance.  Must include components
            "oled_thickness": 4.2,
            # z thickness of clip bezel
            "oled_mount_bezel_thickness": 3.5,
            # depth of the 45 degree chamfer
            "oled_mount_bezel_chamfer": 2.0,
            "oled_mount_connector_hole": 6.0,
            "oled_screen_start_from_conn_end": 6.5,
            "oled_screen_length": 24.5,
            "oled_screen_width": 10.5,
            "oled_clip_thickness": 1.5,
            "oled_clip_width": 6.0,
            "oled_clip_overhang": 1.0,
            "oled_clip_extension": 5.0,
            "oled_clip_width_clearance": 0.5,
            "oled_clip_undercut": 0.5,
            "oled_clip_undercut_thickness": 2.5,
            "oled_clip_y_gap": 0.2,
            "oled_clip_z_gap": 0.2,
        },
    }

    ###################
    ## SCREW INSERTS ##
    ###################
    screws_offset: ScrewOffset = ScrewOffset.INSIDE
    screw_insert_height: float = 3.8
    # Designed for self tapping - use 5.31 / 2 for inserts
    screw_insert_bottom_radius: float = 2.5 / 2
    # Designed for self tapping, - use 5.1 / 2 for inserts
    screw_insert_top_radius: float = 2.5 / 2
    # Common to keep interface to base
    screw_insert_outer_radius: float = 4.25

    # Does anyone even use these?  I think they just get in the way.
    wire_post_height: float = 7.0
    wire_post_overhang: float = 3.5
    wire_post_diameter: float = 2.6

    ###################################
    ## Controller Mount / Connectors ##
    ###################################
    controller_mount_type: ControllerMount = ControllerMount.EXTERNAL

    external_holder_height: float = 12.5
    external_holder_width: float = 28.75
    external_holder_xoffset: float = -5.0
    # Tweak this value to get the right undercut for the tray engagement.
    external_holder_yoffset: float = -4.5

    ###################################
    ## PCB Screw Mount               ##
    ###################################
    pcb_mount_ref_offset: XYZ = (0.0, -5.0, 0.0)
    pcb_holder_size: XYZ = (34.6, 7.0, 4.0)
    pcb_holder_offset: XYZ = (8.9, 0.0, 0.0)

    pcb_usb_hole_size: XYZ = (7.5, 10.0, 4.0)
    pcb_usb_hole_offset: XYZ = (15.0, 0.0, 4.5)

    wall_thinner_size: XYZ = (34.0, 7.0, 10.0)

    trrs_hole_size: XY = (3.0, 20)
    trrs_offset: XYZ = (0.0, 0.0, 1.5)

    pcb_screw_hole_size: XY = (0.5, 10.0)
    pcb_screw_x_offsets: t.Tuple[float, float, float] = (-5.5, 7.75, 22.0)
    pcb_screw_y_offset: float = -2.0

    #############################
    ## Bottom Plate Dimensions ##
    #############################
    # COMMON DIMENSION
    screw_hole_diameter: float = 3.0
    # USED FOR CADQUERY ONLY
    # thickness in the middle of the plate
    base_thickness: float = 3.0
    # Both start flat/flush on the bottom.  This offsets the base up (if positive)
    base_offset: float = 3.0
    # thickness on the outer frame with screws
    base_rim_thickness: float = 5.0
    screw_cbore_diameter: float = 6.0
    screw_cbore_depth: float = 2.5

    ###################################
    ## HOLES ON PLATE FOR PCB MOUNT
    ###################################
    plate_holes: bool = True
    plate_holes_xy_offset: XY = (0.0, 0.0)
    plate_holes_width: float = 14.3
    plate_holes_height: float = 14.3
    plate_holes_diameter: float = 1.6
    plate_holes_depth: float = 20.0

    ##################
    ## EXPERIMENTAL ##
    ##################
    plate_pcb_clear: bool = False
    plate_pcb_size: XYZ = (18.5, 18.5, 5.0)
    # this is off of the back of the plate size.
    plate_pcb_offset: XYZ = (0.0, 0.0, 0.0)

    ############################
    ## SHOW PCB FOR FIT CHECK ##
    ############################
    pcb_width: float = 18.0
    pcb_height: float = 18.0
    pcb_thickness: float = 1.5
    pcb_hole_diameter: float = 2.0
    pcb_hole_pattern_width: float = 14.3
    pcb_hole_pattern_height: float = 14.3

    ####################
    ## COLUMN OFFSETS ##
    ####################
    column_offsets: t.Tuple[XYZ, XYZ, XYZ, XYZ, XYZ, XYZ, XYZ] = (
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
        (0.0, 2.82, -4.5),
        (0.0, 0.0, 0.0),
        (0.0, -6.0, 5.0),  # REDUCED STAGGER
        (0.0, -6.0, 5.0),  # REDUCED STAGGER
        (0.0, -6.0, 5.0),  # NOT USED IN MOST FORMATS (7th column)
    )

    ###############################
    ## END CONFIGURATION SECTION ##
    ###############################

    @validator("show_caps", pre=True)
    @classmethod
    def _show_caps_validator(cls, value: t.Union[None, str, bool]) -> str:
        if isinstance(value, str):
            return value

        if value:
            return "MX"

        return "NONE"

    @validator("oled_mount_type", pre=True)
    @classmethod
    def _oled_mount_type_validator(cls, value: t.Optional[str]) -> str:
        if value is None:
            return "NONE"

        return value
