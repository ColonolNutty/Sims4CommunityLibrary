In this tutorial I will be showing you how you can create your own custom events, utilizing the features of S4CL.
PyCharm is the tool I use most often, it will be what I am using in this tutorial.

## Creating your Custom Event in Python:
In your project create a new python file, we'll call it `my_own_custom_event.py`.

Inside that file, we will add our Custom Event, the details of which can be whatever you wish (They don't have to match the example completely).

```Python
from sims4communitylib.events.event_handling.common_event import CommonEvent

# The name of the event does not matter, however it must inherit from CommonEvent.
class MyOwnCustomEvent(CommonEvent):

    def __init__(self, some_identifier: int):
        self._some_identifier = some_identifier

    @property
    def some_identifier(self) -> Zone:
        return self._some_identifier
```
Let's break this file down:
- First, you'll notice the class inherits from `CommonEvent`. This is important, because it tells the code that it is a type of event.
- Second, you'll notice arguments in the `__init__` function. The arguments or keyword arguments can be whatever you wish, they make up the data that you will be passing to the listeners of `MyOwnCustomEvent`.

## How Do I Dispatch My Custom Event?
- Dispatching your Event is as easy as invoking a function.

Where ever you wish to dispatch your event, you simply have to do the following:
```Python
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry

CommonEventRegistry.get().dispatch(MyOwnCustomEvent(123))
```

Anything listening for the `MyOwnCustomEvent` will be invoked.

## How Do You Listen For Custom Events?

The function listening for the event can either be a global function or a static function within a class like so.

```Python
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry

class MyCustomEventListenerThing:
    @staticmethod
    @CommonEventRegistry.handle_events(ModInfo.get_identity().name)
    def _handle_my_custom_event(event_data: MyOwnCustomEvent):
        if event_data.some_identifier === 123:
            return
        # Do some other code.

@CommonEventRegistry.handle_events(ModInfo.get_identity().name)
def _handle_the_custom_event_globally(event_data: MyOwnCustomEvent):
    if event_data.some_identifier === 123:
        return
    # Do some other code.
    
```

In order for a function to be valid for listening to events, the following criteria must be met:

- The first and only argument of the function MUST have the name `event_data`.
- The `event_data` argument MUST have the Type Hint matching the event you are listening for. (`MyOwnCustomEvent` in the example above)
- The function must either be a global function OR it must be decorated with `@staticmethod`.
  - Class and Instance functions WILL NOT WORK! These are identified by the first argument being either `cls` (Class) or `self` (Instance).

The first argument of `CommonEventRegistry.handle_events` is a string that identifies the Mod that created the listener. It is mainly used when things blow up and exceptions must be logged. It tells S4CL what log it should put the exception message in.


For example, if `ModInfo.get_identity().name` had a value of `CustomModOfMine`, when an exception occurs, the message will be logged in a file with the name `CustomModOfMine_Exceptions.txt`

It is as simple as that.

# File Structure
At the end of this example, you should end up with a couple files.
- `mod_root/scripts/mod_root_namespace/my_own_custom_event.py`

Put your files in the `The Sims 4/Mods` folder and away you go!

- `The Sims 4/Mods/mod_root/scripts/mod_root_namespace/my_own_custom_event.py`