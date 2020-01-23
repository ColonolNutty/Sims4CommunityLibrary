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
    'pip', 'lib', 'sims4', 'google', 'native', 'shared_commands', 'ui', 'cas', 'vet', 'vfx', 'fame', 'fire',
    'pets', 'plex', 'role', 'sims', 'audio', 'audio.voice', 'bucks', 'buffs', 'carry', 'clubs',
    'whims', 'world', 'curfew', 'relics', 'retail', 'server', 'spells', 'temple', 'topics', 'traits', 'trends',
    'venues', 'balloon', 'careers', 'filters', 'fishing', 'laundry', 'objects', 'rewards', 'routing',
    'seasons', 'socials', 'weather', 'adoption', 'autonomy', 'business', 'crafting', 'delivery', 'ensemble',
    'holidays', 'notebook', 'postures', 'services', 'sickness', 'teleport', 'vehicles', 'animation', 'familiars',
    'headlines', 'narrative', 'tutorials', 'apartments', 'automation', 'households',
    'primitives', 'reputation', 'situations', 'statistics', 'aspirations', 'constraints', 'distributor',
    'performance', 'rabbit_hole', 'reservation', 'restaurants', 'achievements', 'away_actions',
    'broadcasters', 'gsi_handlers', 'interactions', 'event_testing', 'relationships',
    'tunable_utils', 'visualization', 'zone_modifier', 'call_to_action', 'celebrity_fans', 'lot_decoration',
    'drama_scheduler', 'global_policies', 'server_commands', 'story_progression', 'conditional_layers',
    'household_calendar', 'game_effect_modifier', 'household_milestones', 'open_street_director',
    'protocolbuffers', '_resourceman', 'enum', 'singletons', 'zone', 'clock', 'date_and_time', 'time_service'
]

add_module_names = False

master_doc = 'index'
autodoc_typehints = 'none'
