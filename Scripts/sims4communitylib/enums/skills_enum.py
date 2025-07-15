"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from sims4communitylib.enums.enumtypes.common_int import CommonInt


class CommonSkillId(CommonInt):
    """Identifiers for sim skills.

    """
    INVALID: 'CommonSkillId' = 0
    ACTING: 'CommonSkillId' = 194727
    APOTHECARY: 'CommonSkillId' = 439222
    ARCHAEOLOGY: 'CommonSkillId' = 174237
    BAKING: 'CommonSkillId' = 104198
    BOWLING: 'CommonSkillId' = 158659
    CHARISMA: 'CommonSkillId' = 16699
    COMEDY: 'CommonSkillId' = 16698
    COMMUNICATION: 'CommonSkillId' = 140170
    COOKING: 'CommonSkillId' = 16705
    CREATIVITY: 'CommonSkillId' = 16718
    CROSS_STITCH: 'CommonSkillId' = 259758
    DANCING: 'CommonSkillId' = 128145
    DJ_MIXING: 'CommonSkillId' = 121612
    ENTREPRENEUR: 'CommonSkillId' = 274197
    EQUESTRIAN_SKILL: 'CommonSkillId' = 322708
    FABRICATION: 'CommonSkillId' = 231908
    FISHING: 'CommonSkillId' = 39397
    FITNESS: 'CommonSkillId' = 16659
    FLOWER_ARRANGING: 'CommonSkillId' = 186703
    GARDENING: 'CommonSkillId' = 16700
    GEMOLOGY: 'CommonSkillId' = 350972
    GOURMET_COOKING: 'CommonSkillId' = 16701
    GUITAR: 'CommonSkillId' = 16702
    HANDINESS: 'CommonSkillId' = 16704
    HERBALISM: 'CommonSkillId' = 101920
    HORSE_AGILITY: 'CommonSkillId' = 324632
    HORSE_ENDURANCE: 'CommonSkillId' = 324634
    HORSE_JUMPING: 'CommonSkillId' = 324633
    HORSE_TEMPERAMENT: 'CommonSkillId' = 324631
    HUMANOID_ROBOT_ENHANCEMENT: 'CommonSkillId' = 224672
    IMAGINATION: 'CommonSkillId' = 140706
    INFANT_CRAWL_HIDDEN: 'CommonSkillId' = 297187
    INFANT_MILESTONE_FINE_MOTOR_HIDDEN: 'CommonSkillId' = 273725
    INFANT_MILESTONE_GROSS_MOTOR_HIDDEN: 'CommonSkillId' = 273723
    INFANT_MILESTONE_SOCIAL_HIDDEN: 'CommonSkillId' = 273726
    INFANT_SOCIAL_AGE_UP_HIDDEN: 'CommonSkillId' = 324352
    JUICE_FIZZING: 'CommonSkillId' = 234806
    JUICE_PONG: 'CommonSkillId' = 213548
    KNITTING: 'CommonSkillId' = 239521
    LOGIC: 'CommonSkillId' = 16706
    MAINTENANCE: 'CommonSkillId' = 111904
    MEDIA_PRODUCTION: 'CommonSkillId' = 192655
    MEDIUM: 'CommonSkillId' = 255249
    MENTAL: 'CommonSkillId' = 16719
    MISCHIEF: 'CommonSkillId' = 16707
    MIXOLOGY: 'CommonSkillId' = 16695
    MOTOR: 'CommonSkillId' = 16720
    MOVEMENT: 'CommonSkillId' = 136140
    NATURAL_LIVING: 'CommonSkillId' = 434909
    PAINTING: 'CommonSkillId' = 16708
    PARENTING: 'CommonSkillId' = 160504
    PET_TRAINING: 'CommonSkillId' = 161220
    PHOTOGRAPHY: 'CommonSkillId' = 105774
    PIANO: 'CommonSkillId' = 16709
    PING_PONG: 'CommonSkillId' = 212561
    PIPE_ORGAN: 'CommonSkillId' = 149665
    POTTERY: 'CommonSkillId' = 371129
    POTTY: 'CommonSkillId' = 144913
    PROGRAMMING: 'CommonSkillId' = 16703
    RANCH_NECTAR: 'CommonSkillId' = 315761
    RESEARCH_AND_DEBATE: 'CommonSkillId' = 221014
    ROBOTICS: 'CommonSkillId' = 217413
    ROCKET_SCIENCE: 'CommonSkillId' = 16710
    ROCK_CLIMBING: 'CommonSkillId' = 245639
    ROCK_CLIMBING_HIDDEN: 'CommonSkillId' = 165900
    ROMANCE: 'CommonSkillId' = 368684
    SALES: 'CommonSkillId' = 111902
    SELVADORADIAN_CULTURE: 'CommonSkillId' = 174687
    SHELL_TUTOR_PICKED_SKILL_HIDDEN: 'CommonSkillId' = 224628
    SINGING: 'CommonSkillId' = 137811
    SKATING_HIDDEN: 'CommonSkillId' = 179925
    SKIING: 'CommonSkillId' = 245613
    SNOWBOARDING: 'CommonSkillId' = 246054
    SOCIAL: 'CommonSkillId' = 16721
    TATTOOING: 'CommonSkillId' = 371481
    THANATOLOGY: 'CommonSkillId' = 380495
    THINKING: 'CommonSkillId' = 140504
    VAMPIRE_LORE_HIDDEN: 'CommonSkillId' = 149556
    VETERINARIAN: 'CommonSkillId' = 161190
    VIDEO_GAMING: 'CommonSkillId' = 16712
    VIOLIN: 'CommonSkillId' = 16713
    WELLNESS: 'CommonSkillId' = 117858
    WORK_ETHIC: 'CommonSkillId' = 111903
    WRITING: 'CommonSkillId' = 16714

    # All of the following values are obsolete, please use the above values instead!
    ADULT_MAJOR_ACTING: 'CommonSkillId' = ACTING
    ADULT_MAJOR_ARCHAEOLOGY: 'CommonSkillId' = ARCHAEOLOGY
    ADULT_MAJOR_BAKING: 'CommonSkillId' = BAKING
    ADULT_MAJOR_BAR_TENDING: 'CommonSkillId' = MIXOLOGY
    ADULT_MAJOR_CHARISMA: 'CommonSkillId' = CHARISMA
    ADULT_MAJOR_COMEDY: 'CommonSkillId' = COMEDY
    ADULT_MAJOR_DJ_MIXING: 'CommonSkillId' = DJ_MIXING
    ADULT_MAJOR_FABRICATION: 'CommonSkillId' = FABRICATION
    ADULT_MAJOR_FISHING: 'CommonSkillId' = FISHING
    ADULT_MAJOR_FLOWER_ARRANGING: 'CommonSkillId' = FLOWER_ARRANGING
    ADULT_MAJOR_GARDENING: 'CommonSkillId' = GARDENING
    ADULT_MAJOR_GOURMET_COOKING: 'CommonSkillId' = GOURMET_COOKING
    ADULT_MAJOR_GUITAR: 'CommonSkillId' = GUITAR
    ADULT_MAJOR_HANDINESS: 'CommonSkillId' = HANDINESS
    ADULT_MAJOR_HERBALISM: 'CommonSkillId' = HERBALISM
    ADULT_MAJOR_HOME_STYLE_COOKING: 'CommonSkillId' = COOKING
    ADULT_MAJOR_LOGIC: 'CommonSkillId' = LOGIC
    ADULT_MAJOR_MISCHIEF: 'CommonSkillId' = MISCHIEF
    ADULT_MAJOR_PAINTING: 'CommonSkillId' = PAINTING
    ADULT_MAJOR_PARENTING: 'CommonSkillId' = PARENTING
    ADULT_MAJOR_PHOTOGRAPHY: 'CommonSkillId' = PHOTOGRAPHY
    ADULT_MAJOR_PIANO: 'CommonSkillId' = PIANO
    ADULT_MAJOR_PIPE_ORGAN: 'CommonSkillId' = PIPE_ORGAN
    ADULT_MAJOR_PROGRAMMING: 'CommonSkillId' = PROGRAMMING
    ADULT_MAJOR_ROCKET_SCIENCE: 'CommonSkillId' = ROCKET_SCIENCE
    ADULT_MAJOR_SINGING: 'CommonSkillId' = SINGING
    ADULT_MAJOR_VETERINARIAN: 'CommonSkillId' = VETERINARIAN
    ADULT_MAJOR_VIDEO_GAMING: 'CommonSkillId' = VIDEO_GAMING
    ADULT_MAJOR_VIOLIN: 'CommonSkillId' = VIOLIN
    ADULT_MAJOR_WELLNESS: 'CommonSkillId' = WELLNESS
    ADULT_MAJOR_WRITING: 'CommonSkillId' = WRITING
    ADULT_MINOR_DANCING: 'CommonSkillId' = DANCING
    ADULT_MINOR_JUICE_FIZZING: 'CommonSkillId' = JUICE_FIZZING
    ADULT_MINOR_LOCAL_CULTURE: 'CommonSkillId' = SELVADORADIAN_CULTURE
    ADULT_MINOR_MEDIA_PRODUCTION: 'CommonSkillId' = MEDIA_PRODUCTION
    CHILD_CREATIVITY: 'CommonSkillId' = CREATIVITY
    CHILD_MENTAL: 'CommonSkillId' = MENTAL
    CHILD_MOTOR: 'CommonSkillId' = MOTOR
    CHILD_SOCIAL: 'CommonSkillId' = SOCIAL
    CHOPSTICKS: 'CommonSkillId' = 142593
    DARTBOARD_DARTS: 'CommonSkillId' = 127868
    DOG_TRAINING: 'CommonSkillId' = PET_TRAINING
    FOOSBALL: 'CommonSkillId' = 122854
    SKATING = SKATING_HIDDEN
    HIDDEN_SKATING: 'CommonSkillId' = SKATING_HIDDEN
    HIDDEN_TREAD_MILL_ROCK_CLIMBING_WALL_CLIMB: 'CommonSkillId' = ROCK_CLIMBING_HIDDEN
    HIDDEN_VAMPIRE_LORE: 'CommonSkillId' = VAMPIRE_LORE_HIDDEN
    OBJECT_UPGRADE_COMPUTER_GAMING: 'CommonSkillId' = 29027
    PET_POOP_CLEAN_UP: 'CommonSkillId' = 161097
    RETAIL_MAINTENANCE: 'CommonSkillId' = MAINTENANCE
    RETAIL_SALES: 'CommonSkillId' = SALES
    RETAIL_WORK_ETHIC: 'CommonSkillId' = WORK_ETHIC
    THROWING_THINGS: 'CommonSkillId' = DARTBOARD_DARTS
    TODDLER_COMMUNICATION: 'CommonSkillId' = COMMUNICATION
    TODDLER_IMAGINATION: 'CommonSkillId' = IMAGINATION
    TODDLER_MOVEMENT: 'CommonSkillId' = MOVEMENT
    TODDLER_POTTY: 'CommonSkillId' = POTTY
    TODDLER_THINKING: 'CommonSkillId' = THINKING
    VAMPIRE_LORE = VAMPIRE_LORE_HIDDEN
