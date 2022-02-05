In this tutorial I will be showing you how you can create your own custom interaction, utilizing the features of S4CL.
Sims 4 Studio and PyCharm are the tools I use most often, they will be what I am using in this tutorial.

## Sims 4 Package File

To start create a package file, within that package file, we will create an Interaction Tuning file.
Each interaction tuning file will have the Type of `E882D22F`.

```XML
<?xml version="1.0" encoding="UTF-8"?>
<I c="ExampleInteraction" i="interaction" m="mod_root_namespace.example_interaction" n="S4CL_Example_Interaction" s="123">
  <V t="disabled" n="_saveable" />
  <T n="category">0</T>  <!--Parent Pie Category, Set to 0 if you want your interaction to appear at the root. -->
  <T n="display_name">0x111111111</T>  <!-- This is the text displayed on the interaction, the string comes from String Tables. i.e. 0xABC would pull the String Table value with identifier "ABC" -->
  <U n="progress_bar_enabled">
    <T n="bar_enabled">False</T>
  </U>
  <E n="target_type">OBJECT</E>
</I>
```
Let's break down the XML tuning file:
First, the root element:
`<I c="ExampleInteraction" i="interaction" m="mod_root_namespace.example_interaction" n="S4CL_Example_Interaction" s="123">`
- `c` is the class the interaction is going to use.
- `i` tells the package file and game what type of tuning file it is.
- `m` is the namespace or file path to the file containing the class specified in `c`.
- `n` is the name of the tuning file, this is a short name given to your tuning file, it doesn't even need to be unique!
- `s` is a unique decimal identifier of the tuning file. It is how you will reference the tuning file from Python.
Now onto different properties:
- `category` is the decimal identifier of the Pie Menu Category Tuning. The interaction will be displayed in the game under this Pie Menu when interacting with things. One example, is the "Friendly" Pie Menu.
- `display_name` is the Hexadecimal identifier of a string from the StringTable. The format is `0x11111111` with the `11111111` portion being the actual Hex.
- `progress_bar_enabled` is an object with its own properties. Namely `bar_enabled`. Setting `bar_enabled` to `False` means that when the sim is performing the interaction in-game, there won't be a progress circle displayed on the interaction in the Sims interaction queue.
- `target_type` is the type of target your interaction will expect to be used on. Right now it is set to `Object` meaning the interaction can occur on any object.

## Creating your Custom Interaction in Python:
Since you have specified the above tuning file to look for the `ExampleInteraction` class within the file `mod_root_namespace.example_interaction.py`, we want to create a file within our project that matches.

Create a folder named `mod_root_namespace` and create a file within it named `example_interaction.py`.
```Python
from typing import Any
from sims4communitylib.classes.testing.common_test_result import CommonTestResult
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from interactions.context import InteractionContext
from sims.sim import Sim
from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction

class ExampleInteraction(CommonImmediateSuperInteraction):
    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> CommonTestResult:
        result = 1 + 1
        # Ignore the following logic, it'll never go in either of the checks, but it is just an example.
        if result == 3:
            # Interaction will show but be disabled and it will display "Test Tooltip" when hovered by the player.
            return cls.create_test_result(False, reason="Test Tooltip")

        if result == 4:
            # Alternative way to specify a Tooltip
            # Interaction will show but be disabled and it will display "Test Tooltip" when hovered by the player.
            return cls.create_test_result(False, reason="No Reason", tooltip='Test Tooltip')

        if result == 5:
            # Interaction will be hidden completely.
            return CommonTestResult.NONE

        # Interaction will display and be enabled.
        return CommonTestResult.TRUE

    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> CommonExecutionResult:
        # Put here what you want the interaction to do as soon as the player clicks it while it is enabled.
        return CommonExecutionResult.TRUE
```
Let's break this file down:
First, notice the name of the class, it is `ExampleInteraction` which matches the value of `c` in the tuning file previously.

The class inherits from another class: `CommonImmediateSuperInteraction`. This is one of the base classes for creating custom interactions while using `S4CL`. It can be used for interactions that appear on Sims as well.

It contains many more hooks than what you see here, but to keep this example simple, we'll be utilizing `on_test` and `on_started`, which are the two main hooks for writing custom interactions.

