"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any


class CommonComponentType:
    """Various component types of vanilla Sims 4

    Components are essentially just Tuning files in package files.

    """
    def _get_component_type(*args) -> Any:
        try:
            import objects.components.types as component_types
            return getattr(component_types, args[0])
        except KeyError:
            return args[0]

    ANIMATION: 'CommonComponentType' = _get_component_type('ANIMATION_COMPONENT')
    AUDIO: 'CommonComponentType' = _get_component_type('AUDIO_COMPONENT')
    EFFECTS: 'CommonComponentType' = _get_component_type('EFFECTS_COMPONENT')
    FOOTPRINT: 'CommonComponentType' = _get_component_type('FOOTPRINT_COMPONENT')
    GAMEPLAY: 'CommonComponentType' = _get_component_type('GAMEPLAY_COMPONENT')
    LIVE_DRAG: 'CommonComponentType' = _get_component_type('LIVE_DRAG_COMPONENT')
    POSITION: 'CommonComponentType' = _get_component_type('POSITION_COMPONENT')
    RENDER: 'CommonComponentType' = _get_component_type('RENDER_COMPONENT')
    ROUTING: 'CommonComponentType' = _get_component_type('ROUTING_COMPONENT')
    SIM: 'CommonComponentType' = _get_component_type('SIM_COMPONENT')
    VIDEO: 'CommonComponentType' = _get_component_type('VIDEO_COMPONENT')
    AFFORDANCE_TUNING: 'CommonComponentType' = _get_component_type('AFFORDANCE_TUNING_COMPONENT')
    ANIMATION_OVERLAY: 'CommonComponentType' = _get_component_type('ANIMATION_OVERLAY_COMPONENT')
    AUTONOMY: 'CommonComponentType' = _get_component_type('AUTONOMY_COMPONENT')
    AWARENESS: 'CommonComponentType' = _get_component_type('AWARENESS_COMPONENT')
    BUFF: 'CommonComponentType' = _get_component_type('BUFF_COMPONENT')
    CAMERA_VIEW: 'CommonComponentType' = _get_component_type('CAMERA_VIEW_COMPONENT')
    CANVAS: 'CommonComponentType' = _get_component_type('CANVAS_COMPONENT')
    CARRYABLE: 'CommonComponentType' = _get_component_type('CARRYABLE_COMPONENT')
    CARRYING: 'CommonComponentType' = _get_component_type('CARRYING_COMPONENT')
    CHANNEL: 'CommonComponentType' = _get_component_type('CHANNEL_COMPONENT')
    CENSOR_GRID: 'CommonComponentType' = _get_component_type('CENSOR_GRID_COMPONENT')
    COLLECTABLE: 'CommonComponentType' = _get_component_type('COLLECTABLE_COMPONENT')
    CONSUMABLE: 'CommonComponentType' = _get_component_type('CONSUMABLE_COMPONENT')
    CRAFTING: 'CommonComponentType' = _get_component_type('CRAFTING_COMPONENT')
    CRAFTING_STATION: 'CommonComponentType' = _get_component_type('CRAFTING_STATION_COMPONENT')
    CURFEW: 'CommonComponentType' = _get_component_type('CURFEW_COMPONENT')
    ENSEMBLE: 'CommonComponentType' = _get_component_type('ENSEMBLE_COMPONENT')
    ENVIRONMENT_SCORE: 'CommonComponentType' = _get_component_type('ENVIRONMENT_SCORE_COMPONENT')
    FLOWING_PUDDLE: 'CommonComponentType' = _get_component_type('FLOWING_PUDDLE_COMPONENT')
    FOCUS: 'CommonComponentType' = _get_component_type('FOCUS_COMPONENT')
    GAME: 'CommonComponentType' = _get_component_type('GAME_COMPONENT')
    GARDENING: 'CommonComponentType' = _get_component_type('GARDENING_COMPONENT')
    IDLE: 'CommonComponentType' = _get_component_type('IDLE_COMPONENT')
    INVENTORY: 'CommonComponentType' = _get_component_type('INVENTORY_COMPONENT')
    INVENTORY_ITEM: 'CommonComponentType' = _get_component_type('INVENTORY_ITEM_COMPONENT')
    LIGHTING: 'CommonComponentType' = _get_component_type('LIGHTING_COMPONENT')
    LINE_OF_SIGHT: 'CommonComponentType' = _get_component_type('LINE_OF_SIGHT_COMPONENT')
    LINKED_OBJECT: 'CommonComponentType' = _get_component_type('LINKED_OBJECT_COMPONENT')
    LIVE_DRAG_TARGET: 'CommonComponentType' = _get_component_type('LIVE_DRAG_TARGET_COMPONENT')
    MANNEQUIN: 'CommonComponentType' = _get_component_type('MANNEQUIN_COMPONENT')
    NAME: 'CommonComponentType' = _get_component_type('NAME_COMPONENT')
    NEW_OBJECT: 'CommonComponentType' = _get_component_type('NEW_OBJECT_COMPONENT')
    OBJECT_AGE: 'CommonComponentType' = _get_component_type('OBJECT_AGE_COMPONENT')
    OBJECT_RELATIONSHIP: 'CommonComponentType' = _get_component_type('OBJECT_RELATIONSHIP_COMPONENT')
    OBJECT_ROUTING: 'CommonComponentType' = _get_component_type('OBJECT_ROUTING_COMPONENT')
    OBJECT_TELEPORTATION: 'CommonComponentType' = _get_component_type('OBJECT_TELEPORTATION_COMPONENT')
    OWNABLE: 'CommonComponentType' = _get_component_type('OWNABLE_COMPONENT')
    PARENT_TO_SIM_HEAD: 'CommonComponentType' = _get_component_type('PARENT_TO_SIM_HEAD_COMPONENT')
    PORTAL: 'CommonComponentType' = _get_component_type('PORTAL_COMPONENT')
    PORTAL_ANIMATION: 'CommonComponentType' = _get_component_type('PORTAL_ANIMATION_COMPONENT')
    PORTAL_LOCKING: 'CommonComponentType' = _get_component_type('PORTAL_LOCKING_COMPONENT')
    PROXIMITY: 'CommonComponentType' = _get_component_type('PROXIMITY_COMPONENT')
    SEASON_AWARE: 'CommonComponentType' = _get_component_type('SEASON_AWARE_COMPONENT')
    SLOT: 'CommonComponentType' = _get_component_type('SLOT_COMPONENT')
    SPAWN_POINT: 'CommonComponentType' = _get_component_type('SPAWN_POINT_COMPONENT')
    SPAWNER: 'CommonComponentType' = _get_component_type('SPAWNER_COMPONENT')
    STATE: 'CommonComponentType' = _get_component_type('STATE_COMPONENT')
    STATISTIC: 'CommonComponentType' = _get_component_type('STATISTIC_COMPONENT')
    STORED_OBJECT_INFO: 'CommonComponentType' = _get_component_type('STORED_OBJECT_INFO_COMPONENT')
    STORED_SIM_INFO: 'CommonComponentType' = _get_component_type('STORED_SIM_INFO_COMPONENT')
    TIME_OF_DAY: 'CommonComponentType' = _get_component_type('TIME_OF_DAY_COMPONENT')
    TOOLTIP: 'CommonComponentType' = _get_component_type('TOOLTIP_COMPONENT')
    TOPIC: 'CommonComponentType' = _get_component_type('TOPIC_COMPONENT')
    FISHING_LOCATION: 'CommonComponentType' = _get_component_type('FISHING_LOCATION_COMPONENT')
    WAITING_LINE: 'CommonComponentType' = _get_component_type('WAITING_LINE_COMPONENT')
    DISPLAY: 'CommonComponentType' = _get_component_type('DISPLAY_COMPONENT')
    RETAIL: 'CommonComponentType' = _get_component_type('RETAIL_COMPONENT')
    STOLEN: 'CommonComponentType' = _get_component_type('STOLEN_COMPONENT')
    EXAMPLE: 'CommonComponentType' = _get_component_type('EXAMPLE_COMPONENT')
    WEATHER_AWARE: 'CommonComponentType' = _get_component_type('WEATHER_AWARE_COMPONENT')
