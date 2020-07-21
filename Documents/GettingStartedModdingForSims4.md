# Python:

All of the tools and installation instructions you will need to know for getting setup with Python can be found from here:

[Getting Started with Python Scripting](http://sims4studio.com/thread/15145/started-python-scripting)

If the link above does not work, these are the Tools you will need:
- [Python 3.7](https://www.python.org/downloads/release/python-370/)
  - _Sims 4 uses Python 3.7 specifically_
  - Download and install Python into a folder you will remember, with no spaces in the entire path
    - example path: `C:\Python37\`
- [PyCharm (Community Edition)](https://www.jetbrains.com/pycharm/download/#section=windows)
  - _Any version will work, even the latest!_
- [Git](https://git-scm.com/downloads)
  - _This will be used for cloning GitHub repositories_
- Alternative to Git, you can download the source files from [the latest release](https://github.com/ColonolNutty/Sims4CommunityLibrary/releases).
  

# Package Files:

Tools you will need:
- [Sims 4 Studio](http://sims4studio.com/board/6/download-sims-studio-open-version)
  - _Download the version that matches your operating system._

## How to use Sims 4 Studio:
- Open The Sims 4 Studio and enter a Creator Name in the bottom corner.
### Create an empty package file:
  1. Open the Tools menu at the top
  2. Click the `Create Empty Package` option
### Import vanilla Sims 4 Tuning files into your package file:
  1. Open the Tools menu at the top
  2. Click the `Extract Tuning` option, wait for it to load.
  3. Locate the Tuning file you wish to import by name. Hint: _Tuning file types are determined by the folder they are in i.e. Interaction tuning files are in `interaction/`_
  4. Click the `Add to current package` button.
### Edit vanilla Tuning files
  1. To edit a vanilla tuning file, follow the steps above to import the tuning file you wish to edit.
  2. Open the file by clicking it in the left window. _You should now see the xml of the file, or the Data in a pretty format_
  3. If you do not see the xml, switch to the XML tab
  4. Make the changes you want to make (See the Custom Interactions tutorial in this wiki for more info on editing interactions.)
### Creating your own Tuning files
  1. In order to create your own tuning files, it is a good idea to import one of the vanilla tuning files to work with.
  2. Once you do this, you will need a unique Hexidecimal Identifier.
    - To get a unique hexidecimal identifier
      1. Open the Tools menu at the top
      2. Click the `Hash Generator` option.
      3. Enter the name of your tuning file (with no spaces, use underscores instead) into the `Text` box under `Hash Text`
        - At this point, you should see a unique `FNV64` identifier for your tuning file. (It is generated based on the text, entering the same text will result in the same identifier.
      4. Copy the `FNV64` value to the clipboard.
      5. Back in your package file, right click the imported vanilla tuning file, click `Duplicate`
      6. Enter the copied `FNV64` value into the `Instance` field. Leave the `Group` field alone.
        - You should now have a duplicate tuning file with the `Instance` identifier set to yours. You may now delete the original tuning file.
      7. Back in the Hash Generator, at the bottom, switch the Mode to Decimal.
      8. Copy the `FNV64` value (It should contain only numbers, no letters)
      9. Go back to your package file once more.
      9. Click on your created tuning file to open it.
      8. Navigate to the XML tab on the right.
      9. At the top of your tuning file, replace the `s` attribute of the `I` element with the copied `FNV64` value
         - Example tuning file: `<I c="..." i="interaction" m="..." n="..." s="203208">`
      10. Once that is complete, you have created your very own unique tuning file.

## How do you Create a Mod Using The Sims 4 Community Library (S4CL)?

- Create a repository based off of the [Template Project](https://github.com/ColonolNutty/s4cl-template-project) by pulling the Template down to your Machine and pushing the code to a new repository.
- Use the green button in the top right [The Main Page](https://github.com/ColonolNutty/Sims4CommunityLibrary) to download this project as a zip file.
- In your project, create another directory called `S4CL`.
- Open the downloaded project and copy the `Scripts/sims4communitylib` folder into the `S4CL` folder we created in the previous step. The folder structure should then be: `<Your Project>/S4CL/sims4communitylib`
- Right click the `S4CL` folder -> Mark Directory as -> Sources Root
  - The `S4CL` folder should turn a blue color and the `sims4communitylib` folder should look like a folder with a dot (In other words, it should NOT be blue).
- Your folder structure should look like this: `<Your Project>/S4CL/sims4communitylib` at this point.
- Ensure you list in the description of your mod a link to the github releases (You may even link a specific release to ensure compatibility.)
- Ensure you properly attribute S4CL and its author according to the license located at the bottom of this readme.
- YOU DO NOT HAVE MY PERMISSION TO BUNDLE S4CL INTO YOUR OWN MOD. So don't do it. Redirect the users of your mod to the [github repository](https://github.com/ColonolNutty/Sims4CommunityLibrary) or [releases](https://github.com/ColonolNutty/Sims4CommunityLibrary/releases) pages instead.