- `on_test` This hook will tell the interaction when and how it should display by using `CommonTestResult` (We'll go more into this further down)
- `on_started` This hook will be what the interaction does when the player (or a sim) is performing an interaction.
### Custom Test Results:
Let's take a look at the different types of `CommonTestResult` we can return and their effects.

Show:

`return CommonTestResult.TRUE`
- Returning this value will show your interaction.

Hide:

`return CommonTestResult.NONE`
- Returning this value will hide your interaction completely.

Tooltip:

`return cls.create_test_result(False, reason="Test Tooltip")`
- Returning something like this will disable your interaction (greyed out in-game). If the player were to hover over the disabled interaction, it will show them a `Tooltip` with the text "Test Tooltip". You can specify Localized strings instead of "Test Tooltip" if you wanted to.

Alternative Tooltip:

`return cls.create_test_result(False, reason="No Reason", tooltip=CommonLocalizationUtils.create_localized_tooltip("Test Tooltip"))`
- This will have the same effect as the previous sample, but it allows you to specify a LocalizedTooltip of your own via the `tooltip` argument. You can utilize `StringTable` text through this, which also enables translations.


# Register Your Custom Interaction:
Finally, we want to register an interaction to display when the player clicks on different things.
Go ahead and create a file named `register_interactions.py` within your `mod_root_namespace` folder.
In this example, we will register the interaction to display when the player clicks on an Elder Sim.
```Python
from typing import Tuple
from objects.script_object import ScriptObject
from sims.sim import Sim
from sims4communitylib.services.interactions.interaction_registration_service import CommonInteractionRegistry, \
    CommonInteractionType, CommonScriptObjectInteractionHandler
from sims4communitylib.utils.common_type_utils import CommonTypeUtils
from sims4communitylib.utils.sims.common_age_utils import CommonAgeUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils

@CommonInteractionRegistry.register_interaction_handler(CommonInteractionType.ON_SCRIPT_OBJECT_LOAD)
class _RegisterExampleInteractionHandler(CommonScriptObjectInteractionHandler):
    @property
    def interactions_to_add(self) -> Tuple[int]:
        interactions: Tuple[int] = (
            123,
        )
        return interactions

    def should_add(self, script_object: ScriptObject, *args, **kwargs) -> bool:
        if not CommonTypeUtils.is_sim_instance(script_object):
            return False # If the object is not a Sim, return False.
        script_object: Sim = script_object # Type hint so we can tell the code that it IS a Sim object (Makes it easier for Intellisense to work with it in PyCharm)
        sim_info = CommonSimUtils.get_sim_info(script_object)
        return CommonAgeUtils.is_elder(sim_info) # If the object is an Elder Sim.
```
There are a couple of required things to get this going:
Let's take a look at the decorator of the class.

`@CommonInteractionRegistry.register_interaction_handler(CommonInteractionType.ON_SCRIPT_OBJECT_LOAD)`
- We are essentially telling the `CommonInteractionRegistry` that our handler registers interactions to `ScriptObject`s

Next we are inheriting from the class `CommonScriptObjectInteractionHandler`. This is the base class for registration handlers that register their interactions to `ScriptObject`'s

Now for the hooks we are using:
- `interactions_to_add` - This property contains the Decimal Identifiers of the interactions we want to register, remember the `s` attribute from the tuning files at the start? Well, this is where it is used.
- `should_add` - In this function, we determine if we want a `ScriptObject` to have our interaction show up on it when clicked. In the example above, we are checking that the `ScriptObject` is an Elder Sim.

# File Structure
At the end of this example, you should end up with a couple files.
- `mod_root/scripts/mod_root_namespace/register_interactions.py`
- `mod_root/scripts/mod_root_namespace/example_interaction.py`
- `mod_root/mod_name.package`

Put your files in the `The Sims 4/Mods` folder and away you go!

- `The Sims 4/Mods/mod_root/scripts/mod_root_namespace/register_interactions.py`
- `The Sims 4/Mods/mod_root/scripts/mod_root_namespace/example_interaction.py`
- `The Sims 4/Mods/mod_root/mod_name.package`