# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

script_paths = [
    '../Scripts/sims4communitylib'
]

sys.path.insert(0, os.path.abspath('../Scripts'))
current_index = 1
for script_path in script_paths:
    for subdir, dirs, files in os.walk(script_path):
        if '__pycache__' in subdir:
            continue
        print(subdir)
        sys.path.insert(current_index, os.path.abspath(subdir))
        current_index += 1

# -- Project information -----------------------------------------------------

project = 'sims4communitylib'
copyright = '2020, ColonolNutty'
author = 'ColonolNutty'

# The full version, including alpha/beta/rc tags
release = '1.2.6'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [

]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

autodoc_mock_imports = [
    'lib.xml', 'lib.xml.dom', 'lib.xml.sax', 'lib.xml.etree', 'lib.xml.parsers', 'lib.html', 'lib.http',
    'lib.json', 'lib.email', 'lib.email.mime', 'lib.urllib', 'lib.xmlrpc', 'lib.logging', 'lib.unittest',
    'lib.unittest.test', 'lib.unittest.test.testmock', 'lib.encodings', 'lib.importlib', 'lib.collections',
    'sims4', 'sims4.gsi', 'sims4.tuning', 'sims4.testing', 'sims4.importer', 'sims4.localization', 'google',
    'google.protobuf', 'google.protobuf.compiler', 'google.protobuf.internal', 'native', 'native.routing',
    'native.animation', 'native.performance', 'shared_commands', 'ui', 'cas', 'vet', 'vfx', 'fame', 'fire',
    'pets', 'plex', 'role', 'sims', 'sims.baby', 'sims.pets', 'sims.aging', 'sims.occult', 'sims.suntan',
    'sims.culling', 'sims.outfits', 'sims.favorites', 'sims.pregnancy', 'sims.households',
    'sims.household_utilities', 'sims.template_affordance_provider', 'audio', 'audio.voice', 'bucks', 'buffs',
    'buffs.appearance_modifier', 'carry', 'clubs', 'whims', 'world', 'curfew', 'relics', 'retail', 'server',
    'spells', 'temple', 'topics', 'traits', 'trends', 'venues', 'venues.bar_venue', 'venues.cafe_venue',
    'venues.club_venue', 'venues.pool_venue', 'venues.lounge_venue', 'venues.chalet_garden',
    'venues.karaoke_venue', 'venues.secret_lab_venue', 'venues.center_park_venue', 'balloon', 'careers',
    'careers.acting', 'careers.doctor', 'careers.school', 'careers.detective', 'careers.prep_tasks',
    'filters', 'fishing', 'laundry', 'objects', 'objects.fire', 'objects.doors', 'objects.parts',
    'objects.pools', 'objects.props', 'objects.walls', 'objects.helpers', 'objects.puddles',
    'objects.lighting', 'objects.locators', 'objects.gardening', 'objects.placement', 'objects.attractors',
    'objects.components', 'objects.components.game', 'objects.components.utils', 'objects.decorative',
    'objects.visibility', 'objects.electronics', 'rewards', 'routing', 'routing.portals', 'routing.formation',
    'routing.walkstyle', 'routing.waypoints', 'routing.path_planner', 'routing.route_events',
    'routing.object_routing', 'seasons', 'socials', 'socials.jigs', 'weather', 'adoption', 'autonomy',
    'business', 'crafting', 'delivery', 'ensemble', 'holidays', 'notebook', 'postures', 'services',
    'sickness', 'teleport', 'vehicles', 'animation', 'animation.focus', 'animation.awareness', 'familiars',
    'headlines', 'narrative', 'tutorials', 'apartments', 'apartments.situations', 'automation', 'households',
    'primitives', 'reputation', 'situations', 'situations.ambient', 'situations.bouncer',
    'situations.complex', 'situations.complex.group_dance', 'situations.visiting', 'situations.go_dancing',
    'situations.npc_hosted', 'situations.service_npcs', 'situations.service_npcs.butler',
    'situations.special_npc_situations', 'statistics', 'aspirations', 'constraints', 'distributor',
    'performance', 'rabbit_hole', 'reservation', 'restaurants', 'achievements', 'away_actions',
    'broadcasters', 'broadcasters.environment_score', 'gsi_handlers', 'interactions', 'interactions.base',
    'interactions.utils', 'interactions.cheats', 'interactions.picker', 'interactions.social',
    'interactions.social.greeting_socials', 'interactions.payment', 'event_testing', 'relationships',
    'tunable_utils', 'visualization', 'zone_modifier', 'call_to_action', 'celebrity_fans', 'lot_decoration',
    'drama_scheduler', 'global_policies', 'server_commands', 'story_progression', 'conditional_layers',
    'household_calendar', 'game_effect_modifier', 'household_milestones', 'open_street_director',
    'protocolbuffers', '_resourceman', 'enum', 'enum.Int', 'enum.IntFlags', 'singletons', 'zone', 'clock',
    'date_and_time', 'time_service'
]

add_module_names = False

master_doc = 'index'
