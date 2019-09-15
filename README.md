Welcome to The Sims 4 Community Library!

This is more of an API than a mod itself. It does nothing on its own and is meant as a framework for other Sims 4 developers to utilize in their own code bases.



Current Features:

- Access to Vanilla Tuning identifiers for
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
 - Enable/Disable logs via a command in-game.
 - `s4clib.enable_log <log_name>`
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
 - Ok/Cancel - The Player can choose either Ok or Cancel
   - The text for both the Ok and the Cancel buttons can be custom text as well.
- Custom Notifications
 - Basic Notification - Display a notification with a title and description of varying urgency.
- Interactions
  - Registration
  - Register Interactions to:
    - Terrain
    - Ocean
    - Objects (Sims, Furniture, etc.)
- Utilities
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
  - Sims - Get all nearby sims and filter which types of sims to get (Age, Species, Occult, Traits, Buffs, Statistics, Motive Levels)
  - Club - Detect sims that are part of a club, whether they are at a club gathering, whether their club encourages or discourages certain things
  - CAS Parts Modification (Functions to equip/unequip or list cas parts, etc.)
  - Buff Management (Detect buffs currently on sims, or add your own)
  - Trait Management (Detect traits currently on sims or add your own)
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
    - The ability to formulate a window that could contain settings or a list of items.
    - Prompt users to input Numbers/Text
    - Prompt the user to select from a list of items.
  - Sim Picker - Have the player choose a sim or a number of sims.
  - Object Picker - Have the player choose from a list of items.


Installation:

- Download the zip archive from the download link
- Unpack the archive using your favorite archiving tool.
- Drag the files/folders to your Mods directory.
- Keep in mind the ts4script file MUST be either top level (Directly in the Mods/<ts4script file> folder) or one folder deep (Mods/Blah/<ts4script file>). Any deeper and it will not work.


Requirements:

- Sims 4 version 1.54.120.1020 (Island Living) or above


Note for Modders:

- If you have ideas for additions to add or want one of the planned features sooner rather than later, I'm all ears! Let's work together to create a library that we all can use!

