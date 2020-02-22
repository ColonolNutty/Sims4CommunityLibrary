from sims4communitylib.modinfo import ModInfo
from sims4communitylib.testing.common_assertion_utils import CommonAssertionUtils
from sims4communitylib.testing.common_test_service import CommonTestService
from sims4communitylib.utils.sims.common_sim_spawn_utils import CommonSimSpawnUtils


@CommonTestService.test_class(ModInfo.get_identity().name)
class _CommonSimSpawnUtilsTests:
    @staticmethod
    @CommonTestService.test()
    def _should_spawn_and_despawn_human_sim_properly() -> None:
        sim_info = CommonSimSpawnUtils.create_human_sim_info(first_name='Tester', last_name='McTest', source='testing')
        CommonAssertionUtils.is_true(sim_info is not None)
        CommonAssertionUtils.is_true(CommonSimSpawnUtils.despawn_sim(sim_info, cause='Was just a test.'))

