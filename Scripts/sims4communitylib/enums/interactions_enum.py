"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonInteractionId(CommonInt):
    """Identifiers for interactions.

    """
    INVALID: 'CommonInteractionId' = 0
    PICK_UP_SIM: 'CommonInteractionId' = 141018
    PICK_UP_SIM_REVERSED: 'CommonInteractionId' = 141925
    CARRY_PICK_UP_TO_BED: 'CommonInteractionId' = 156217
    CARRY_PICK_UP: 'CommonInteractionId' = 134423
    CARRY_PICK_UP_FROM_SEATED: 'CommonInteractionId' = 155633
    CARRY_HUG: 'CommonInteractionId' = 155721
    CARRY_HOLD_OBJECT: 'CommonInteractionId' = 13135
    CARRY_HOLD_SIM: 'CommonInteractionId' = 132170
    CALL_INTO_ARMS_PICK_UP_PET: 'CommonInteractionId' = 173668
    SIM_TO_PET_NON_TOUCHING_PICKUP_PET: 'CommonInteractionId' = 186124
    SOCIAL_MIXER_SUPER_PICK_UP_PET: 'CommonInteractionId' = 160585
    MIXER_SOCIAL_T_PETS_FRIENDLY_HOLD_UP_CARRYING_CHILD: 'CommonInteractionId' = 168236
    GO_HERE: 'CommonInteractionId' = 14410
    SUPER_INTERACTION_GO_HERE: 'CommonInteractionId' = 27242
    GUITAR_PRACTICE: 'CommonInteractionId' = 13471

    SIM_STAND: 'CommonInteractionId' = 13983
    SIM_STAND_EXCLUSIVE: 'CommonInteractionId' = 23835
    STAND_PASSIVE: 'CommonInteractionId' = 14310
    SIM_SWIM: 'CommonInteractionId' = 102325
    SIM_CHAT: 'CommonInteractionId' = 13998
    SIM_BE_AFFECTIONATE: 'CommonInteractionId' = 13991
    CAT_STAND: 'CommonInteractionId' = 120562
    CAT_STAND_PASSIVE: 'CommonInteractionId' = 120558
    DOG_STAND: 'CommonInteractionId' = 120569
    DOG_STAND_PASSIVE: 'CommonInteractionId' = 120561
    DOG_SWIM: 'CommonInteractionId' = 170682
    DOG_SWIM_PASSIVE: 'CommonInteractionId' = 174558
    FOX_STAND: 'CommonInteractionId' = 257164
    FOX_STAND_PASSIVE: 'CommonInteractionId' = 257160

    HORSE_STAND: 'CommonInteractionId' = 120430
    HORSE_STAND_PASSIVE: 'CommonInteractionId' = 120431

    # Deliver Baby
    DELIVER_BABY_CAT: 'CommonInteractionId' = 159901
    DELIVER_BABY_DOG: 'CommonInteractionId' = 159902
    BASSINET_DELIVER_BABY: 'CommonInteractionId' = 13070
    SIM_DELIVER_BABY_CREATE_BASSINET: 'CommonInteractionId' = 97294

    # Sit
    SEATING_SIT: 'CommonInteractionId' = 31564
    SEATING_SIT_TODDLER_BED: 'CommonInteractionId' = 156920
    SEATING_SIT_SINGLE: 'CommonInteractionId' = 74779
    SEATING_SIT_CTYAE: 'CommonInteractionId' = 157667
    SEATING_SIT_RESTAURANT_RALLY_ONLY: 'CommonInteractionId' = 134949
    SEATING_SIT_POST_GRAND_MEAL_WAIT_ENJOY_COMPANY: 'CommonInteractionId' = 182774
    SEATING_SIT_DIRECTOR_CHAIR: 'CommonInteractionId' = 191162
    SEATING_SIT_HAIR_MAKE_UP_CHAIR: 'CommonInteractionId' = 201508
    SIT_PASSIVE: 'CommonInteractionId' = 14244

    # Shower
    GENERIC_SHOWER: 'CommonInteractionId' = 13439
    SHOWER_TAKE_SHOWER: 'CommonInteractionId' = 13950
    SHOWER_TAKE_SHOWER_NO_PRIVACY: 'CommonInteractionId' = 110817
    SHOWER_TAKE_SHOWER_PASSIVE: 'CommonInteractionId' = 13952
    SHOWER_TAKE_SHOWER_APARTMENT_NEIGHBOR_FLIRTY: 'CommonInteractionId' = 154397
    SHOWER_TAKE_SHOWER_BRISK: 'CommonInteractionId' = 39965
    SHOWER_TAKE_SHOWER_BRISK_NO_PRIVACY: 'CommonInteractionId' = 110818
    SHOWER_TAKE_SHOWER_COLD_SHOWER: 'CommonInteractionId' = 24332
    SHOWER_TAKE_SHOWER_COLD_SHOWER_NO_PRIVACY: 'CommonInteractionId' = 110819
    SHOWER_TAKE_SHOWER_ENERGIZED: 'CommonInteractionId' = 23839
    SHOWER_TAKE_SHOWER_ENERGIZED_NO_PRIVACY: 'CommonInteractionId' = 110820
    SHOWER_TAKE_SHOWER_SING_IN_SHOWER: 'CommonInteractionId' = 141926
    SHOWER_TAKE_SHOWER_STEAMY: 'CommonInteractionId' = 39860
    SHOWER_TAKE_SHOWER_STEAMY_NO_PRIVACY: 'CommonInteractionId' = 110821
    SHOWER_TAKE_SHOWER_THOUGHTFUL: 'CommonInteractionId' = 39845
    SHOWER_TAKE_SHOWER_THOUGHTFUL_NO_PRIVACY: 'CommonInteractionId' = 110822
    SUPER_INTERACTION_CAMPING_BATHROOM_SHOWER_FEMALE: 'CommonInteractionId' = 104658
    SUPER_INTERACTION_CAMPING_BATHROOM_SHOWER_MALE: 'CommonInteractionId' = 104659
    SIM_RAIN_SHOWER: 'CommonInteractionId' = 185951
    SOCIAL_MIXER_SHOWER_SING_IN_SHOWER: 'CommonInteractionId' = 141216
    SOCIAL_MIXER_SHOWER_SING_IN_SHOWER_AUTONOMOUS: 'CommonInteractionId' = 141928

    # Bath
    GENERIC_BATH: 'CommonInteractionId' = 13427
    GENERIC_BUBBLE_BATH: 'CommonInteractionId' = 35352
    GENERIC_RELAXING_BATH: 'CommonInteractionId' = 120467
    BATHTUB_TAKE_BATH_LOOP: 'CommonInteractionId' = 13085
    BATHTUB_TAKE_BATH_RELAXING_BATH_IDLE_LOOP: 'CommonInteractionId' = 120473
    BATHTUB_TAKE_BATH_RELAXING_BATH_PLAY: 'CommonInteractionId' = 120474
    BATHTUB_TAKE_BATH_RELAXING_BATH_FALL_ASLEEP: 'CommonInteractionId' = 120475
    BATHTUB_TAKE_BATH_RELAXING_BATH_IDLE_LOOP_MUD: 'CommonInteractionId' = 121800
    BATHTUB_TAKE_BATH_RELAXING_BATH_PLAY_MUD: 'CommonInteractionId' = 121804
    BATHTUB_TAKE_BATH_RELAXING_BATH_FALL_ASLEEP_MUD: 'CommonInteractionId' = 121802
    BATHTUB_TAKE_BUBBLE_BATH_MERMAID: 'CommonInteractionId' = 213939
    BATHTUB_TAKE_BATH_MERMAID: 'CommonInteractionId' = 213938
    BATHTUB_NAP_MERMAID: 'CommonInteractionId' = 215915
    BATHTUB_PLAY_MERMAID: 'CommonInteractionId' = 215876
    IDLE_HYGIENE_MERMAID: 'CommonInteractionId' = 215764

    # S4CL
    S4CL_DEBUG_SHOW_RUNNING_AND_QUEUED_INTERACTIONS: 'CommonInteractionId' = 5900237111545222349
    S4CL_DEBUG_SHOW_ACTIVE_BUFFS: 'CommonInteractionId' = 12481803320243318715
    S4CL_DEBUG_SHOW_TRAITS: 'CommonInteractionId' = 2108116777929577381
    S4CL_DEBUG_SHOW_RUNNING_SITUATIONS: 'CommonInteractionId' = 10355438442708473961
    S4CL_DEBUG_LOG_ALL_INTERACTIONS: 'CommonInteractionId' = 741312864308659038
    S4CL_DEBUG_LOG_ALL_INTERACTIONS_PHONE: 'CommonInteractionId' = 2534976194662328318
    S4CL_DEBUG_INDUCE_LABOR: 'CommonInteractionId' = 5145499017874001819
    S4CL_DEBUG_OBJECT_BREAK: 'CommonInteractionId' = 14420264135453255013
    S4CL_DEBUG_OBJECT_FIX: 'CommonInteractionId' = 11726582335911165817
    S4CL_DEBUG_OBJECT_MAKE_DIRTY: 'CommonInteractionId' = 1799349573117453079
    S4CL_DEBUG_OBJECT_MAKE_CLEAN: 'CommonInteractionId' = 5335871574274933500
    S4CL_DEBUG_LOG_ALL_GAME_TAGS: 'CommonInteractionId' = 13483495329565765760
    S4CL_DEBUG_CHANGE_OBJECT_STATES: 'CommonInteractionId' = 15058010603771996272

    S4CL_SOCIAL_SUPER_SIM_TO_PET_HUMAN: 'CommonInteractionId' = 17045599576038631962
    S4CL_SOCIAL_SUPER_SIM_TO_PET_PET: 'CommonInteractionId' = 17048453908224900188

    S4CL_SOCIAL_SUPER_SIM_TO_FOX_HUMAN: 'CommonInteractionId' = 0xCC4FDF3D68E78F5E
    S4CL_SOCIAL_SUPER_SIM_TO_FOX_FOX: 'CommonInteractionId' = 0xCC2B053D68C8B3F0

    SHOWER_TAKE_SHOWER_WALL_PRIVACY_CHILD_TEEN = 224187
    GENERIC_TOILET_SIT_STALL = 213986

    # bar_OrderDrink
    BAR_ORDER_DRINK = 13050
    # bar_PushOrderDrink_Autonomous
    BAR_ORDER_DRINK_AUTONOMOUS = 13053
    # bar_Order_Food
    BAR_ORDER_FOOD = 178213

    # bar_WaitForDrink
    BAR_WAIT_FOR_DRINK = 13065
    # bar_WaitFor_Food
    BAR_WAIT_FOR_FOOD = 178214
    # bar_WaitForFood_CriticCareer
    BAR_WAIT_FOR_FOOD_CRITIC = 137790

    TOGGLE_PHONE_SILENCE = 40130  # toggle_phone_silence
