"""Sel4SDK ToyBox dumpe2fs Test"""
import re
import pytest
from niotest.platform.nvos.common.ecu.base import NvosEcu

# pylint: disable=too-many-locals, too-many-arguments


@pytest.mark.run_only_if_function_support(
    {"IS_MPU"},
    reason="Sel4SDK Toybox Test is support simulator and hardware",
)
class TestSel4ToyBoxDumpe2FS:
    """dumpe2fs test"""

    @classmethod
    def setup_class(cls):
        """setup for test"""

    @pytest.mark.NVOSQ_66812
    @pytest.mark.NVOS_66630
    def test_dumpe2fs(self, ecu: NvosEcu):
        """test dumpe2fs with every blocks"""
        blocks = []
        response = ecu.execute("df -h", timeout=5)
        assert response is not None

        for line in response.split("\n"):
            if "/dev" in line:
                block = line.split()[0]
                blocks.append(block)

        for existent_path in blocks:
            response = ecu.execute(f"dumpe2fs {existent_path}", timeout=5)
            with pytest.assume:
                assert response is not None
                assert re.search("Filesystem features.*dir_index", response)
