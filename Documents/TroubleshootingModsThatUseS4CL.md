# General Troubleshooting Steps:

The following are a few steps used to troubleshoot Mods that use The Sims 4 Community Library (or even ones that don't). Depending on how a Mod has been setup, these troubleshooting steps may or may not work for you!

**These steps may also be used to track down rogue mods causing issues as well! (Even if unrelated to S4CL itself)**

## Step One:
- Ensure you have the Custom Scripts option enabled in-game in the settings
  1. At the Main Menu Press `Esc`
  2. Open `Game Options`
  3. Open `Other Settings`
  4. Make sure the `Enable Custom Content and Mods` option is checked.
    - If it was not checked, restart your game.
- If you get a corrupted file error while unzipping, update the version of your 7-zip and start over
- Verify, that you have fulfilled **all of the requirements** and their **specific versions** for the Mod being troubleshooted.
  - It should be obvious, but if a Mod has directed you to these Troubleshooting Steps, ensure you have installed [S4CL](https://github.com/ColonolNutty/Sims4CommunityLibrary/releases).
- Verify, that you have completed all of the steps in the installation process (Steps for installation are likely described in the description of the Mod)
- Ensure you have not accidentally installed duplicates of the Mod you are troubleshooting.
- Ensure you have not installed duplicates of the requirements of the Mod you are troubleshooting.
- If you have done all of the above and the Mod still does not work, move to Step Two
## Step Two:
- Rename your `Documents\Electronic Arts\The Sims 4` folder to `Documents\Electronic Arts\The Sims 4.bak`
  - This will ensure Sims 4 will recreate the folder in a clean state.
  - You can always recreate your existing game by deleting the `Documents\Electronic Arts\The Sims 4` folder and renaming `Documents\Electronic Arts\The Sims 4.bak` to `Documents\Electronic Arts\The Sims 4`
- Start Sims 4 and create a simple household with an Adult, a Teen, and a Pet (Cat or Dog, if you can)
  - If you cannot create a household or cannot load The Sims 4, skip this step.
- Save and exit the game
- Download and install the Mod (and all of its requirements) you are trying to get working
- Start the game with the household you created above (or create a new one, if the previous step was skipped)
  - Does the problem persist?
    - Yes:
      - Go to the next step
    - No:
      - You have some other Mod or a bad save that is causing you problems
## Step Three:
- Add your other Mods one by one
  - Does the problem persist?
    - Yes:
      - You have found the Mod that causes things to break, report it to the author of that Mod
    - No:
      - Continue adding Mods one by one until the problem begins to appear
      - If you've run out of Mods to add, then it was probably just a fluke in the system. (Magic *sparkle* *sparkle*)

# Problem Reporting:
- Send a message in the Discord server or Post in the Support Thread of the Mod being troubleshooted the following details:
  - Provide a detailed description of the problem (Or your best guess at the time it occurred)
    - These are essentially the steps you took that led you to the problem, or a best guess of what you were doing at the time of the error.
      - Example: I clicked on the fridge to make a Sim grab a plate of leftovers, then they put it down and immediately began doing flips out of nowhere.
  - Upload the following files that are located in the `Documents\Electronic Arts\The Sims 4` folder
    - **THESE FILES ARE ABSOLUTELY REQUIRED IF YOU HAVE AN ORANGE NOTIFICATION BOX IN-GAME**
    - The `lastexception.txt (lastexception)` file
    - The `<Mod Name>_Exceptions.txt (<Mod Name>_Exceptions)` file
    - The `<Mod Name>_Messages.txt (<Mod Name>_Messages)` file (This file may not exist)
  - Information about the Sim(s) you are having problems with (Adult, Teen, Pet, etc.)
  - The current version of **all requirements** of the Mod you are troubleshooting that you have installed. ("Most Recent" or "Latest" are not valid answers)
  - Your current Sims 4 version. Look at the bottom of the Main Menu to find the version.

## Things that will *NOT* help to solve the problem you are having:
- A screenshot of the orange "error" text box you get in-game telling you there is a problem
  - This does not contain any useful information to a Mod Author. What it does tell you is where you can find the file you need to upload.
- A "prettified" exception message.
  - Most of the time the most important details are cut out from the "prettified" exceptions which makes them useless for debugging issues.
- A one line statement only containing the main message of the exception.
  - Doing this tells me nothing about _WHERE_ the problem is, it only tells me _WHAT_ the problem is. I need the full details of exceptions to properly debug issues!
- A generic statement "I has problem, fix it please!"
  - I don't know what your problem is or if it is even related to the Mod (Mod Authors are not psychiatrists or mind readers!)
- A statement such as "I had a problem with your mod, so I uninstalled it, just wanted to let you know"
  - This doesn't help anyone and is very rude, even if you didn't mean it that way!
