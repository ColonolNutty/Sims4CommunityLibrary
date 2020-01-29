Custom Interactions
==============================================

.. note::

    To add Custom Interactions to various objects and places, take a look at :class:`.CommonInteractionRegistry`

    For an example on creating a Custom Interaction, take a look at this `Custom Interaction Tutorial`_

`Interaction`
-----------------------------------------------------------------

.. autoclass:: sims4communitylib.classes.interactions.common_interaction.CommonInteraction
   :members:
   :show-inheritance:
   :exclude-members: apply_posture_state, on_reset

`Immediate Super Interaction`
-----------------------------------------------------------------------------------

.. autoclass:: sims4communitylib.classes.interactions.common_immediate_super_interaction.CommonImmediateSuperInteraction
   :members:
   :undoc-members:
   :show-inheritance:

`Mixer Interaction`
------------------------------------------------------------------------

.. autoclass:: sims4communitylib.classes.interactions.common_mixer_interaction.CommonMixerInteraction
   :members:
   :undoc-members:
   :show-inheritance:

`Social Mixer Interaction`
--------------------------------------------------------------------------------

.. autoclass:: sims4communitylib.classes.interactions.common_social_mixer_interaction.CommonSocialMixerInteraction
   :members:
   :undoc-members:
   :show-inheritance:

`Super Interaction`
------------------------------------------------------------------------

.. autoclass:: sims4communitylib.classes.interactions.common_super_interaction.CommonSuperInteraction
   :members:
   :undoc-members:
   :show-inheritance:

`Terrain Interaction`
--------------------------------------------------------------------------

An inheritable class that provides a way to create custom Terrain Interactions.

The main use for this class is to create interactions that occur when clicking on the ground.

.. autoclass:: sims4communitylib.classes.interactions.common_terrain_interaction.CommonTerrainInteraction
   :members:
   :undoc-members:

`Interaction Registration`
--------------------------------------------------------------------------

**********************
`Interaction Registry`
**********************

.. autoclass:: sims4communitylib.services.interactions.interaction_registration_service.CommonInteractionRegistry
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: on_script_object_add, on_terrain_load, on_ocean_load

********************************************
`Script Object Interaction Handler`
********************************************

.. autoclass:: sims4communitylib.services.interactions.interaction_registration_service.CommonScriptObjectInteractionHandler
   :members:
   :undoc-members:
   :show-inheritance:


.. target-notes::
   :hidden:

.. _`Custom Interaction Tutorial`: https://github.com/ColonolNutty/Sims4CommunityLibrary/wiki/Custom-Interaction-Tutorial