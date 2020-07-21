In this tutorial we will cover the basics of logging.

## How Do I Log A Message?

### Create Logger
- Before you can log a message, you must register (create) a log.

```Python
from sims4communitylib.utils.common_log_registry import CommonLogRegistry

example_log: CommonLog = CommonLogRegistry.get().register_log('MyModName', 'example_logger_of_logs')
```

Let's break this down:
- `CommonLogRegistry` is the class that holds all logs, you use it to register, enable, and disable logs.
- `example_log` is your Logger, use it to log messages.
- `example_logger_of_logs` is the name of your Logger. This is the unique identifier of this logger and is used in conjunction with the in-game command `s4clib.enable_log example_logger_of_logs`.
- `MyModName` is the name of your Mod, it is also used to tell S4CL where to log any messages. `MyModName_Messages.txt`

### Log Messages:

Once you've created a logger, you can then invoke various functions on it. (For more details, check out the [docs](https://sims4communitylibrary.readthedocs.io/en/latest/sims4communitylib.logging.html#common-log))
- `debug(str)` is likely the most common function you will use, it is a basic function you may use to log information.
- `enable()` will enable your log in the code. Similar to the command `s4clib.enable_log <log_name>`
- `disable()` will disable your log in the code. Similar to the command `s4clib.disable_log <log_name>`

### Example:
```Python
from sims4communitylib.utils.common_log_registry import CommonLogRegistry

example_log: CommonLog = CommonLogRegistry.get().register_log('MyModName', 'example_logger_of_logs')
example_log.debug('I am a message, fear {}!'.format('me'))
```

If `example_log` has been enabled, either through the `s4clib.enable_log` command or `example_log.enable()`, then the message `I am a message, fear me!` will be logged in a file with the name `MyModName_Messages.txt`

An interesting thing you can do with `enable` and `disable` is to only enable it in certain cases.

```Python
from sims4communitylib.utils.common_log_registry import CommonLogRegistry

example_log: CommonLog = CommonLogRegistry.get().register_log('MyModName', 'example_logger_of_logs')
example_log.debug('I am a message, fear {}!'.format('me'))
example_log.enable()
example_log.debug('I am message number 2!')
example_log.disable()
example_log.debug('I am message number 3!')
```

In the above example, only the message `I am message number 2!` will be logged to `MyModName`, because `example_log` was only enabled at the time of hitting that line.