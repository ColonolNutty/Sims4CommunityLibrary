# Welcome to The Sims 4 Community Library!

This is more of an API than a mod itself. It does nothing on its own and is meant as a framework for other Sims 4 developers to utilize in their own code bases.

To see the documentation for S4CL [check out the docs](https://sims4communitylibrary.readthedocs.io/en/latest/)!

To start creating mods using S4CL [check out the template project](https://github.com/ColonolNutty/s4cl-template-project)!

## Looking to install S4CL?
Follow the installation instructions below for details. 

### Current Features:

- Access to Vanilla Tuning identifiers for:
  - Buffs
  - Interactions
  - Relationship Bits
  - Relationship Tracks
  - Short-Term Relationship Bits
  - Motives
  - Moods
  - Lot Traits
  - Sim Traits
  - Situations
  - Situation Jobs
  - Many Others!
- Logging
  - Log messages to a file
  - Log custom exceptions
  - Log the current stack trace, find out who or what is calling your functions!
  - Useful when debugging code!
    - Enable/Disable logs via a command in-game. `s4clib.enable_log�<log_name>`
- Exception Handling
  - Log to a file exceptions that are thrown
  - Catch exceptions within your functions via a decorator
- Custom Enums
  - Create your own custom Enums
  - Four types of Enums (More will be added if requested)
    - Int
    - String
    - Float
    - Object
- Custom Dialogs
  - Ok/Cancel - Prompt the player with a message and have them choose either Ok or Cancel
    - The text for both the Ok and the Cancel buttons can be custom text as well. (They could be Yes/No as one custom example)
  - Choose Object Dialog 
    - Prompt the player to choose an object from a list of items.
    - Custom icons can be used.
  - Custom Icons available for use with dialogs.
    - Right Arrow
    - Navigate Into Arrow
    - Question Mark
    - Six Sided Dice
    - Checked Box
    - Unchecked Box
  - Notifications
    - Sim Icons
    - Warnings
    - Errors
    - Info
  - Story Dialogs (Add custom buttons, add sim icons)
  - Sim Picker
    - Prompt the player to choose a sim or a number of sims from a dialog.
- Custom Notifications
  - Basic Notification - Display a notification with a title and description of varying urgency.
- Interactions
  - Registration
  - Register Interactions to:
    - Terrain
    - Ocean
    - Objects (Sims, Furniture, etc.)
  - Custom Interactions
    - Create interactions the run Python code in their backends
    - Interaction Types:
      - CommonInteraction - Inherit from this to hook into an interaction and add python functionality to its functions
      - Immediate Super Interaction - An interaction that doesn't require a target to perform. It is started immediately and without an animation.
      - Super Interaction - Like the Immediate Super interaction but these require a target to perform. (sim_chat is one example of a Super Interaction)
      - Mixer Interaction - Use this for custom Mixer interactions.
      - Social Mixer Interaction - Use this for custom Social Mixer interactions.
      - Terrain Interaction - Use for interactions that appear when clicking on the ground.
    - Perform logical checks to determine whether or not to show an interaction
      - Or display an interaction as disabled, with a displayed tooltip that shows when the player hovers the interaction.
    - Run Python code when an interaction is started, cancelled, or has finished.
    - Custom Interaction Tooltips
      - Display tooltips on interactions that display on hover.
      - Locate CommonInteraction for an example of how to utilize custom tooltips in your own interactions.
- Event Handling
  - Create, Dispatch, and Handle Dynamic Events
    - Handle events without needing a reference to the code that sends the event.
    - Decouple that code!
  - Interval Events
    - Run functions on millisecond intervals.
    - Run functions once, after an amount of time has passed.
  - Interaction events (Queued, Started, Ended, Interaction Outcomes)
  - Sim
    - Spawn - Occurs when a Sim spawns or is born into the world.
    - Initialization - Occurs when a Sim is initialized (before being spawned).
    - Occult Swapping - Occurs when a Sim changes to a different Occult (i.e. Human to Mermaid or Human to Vampire or vice verse)
  - Zone Events
    - Zone Update - Occurs every time the zone updates. (Basically every time the game ticks)
    - Zone Teardown - Occurs every time the zone is torn down. Occurs before a loading screen, but only after a Zone had been previously loaded. (See Zone Early/Late Load)
    - Zone Save - Occurs every time a zone is saved. This occurs before the game saves for the player. Be careful with this one!
    - Zone Early Load - Occurs when a zone is loaded, but before the players household has loaded.
    - Zone Late Load - Occurs when a zone is loaded, but after the players household has loaded.
- Utilities
  - Sim utilities
    - Get the Active Sim
    - Get Sim Info, Sim Instance, and Sim Ids
    - Get All Sims nearby and�filter which types of sims to get�(Age, Species, Occult, Traits, Buffs, etc.)
    - Occults - Check Occult Types of sims.
    - Ages - Get/Set/Check Ages of sims.
    - Genders - Get/Set/Check Genders of sims.
    - Species - Get/Set/Check Species of sims.
    - Buffs - Add/Remove/Check Buffs of sims.
    - Traits - Add/Remove/Check Traits of sims.
    - Sim State - Check various states of sims. (Wearing towel, Dying, etc.)
  - CAS
    - Outfit - Set/Get/Update/Check the current outfit of sims.
    - CAS Utils - Attach/Detach/Check cas parts of a sims outfit. You can put any cas part in any BodyType via these.
  - Components - Get various components of objects (Statistics, Traits, Buffs, etc.)
  - Resources - Load Resources or Tuning files by their identifiers. (Buffs, Traits, Statistics, Snippets, etc.)
  - Icons - Load Icons provided by S4CL or your own Icons.
  - Types - Determine the type of objects without needing to use isinstance or having a reference to the type itself in your own code.
  - Time - Manage time. Pause the game, get/change the current game speed, get/set the time of day, etc.
  - Collections - Determine if an object is a collection, combine collections, flatten collections, etc.
  - Injection - Inject custom functionality into functions
  - IO (Input/Output) - Write string data to a file or load string data from a file.
  - Stack Trace�- Retrieve the�complete and full stack trace.
  - Localization utilities
    - Retrieve LocalizedStrings from StringTables of .package files.
    - Format tokens into LocalizedStrings
    - Display text�in�specific colors (Colors can be added by request)
      - Blue
      - Green
      - Red
    - Create Localized Tooltips - Use to display tooltips on interactions (while also displaying the interaction)
      - These can be useful to give more information to the player about why something cannot be performed, instead of simply hiding that something.
  - Weather
    - Detect and change weather conditions
  - Statistic Management
    - Manage statistics such as motives, mood, etc.
  - Motive Management
    - Change motive levels and moods of sims
  - and Many More, explore to your hearts content!
- Testing Framework
  - Write tests to test your python code and run the tests via a command within the game.
  - The results will be logged to the 'Documents/The Sims 4/'�folder
  - A single function can handle multiple tests utilizing the same code with different arguments.
  - Run tests via the command: `s4clib.run_tests <class_names_separated_by_a_space>`
  - Class Names are the names of the classes decorated with 'test_class'
  - If no class names are provided, all of the tests will run.


### Installation:

- Download the latest zip archive from the [releases](https://github.com/ColonolNutty/Sims4CommunityLibrary/releases) page (It is the one with the version number in it Example: sims4communitylib.v0.0.0.zip) (Ignore the ones that say Source Code)
- Unpack the archive using your favorite archiving tool.
- Drag the files/folders to your Mods directory.
- Keep in mind the ts4script file MUST be either top level (Directly in the Mods/<ts4script file>�folder) or one folder deep (Mods/Blah/<ts4script file>). Any deeper and it will not work.
- Keep the `sims4communitylib.ts4script` and `sims4communitylib.config` files together!


### Requirements:

- Sims 4 Patch Version 1.90.358.1030 (Up to the High School Years patch, the High School Years DLC is not required) or above
- DLCs are NOT required, you only need to have an up to date game (Check the bottom of the main menu for your current version).

### Planned Features:

- Many more functions, utilities, and�services to make coding for the sims 4 much easier. You won't need to reinvent the wheel anymore!
- Exception Handling (stack trace customization)
- Services & Utilities:
  - Weather - Change weather conditions
  - Club - Detect sims that are part of a club, whether they are at a club gathering, whether their club encourages or discourages certain things
- Custom Enum Types
  - Bitwise (Support for bitwise operations on custom enums)
- Notifications
  - Notifications with Buttons.
- Custom Dialogs
  - Prompt the player to input Numbers/Text


### Note for Modders:

- If you have ideas for additions to add or want one of the planned features sooner rather than later, I'm all ears! Let's work together to create a library that we all can use!
- To see the documentation for S4CL [check out the docs](https://sims4communitylibrary.readthedocs.io/en/latest/)!


### What is the workflow for working with S4CL?
- Create a project based off of the [Template Project](https://github.com/ColonolNutty/s4cl-template-project)
- Use the green button in the top right [The Main Page](https://github.com/ColonolNutty/Sims4CommunityLibrary) to download this project as a zip file.
- In your project, create another directory called `S4CL`.
- Open the downloaded project and copy the `Scripts/sims4communitylib` folder into the `S4CL` folder we created in the previous step. The folder structure should then be: `<Your Project>/S4CL/sims4communitylib`
- Right click the `S4CL` folder -> Mark Directory as -> Sources Root
  - The `S4CL` folder should turn a blue color and the `sims4communitylib` folder should look like a folder with a dot (In other words, it should NOT be blue).
- Your folder structure should look like this: `<Your Project>/S4CL/sims4communitylib` at this point.
- Ensure you list in the description of your mod a link to the github releases (You may even link a specific release to ensure compatibility.)
- Ensure you properly attribute S4CL and its author according to the license located at the bottom of this readme.
- In order to prevent users from accidentally installing multiple copies of S4CL into their Mods folder, it is preferred to redirect the users of your mod to download S4CL from either the [github repository](https://github.com/ColonolNutty/Sims4CommunityLibrary) or [releases](https://github.com/ColonolNutty/Sims4CommunityLibrary/releases) pages instead of bundling it with your mod.

### Copyright:

The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY