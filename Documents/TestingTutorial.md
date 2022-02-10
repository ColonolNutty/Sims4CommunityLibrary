In this tutorial we will cover the basics of testing.

## How Do I Create A Test?
- To create a test you will use the `CommonTestService.test_class` and `CommonTestService.test` decorators.

```Python
from sims4communitylib.testing.common_assertion_utils import CommonAssertionUtils
from sims4communitylib.testing.common_test_service import CommonTestService
from sims4communitylib.mod_support.common_mod_info import CommonModInfo


class ModInfo(CommonModInfo):
    _FILE_PATH: str = str(__file__)

    @property
    def _name(self) -> str:
        return 'MyModName'

    @property
    def _author(self) -> str:
        return 'MyName'

    @property
    def _base_namespace(self) -> str:
        return 'mod_package_name'

    @property
    def _file_path(self) -> str:
        return ModInfo._FILE_PATH

    @property
    def _version(self) -> str:
        return 'v1.0'

@CommonTestService.test_class(ModInfo.get_identity())
class _ExampleTests:
    @staticmethod
    @CommonTestService.test()
    def _do_a_test():
        CommonAssertionUtils.are_equal(True, False)

    @staticmethod
    @CommonTestService.test(True, True)
    def _do_a_test_with_args(result: bool, expected_result: bool):
        CommonAssertionUtils.are_equal(result, expected_result)
```

Let's break this down:
- The argument being sent to the `CommonTestService.test_class` decorator is the identity of your Mod, this will allow S4CL to group tests to a specific mod and know where it should store the results of the tests for example: `MyModName_Messages.txt`.
- `CommonAssertionUtils` is the utility used to assert values. (See the [docs](https://sims4communitylibrary.readthedocs.io/en/latest/sims4communitylib.testing.html#assertion-utils) for more details)
- `CommonTestService.test` will accept any number of arguments and will send those arguments to the test function when the tests are run. This allows you to keep similar test code but provide different values to it. If no arguments are passed in to the decorator, then no arguments will be sent to your test.
- Tests must ALWAYS be decorated with `@staticmethod`.

### How Do You Run The Tests And Where Do You See The Results?

- If your Tests do not rely on code specific to The Sims 4, you can simply run them through your editor.
  - The results will be displayed in your Editor Output.

```Python
# Import the Tests you want to run, Importing them registers them to the CommonTestService.
import tests.example_test
from sims4communitylib.testing.common_test_service import CommonTestService

# Run The Tests.
CommonTestService.get().run_tests()
```
- If your Tests rely on code specific to The Sims 4 (For example SimInfo), you must:
  1. Run the game
  2. Open the console (CTRL + SHIFT + C)
  3. Type the following command `s4clib.run_tests`.
  - The results will be displayed in a file within the `The Sims 4/mod_logs` folder, with a name dependent on what you sent to the `test_class` decorator: `<ModName>_Messages.txt`