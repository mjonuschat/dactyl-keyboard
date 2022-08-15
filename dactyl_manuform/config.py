#!/usr/bin/env python3
from __future__ import annotations

import typing as t
from pathlib import Path

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
)

from pydantic import BaseModel as PydanticBaseModel, Field, validator


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
    engine: RenderEngine = Field(alias="ENGINE")

    # Shape Parameters
    save_dir: Path
    config_name: str
    show_caps: KeyCapType
    show_pcbs: bool
    nrows: int
    ncols: int
    alpha: float
    beta: float
    centercol: int
    centerrow_offset: int
    tenting_angle: float
    symmetry: str
    column_style_gt5: str
    column_style: str
    reduced_inner_cols: int
    reduced_outer_cols: int
    thumb_offsets: XYZ
    keyboard_z_offset: float
    extra_width: float
    extra_height: float
    web_thickness: float
    post_size: float
    post_adj: float

    # Thumb Parameters
    thumb_style: ThumbStyle
    default_1U_cluster: bool
    minidox_Usize: float
    mini_index_key: bool

    default_thumb_screw_xy_locations: t.Tuple[XY]
    default_separable_thumb_screw_xy_locations: t.Tuple[XY]
    mini_thumb_screw_xy_locations: t.Tuple[XY]
    mini_separable_thumb_screw_xy_locations: t.Tuple[XY, XY, XY]
    minidox_thumb_screw_xy_locations: t.Tuple[XY]
    minidox_separable_thumb_screw_xy_locations: t.Tuple[XY, XY, XY]
    carbonfet_thumb_screw_xy_locations: t.Tuple[XY]
    carbonfet_separable_thumb_screw_xy_locations: t.Tuple[XY, XY, XY]
    orbyl_thumb_screw_xy_locations: t.Tuple[XY]
    orbyl_separable_thumb_screw_xy_locations: t.Tuple[XY, XY, XY]
    tbcj_thumb_screw_xy_locations: t.Tuple[XY]
    tbcj_separable_thumb_screw_xy_locations: t.Tuple[XY, XY, XY]
    thumb_plate_tr_rotation: float
    thumb_plate_tl_rotation: float
    thumb_plate_mr_rotation: float
    thumb_plate_ml_rotation: float
    thumb_plate_br_rotation: float
    thumb_plate_bl_rotation: float
    separable_thumb: bool

    # Trackball in Wall
    trackball_in_wall: bool
    tbiw_ball_center_row: float
    tbiw_translational_offset: XYZ
    tbiw_rotation_offset: XYZ
    tbiw_left_wall_x_offset_override: float
    tbiw_left_wall_z_offset_override: float
    tbiw_left_wall_lower_x_offset: float
    tbiw_left_wall_lower_y_offset: float
    tbiw_left_wall_lower_z_offset: float
    tbiw_oled_center_row: float
    tbiw_oled_translation_offset: XYZ
    tbiw_oled_rotation_offset: XYZ

    # Finger Trackball in Wall EXPERIMENTAL WIP!!!!
    finger_trackball_in_wall: bool
    tbiw_ball_center_column: float
    tbiw_translational_offset: XYZ
    tbiw_rotation_offset: XYZ
    tbiw_top_wall_y_offset_override: float
    tbiw_top_wall_z_offset_override: float
    tbiw_top_wall_extension_cols: int

    # Trackball JS / ORBYL Thumb Cluster
    other_thumb: ThumbStyle
    tbjs_key_diameter: float
    tbjs_Uwidth: float
    tbjs_Uheight: float
    tbjs_translation_offset: XYZ
    tbjs_rotation_offset: XYZ
    tbjs_key_translation_offsets: t.Tuple[XYZ, XYZ, XYZ, XYZ]
    tbjs_key_rotation_offsets: t.Tuple[XYZ, XYZ, XYZ, XYZ]

    # Trackball CJ Thumb Cluster
    tbcj_inner_diameter: float
    tbcj_thickness: float
    tbcj_outer_diameter: float

    # Trackball General
    trackball_modular: bool
    trackball_modular_lip_width: float
    trackball_modular_ball_height: float
    trackball_modular_ring_height: float
    trackball_modular_clearance: float

    ball_side: Side
    ball_diameter: float
    ball_wall_thickness: float
    ball_gap: float
    trackball_hole_diameter: float
    trackball_hole_height: float
    trackball_plate_thickness: float
    trackball_plate_width: float
    tb_socket_translation_offset: XYZ
    tb_socket_rotation_offset: XYZ
    tb_sensor_translation_offset: XYZ
    tb_sensor_rotation_offset: XYZ

    # EXPERIMENTAL PARAMETERS
    pinky_1_5U: bool
    first_1_5U_row: float
    last_1_5U_row: float
    skeletal: bool

    # TODO: Which group?
    wall_z_offset: float
    wall_x_offset: float
    wall_y_offset: float
    left_wall_x_offset: float
    left_wall_z_offset: float
    left_wall_lower_x_offset: float
    left_wall_lower_y_offset: float
    left_wall_lower_z_offset: float
    wall_thickness: float
    wall_base_y_thickness: float
    wall_base_x_thickness: float
    wall_base_back_thickness: float

    # Column Style: FIXED
    fixed_angles: t.Tuple[float, float, float, float, float, float, float]
    fixed_x: t.Tuple[float, float, float, float, float, float, float]
    fixed_z: t.Tuple[float, float, float, float, float, float, float]
    fixed_tenting: float

    # Switch Hole
    plate_style: str

    hole_keyswitch_height: float
    hole_keyswitch_width: float

    nub_keyswitch_height: float
    nub_keyswitch_width: float

    undercut_keyswitch_height: float
    undercut_keyswitch_width: float
    notch_width: float

    sa_profile_key_height: float
    sa_length: float
    sa_double_length: float
    plate_thickness: float

    plate_rim: float
    # Undercut style dimensions
    clip_thickness: float
    clip_undercut: float
    undercut_transition: float

    # Custom plate step file
    plate_file: t.Optional[str]
    plate_offset: float

    # OLED Mount Location
    oled_mount_type: OledMount
    oled_center_row: float
    oled_translation_offset: XYZ
    oled_rotation_offset: XYZ

    oled_configurations: t.Dict[OledMount, t.Dict[str, t.Union[float, XYZ]]]

    # TODO: Section (Plate?)
    screws_offset: ScrewOffset
    screw_insert_height: float
    screw_insert_bottom_radius: float
    screw_insert_top_radius: float
    screw_insert_outer_radius: float

    wire_post_height: float
    wire_post_overhang: float
    wire_post_diameter: float

    # Controller Mount / Connectors
    controller_mount_type: ControllerMount

    external_holder_height: float
    external_holder_width: float
    external_holder_xoffset: float
    external_holder_yoffset: float

    # PCB Screw Mount
    pcb_mount_ref_offset: XYZ
    pcb_holder_size: XYZ
    pcb_holder_offset: XYZ
    pcb_usb_hole_size: XYZ
    pcb_usb_hole_offset: XYZ
    wall_thinner_size: XYZ
    trrs_hole_size: XY
    trrs_offset: XYZ
    pcb_screw_hole_size: XY
    pcb_screw_x_offsets: t.Tuple[float, float, float]
    pcb_screw_y_offset: float

    # Bottom Plate Dimensions
    # COMMON DIMENSION
    screw_hole_diameter: float
    # USED FOR CADQUERY ONLY
    base_thickness: float
    base_offset: float
    base_rim_thickness: float
    screw_cbore_diameter: float
    screw_cbore_depth: float

    # HOLES ON PLATE FOR PCB MOUNT
    plate_holes: bool
    plate_holes_xy_offset: XY
    plate_holes_width: float
    plate_holes_height: float
    plate_holes_diameter: float
    plate_holes_depth: float
    # EXPERIMENTAL
    plate_pcb_clear: bool
    plate_pcb_size: XYZ
    plate_pcb_offset: XYZ

    # SHOW PCB FOR FIT CHECK
    pcb_width: float
    pcb_height: float
    pcb_thickness: float
    pcb_hole_diameter: float
    pcb_hole_pattern_width: float
    pcb_hole_pattern_height: float

    # COLUMN OFFSETS
    column_offsets: t.Tuple[XYZ, XYZ, XYZ, XYZ, XYZ, XYZ, XYZ]

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
