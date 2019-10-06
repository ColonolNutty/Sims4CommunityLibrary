Welcome to The Sims 4 Community Library!

This is more of an API than a mod itself. It does nothing on its own and is meant as a framework for other Sims 4 developers to utilize in their own code bases.



Current Features:

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
    - Enable/Disable logs via a command in-game. `s4clib.enable_log <log_name>`
- Exception Handling
  - Log to a file exceptions that are thrown
  - Catch exceptions within your functions via a decorator
- Custom Enums
  - Create your own custom Enums (Because The Sims 4 is silly and decided to override the enum module, doh!)
  - Four types of Enums (More will be added if requested)
    - Int
    - String
    - Float
    - Object
- Custom Dialogs
  - Ok/Cancel - Prompt the player with a message and have them choose either Ok or Cancel
    - The text for both the Ok and the Cancel buttons can be custom text as well. (They could be Yes/No as one custom example)
  - Choose Item Dialog 
    - Prompt the player to choose an item from a list of items.
    - Custom icons can be used.
    - A possible use of this could be to display settings of some kind.
  - Custom Icons available for use with dialogs.
    - Right Arrow
    - Navigate Into Arrow
    - Question Mark
    - Six Sided Dice
    - Checked Box
    - Unchecked Box
- Custom Notifications
  - Basic Notification - Display a notification with a title and description of varying urgency.
- Interactions
  - Registration
  - Register Interactions to:
    - Terrain
    - Ocean
    - Objects (Sims, Furniture, etc.)
  - Custom Interactions
    - Create interactions to perform custom functionality
    - Interaction Types:
      - Immediate Super Interaction - An interaction that doesn't require a target to perform. It is started immediately and without an animation.
      - Super Interaction - Like the Immediate Super interaction but these require a target to perform. (sim_Chat is one example of a Super Interaction)
      - Mixer Interaction - Use this for custom Mixer interactions.
      - Social Mixer Interaction - Use this for custom Social Mixer interactions.
      - Terrain Interaction - Use for interactions that appear when clicking on the ground.
    - Perform logical checks to determine whether or not to show an interaction
      - Or display an interaction as disabled, with a displayed tooltip that shows when the player hovers the interaction.
    - Run Python code when an interaction is started, cancelled, or has finished.
    - Custom Interaction Tooltips
      - Display tooltips on interactions that display on hover.
      - Locate CommonInteraction for an example of how to utilize custom tooltips in your own interactions.
- Utilities
  - Sim utilities
    - Get the Active Sim
    - Get Sim Info, Sim Instance, and Sim Ids
    - Get All Sims nearby and filter which types of sims to get (Age, Species, Occult, Traits, Buffs, etc.)
    - Occults - Check Occult Types of sims.
    - Ages - Get/Set/Check Ages of sims.
    - Genders - Get/Set/Check Genders of sims.
    - Species - Get/Set/Check Species of sims.
    - Buffs - Add/Remove/Check Buffs of sims.
    - Traits - Add/Remove/Check Traits of sims.
    - Sim State - Check various states of sims. (Wearing towel, Dying, etc.)
  - CAS
    - Outfit - Set/Get/Update/Check the current outfit of sims.
  - Components - Get various components of objects (Statistics, Traits, Buffs, etc.)
  - Resources - Load Resources or Tuning files by their identifiers. (Buffs, Traits, Statistics, Snippets, etc.)
  - Type utilities - Determine the type of objects without needing to use isinstance or having a reference to the type itself in your own code.
  - Time - Manage time. Pause the game, get/change the current game speed, get/set the time of day, etc.
  - Collection utilities - Determine if an object is a collection, combine collections, flatten collections, etc.
  - Injection - Inject custom functionality into functions
  - IO (Input/Output) - Write string data to a file or load string data from a file.
  - Stack Trace - Retrieve the complete and full stack trace.
  - Localization utilities
    - Retrieve LocalizedStrings from StringTables of .package files.
    - Format tokens into LocalizedStrings
    - Display text in specific colors (Colors can be added by request)
      - Blue
      - Green
      - Red
    - Create Localized Tooltips - Use to display tooltips on interactions (while also displaying the interaction)
      - These can be useful to give more information to the player about why an interaction cannot be performed, instead of simply hiding interactions.
- Testing Framework
  - Write tests to test your python code and run the tests via a command within the game.
  - The results will be logged to the 'Documents/The Sims 4/' folder
  - A single function can handle multiple tests utilizing the same code with different arguments.
  - Run tests via the command: `s4clib.run_tests <class_names_separated_by_a_space>`
  - Class Names are the names of the classes decorated with 'test_class'
  - If no class names are provided, all of the tests will run.

Planned Features:

- Many functions, utilities, and services to make coding for the sims 4 much easier. You won't need to reinvent the wheel anymore!
- Exception Handling (stack trace customization)
- Services & Utilities:
  - Weather - Detect and change weather conditions
  - Club - Detect sims that are part of a club, whether they are at a club gathering, whether their club encourages or discourages certain things
  - CAS Parts Modification (Functions to equip/unequip or list cas parts, etc.)
  - Statistic Management (Manage statistics such as motives, mood, etc.)
  - Motive Management (Change motive levels and moods of sims)
- Event handling
  - Interaction events (Queued, Started, Ended, Interaction Outcomes)
  - Game Tick - Register functions to run when the game updates and how often to run.
  - Zone Updates - Update, Teardown, Zone Load. Detect when the game has finished loading in to a household
  - Sim - (Spawn, Initialization, Occult Swapping)
- Custom Enum Types
  - Collections (Tuple, List)
  - Bitwise (Support for bitwise operations on custom enums)
- Dialogs and Notifications
  - Notifications
    - Sim Icons
    - Warnings
    - Errors
    - Info
    - Notifications with Custom Buttons.
  - Story Dialogs (Add custom buttons, add sim icons)
  - Custom Dialog Boxes
    - Prompt users to input Numbers/Text
    - Prompt the user to select from a list of items.
  - Sim Picker - Prompt the player to choose a sim or a number of sims from a dialog.


Installation:

- Download the zip archive from the download link
- Unpack the archive using your favorite archiving tool.
- Drag the files/folders to your Mods directory.
- Keep in mind the ts4script file MUST be either top level (Directly in the Mods/<ts4script file> folder) or one folder deep (Mods/Blah/<ts4script file>). Any deeper and it will not work.


Requirements:

- Sims 4 version 1.54.120.1020 (Island Living) or above


Note for Modders:

- If you have ideas for additions to add or want one of the planned features sooner rather than later, I'm all ears! Let's work together to create a library that we all can use!


What is the workflow for working with S4CL?
- Simply copy the source folder Scripts/sims4communitylibrary into your own PyCharm project.
- Right click the copied folder -> Mark Directory as -> Sources Root
- Once you've done this you just have to import sims4communitylibrary as you would with any other python files
- Ensure you list in the description of your mod a link to the github releases (You may even link a specific release to ensure compatibility.)
- YOU DO NOT HAVE MY PERMISSION TO INCLUDE S4CL IN YOUR OWN MOD. So don't do it.

Copyright:

The Sims 4 Community Library is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) COLONOLNUTTY