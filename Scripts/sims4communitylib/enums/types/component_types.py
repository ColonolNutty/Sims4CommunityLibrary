"""
This file is part of the Sims 4 Community Library, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""


class CommonComponentType:
    """A wrapper for component_types.

    """
    def _get_component_type(*args):
        try:
            import objects.components.types as component_types
            return getattr(component_types, args[0])
        except KeyError:
            return args[0]

    ANIMATION = _get_component_type('ANIMATION_COMPONENT')
    AUDIO = _get_component_type('AUDIO_COMPONENT')
    EFFECTS = _get_component_type('EFFECTS_COMPONENT')
    FOOTPRINT = _get_component_type('FOOTPRINT_COMPONENT')
    GAMEPLAY = _get_component_type('GAMEPLAY_COMPONENT')
    LIVE_DRAG = _get_component_type('LIVE_DRAG_COMPONENT')
    POSITION = _get_component_type('POSITION_COMPONENT')
    RENDER = _get_component_type('RENDER_COMPONENT')
    ROUTING = _get_component_type('ROUTING_COMPONENT')
    SIM = _get_component_type('SIM_COMPONENT')
    VIDEO = _get_component_type('VIDEO_COMPONENT')
    AFFORDANCE_TUNING = _get_component_type('AFFORDANCE_TUNING_COMPONENT')
    ANIMATION_OVERLAY = _get_component_type('ANIMATION_OVERLAY_COMPONENT')
    AUTONOMY = _get_component_type('AUTONOMY_COMPONENT')
    AWARENESS = _get_component_type('AWARENESS_COMPONENT')
    BUFF = _get_component_type('BUFF_COMPONENT')
    CAMERA_VIEW = _get_component_type('CAMERA_VIEW_COMPONENT')
    CANVAS = _get_component_type('CANVAS_COMPONENT')
    CARRYABLE = _get_component_type('CARRYABLE_COMPONENT')
    CARRYING = _get_component_type('CARRYING_COMPONENT')
    CHANNEL = _get_component_type('CHANNEL_COMPONENT')
    CENSOR_GRID = _get_component_type('CENSOR_GRID_COMPONENT')
    COLLECTABLE = _get_component_type('COLLECTABLE_COMPONENT')
    CONSUMABLE = _get_component_type('CONSUMABLE_COMPONENT')
    CRAFTING = _get_component_type('CRAFTING_COMPONENT')
    CRAFTING_STATION = _get_component_type('CRAFTING_STATION_COMPONENT')
    CURFEW = _get_component_type('CURFEW_COMPONENT')
    ENSEMBLE = _get_component_type('ENSEMBLE_COMPONENT')
    ENVIRONMENT_SCORE = _get_component_type('ENVIRONMENT_SCORE_COMPONENT')
    FLOWING_PUDDLE = _get_component_type('FLOWING_PUDDLE_COMPONENT')
    FOCUS = _get_component_type('FOCUS_COMPONENT')
    GAME = _get_component_type('GAME_COMPONENT')
    GARDENING = _get_component_type('GARDENING_COMPONENT')
    IDLE = _get_component_type('IDLE_COMPONENT')
    INVENTORY = _get_component_type('INVENTORY_COMPONENT')
    INVENTORY_ITEM = _get_component_type('INVENTORY_ITEM_COMPONENT')
    LIGHTING = _get_component_type('LIGHTING_COMPONENT')
    LINE_OF_SIGHT = _get_component_type('LINE_OF_SIGHT_COMPONENT')
    LINKED_OBJECT = _get_component_type('LINKED_OBJECT_COMPONENT')
    LIVE_DRAG_TARGET = _get_component_type('LIVE_DRAG_TARGET_COMPONENT')
    MANNEQUIN = _get_component_type('MANNEQUIN_COMPONENT')
    NAME = _get_component_type('NAME_COMPONENT')
    NEW_OBJECT = _get_component_type('NEW_OBJECT_COMPONENT')
    OBJECT_AGE = _get_component_type('OBJECT_AGE_COMPONENT')
    OBJECT_RELATIONSHIP = _get_component_type('OBJECT_RELATIONSHIP_COMPONENT')
    OBJECT_ROUTING = _get_component_type('OBJECT_ROUTING_COMPONENT')
    OBJECT_TELEPORTATION = _get_component_type('OBJECT_TELEPORTATION_COMPONENT')
    OWNABLE = _get_component_type('OWNABLE_COMPONENT')
    PARENT_TO_SIM_HEAD = _get_component_type('PARENT_TO_SIM_HEAD_COMPONENT')
    PORTAL = _get_component_type('PORTAL_COMPONENT')
    PORTAL_ANIMATION = _get_component_type('PORTAL_ANIMATION_COMPONENT')
    PORTAL_LOCKING = _get_component_type('PORTAL_LOCKING_COMPONENT')
    PROXIMITY = _get_component_type('PROXIMITY_COMPONENT')
    SEASON_AWARE = _get_component_type('SEASON_AWARE_COMPONENT')
    SLOT = _get_component_type('SLOT_COMPONENT')
    SPAWN_POINT = _get_component_type('SPAWN_POINT_COMPONENT')
    SPAWNER = _get_component_type('SPAWNER_COMPONENT')
    STATE = _get_component_type('STATE_COMPONENT')
    STATISTIC = _get_component_type('STATISTIC_COMPONENT')
    STORED_OBJECT_INFO = _get_component_type('STORED_OBJECT_INFO_COMPONENT')
    STORED_SIM_INFO = _get_component_type('STORED_SIM_INFO_COMPONENT')
    TIME_OF_DAY = _get_component_type('TIME_OF_DAY_COMPONENT')
    TOOLTIP = _get_component_type('TOOLTIP_COMPONENT')
    TOPIC = _get_component_type('TOPIC_COMPONENT')
    FISHING_LOCATION = _get_component_type('FISHING_LOCATION_COMPONENT')
    WAITING_LINE = _get_component_type('WAITING_LINE_COMPONENT')
    DISPLAY = _get_component_type('DISPLAY_COMPONENT')
    RETAIL = _get_component_type('RETAIL_COMPONENT')
    STOLEN = _get_component_type('STOLEN_COMPONENT')
    EXAMPLE = _get_component_type('EXAMPLE_COMPONENT')
    WEATHER_AWARE = _get_component_type('WEATHER_AWARE_COMPONENT')
