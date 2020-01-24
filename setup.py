from os.path import exists

from setuptools import setup

setup(
    name='sims4communitylib',
    version='v1.2.6',
    packages=['lib.xml', 'lib.xml.dom', 'lib.xml.sax', 'lib.xml.etree', 'lib.xml.parsers', 'lib.html', 'lib.http',
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
              'protocolbuffers', 'tests', 'tests.enums', 'tests.enums.enumtypes', 'tests.utils', 'compile',
              'sims4communitylib', 'sims4communitylib.enums', 'sims4communitylib.enums.types',
              'sims4communitylib.enums.enumtypes', 'sims4communitylib.utils', 'sims4communitylib.utils.cas',
              'sims4communitylib.utils.sims', 'sims4communitylib.utils.location', 'sims4communitylib.utils.resources',
              'sims4communitylib.utils.localization', 'sims4communitylib.events', 'sims4communitylib.events.sim',
              'sims4communitylib.events.sim.events', 'sims4communitylib.events.interval',
              'sims4communitylib.events.build_buy', 'sims4communitylib.events.build_buy.events',
              'sims4communitylib.events.zone_spin', 'sims4communitylib.events.zone_spin.events',
              'sims4communitylib.events.interaction', 'sims4communitylib.events.interaction.events',
              'sims4communitylib.events.zone_update', 'sims4communitylib.events.zone_update.events',
              'sims4communitylib.events.event_handling', 'sims4communitylib.classes',
              'sims4communitylib.classes.interactions', 'sims4communitylib.dialogs', 'sims4communitylib.dialogs.utils',
              'sims4communitylib.dialogs.option_dialogs', 'sims4communitylib.dialogs.option_dialogs.options',
              'sims4communitylib.dialogs.option_dialogs.options.sims',
              'sims4communitylib.dialogs.option_dialogs.options.objects', 'sims4communitylib.logging',
              'sims4communitylib.testing', 'sims4communitylib.services', 'sims4communitylib.services.interactions',
              'sims4communitylib.exceptions', 'sims4communitylib.mod_support', 'sims4communitylib.conditionals',
              'sims4communitylib.notifications'],
    package_dir={'': 'EA/base'},
    url='https://github.com/ColonolNutty/Sims4CommunityLibrary/',
    license='https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode',
    author='ColonolNutty',
    author_email='',
    description='An open source library with a focus on providing utilities and services to the larger Sims 4 modding community. Let\'s not reinvent the wheel! ',
    long_description=(open('README.md').read() if exists('README.md') else ''),
    extras_require={
          'docs': [
              'sphinx',
              'sphinx-autopackagesummary',
              'sphinx_rtd_theme'
          ]
      },
)
