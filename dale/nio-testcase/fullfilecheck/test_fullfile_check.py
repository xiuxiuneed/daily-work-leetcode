"""SafeOS Fullfile Check"""
import logging
import pytest


from niotest.platform.nvos.common.ecu.base import NvosEcu


@pytest.mark.run_only_if_function_support(
    {"SEL4", "IS_HW"},
    reason="SafeOSSDK FullfileCheck Test is supprot simulator and hardware",
)
class TestFilecheck:
    """Test Check File"""

    @pytest.mark.NVOSQ_66169
    @pytest.mark.NVOS_62041
    def test_fullfile_specification_check(self, ecu: NvosEcu):
        """Test specification"""
        response = ecu.execute("ls -hlR /", timeout=5)
        logging.info("Get the command result")
        assert response is not None

        lines = response.split("\n")
        assert lines, "Response does not contain any lines"

        valid_prefixes = ("./", "-rw", "drw", "total", "", ".")

        all_lines_valid = True

        for line in lines:
            if line:
                with pytest.assume:
                    assert any(
                        line.startswith(prefix) for prefix in valid_prefixes
                    ), f"This line does not follow the rules: {line}"
                    all_lines_valid &= any(
                        line.startswith(prefix) for prefix in valid_prefixes
                    )

        if all_lines_valid:
            logging.info("all file attributes are in compliance with the specification")
