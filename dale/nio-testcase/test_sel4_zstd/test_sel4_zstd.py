"""Sel4SDK Zstd Test"""

import re
import logging
import pytest

from niotest.platform.nvos.common.ecu.base import NvosEcu

# pylint: disable=attribute-defined-outside-init,line-too-long
# pylint: disable=too-many-public-methods,missing-function-docstring,redefined-outer-name


@pytest.mark.NVOS_77949
@pytest.mark.run_only_if_function_support(
    {"SEL4"},
    reason="Sel4SDK FY zip Test is support hardware",
)
class TestZstd:
    """Test Zstd"""

    def before_class(self, ecu: NvosEcu, **kwargs):
        """setup before test execute"""
        self.logger = logging.getLogger("ZstdLog")
        self.file_path = "/tmp/a.cpp"
        self.file_path_b = "/tmp/b.txt"
        self.file_path_c = "/tmp/c.txt"

    def before_each_func(
        self,
        ecu: NvosEcu,
        **kwargs,
    ):
        """setup before each test case execute"""

        ecu.execute(f'echo "blue sky is coming" > {self.file_path}')
        ecu.execute(f'echo "printf("Ilovenio")" > {self.file_path_b}')

    def after_each_func(
        self,
        ecu: NvosEcu,
        **kwargs,
    ):
        """teardown after each test case execute"""

        ecu.execute(
            f"rm -rf {self.file_path} {self.file_path_b} {self.file_path}.zst {self.file_path_b}.zst"
        )

    @pytest.mark.NVOSQ_68125
    def test_zstd_version(self, ecu: NvosEcu):
        """test Zstd version"""
        version_response = ecu.execute("zstd -V")
        assert "Zstandard" in version_response
        assert "not found" not in version_response, "Zstd Version Check Failed"

    @pytest.mark.NVOSQ_68126
    def test_zstd_help(self, ecu: NvosEcu):
        """test Zstd with help"""
        help_response = ecu.execute("zstd -h")
        assert (
            "Usage: zstd [OPTIONS...] [INPUT... | -] [-o OUTPUT]" in help_response
        ), "Zstd Help Check Failed!"

    @pytest.mark.NVOSQ_68127
    def test_zstd_only_with_v(self, ecu: NvosEcu):
        """test zstd with v to compress a file"""
        ecu.execute(f"zstd -v {self.file_path}")
        self.check_file_exist(self.file_path, ecu)
        self.check_file_exist(self.file_path + ".zst", ecu)

    @pytest.mark.NVOSQ_68128
    def test_zstd_multi_files(self, ecu: NvosEcu):
        """test zstd without parameter to compress multiple files"""
        ecu.execute(f"zstd {self.file_path} {self.file_path_b}")
        for file in [self.file_path, self.file_path_b]:
            self.check_file_exist(file, ecu)
            self.check_file_exist(file + ".zst", ecu)

    @pytest.mark.NVOSQ_68129
    def test_zstd_compress_o(self, ecu: NvosEcu):
        """test zstd  compress file"""
        ecu.execute(f"zstd {self.file_path} -o {self.file_path}.zst")
        self.check_file_exist(self.file_path, ecu)
        self.check_file_exist(self.file_path + ".zst", ecu)
        self.check_file_not_empty(self.file_path + ".zst", ecu)

    @pytest.mark.NVOSQ_68130
    def test_zstd_compress_to_stout(self, ecu: NvosEcu):
        """test zstd compress file to stout"""
        ecu.execute(f"zstd -c {self.file_path} > {self.file_path}.zst")
        self.check_file_exist(self.file_path, ecu)
        self.check_file_exist(self.file_path + ".zst", ecu)
        self.check_file_not_empty(self.file_path + ".zst", ecu)

    @pytest.mark.NVOSQ_68131
    def test_zstd_compress_l(self, ecu: NvosEcu):
        """test zstd compress a file and zstd l parameter"""
        ecu.execute(f"zstd {self.file_path}")
        self.check_file_exist(self.file_path, ecu)
        self.check_file_exist(self.file_path + ".zst", ecu)
        response = ecu.execute(f"zstd -l {self.file_path}.zst")
        assert (
            "Frames  Skips  Compressed  Uncompressed  Ratio  Check  Filename"
            in response
        ), "zstd -l check failed"

    @pytest.mark.NVOSQ_68132
    def test_zstd_comperss_force(self, ecu: NvosEcu):
        """test zstd compress file force"""
        ecu.execute("zstd " + self.file_path)
        self.check_file_exist(self.file_path, ecu)
        self.check_file_exist(self.file_path + ".zst", ecu)
        origin_md5 = self.get_file_md5(self.file_path + ".zst", ecu)
        ecu.execute(f'echo "Idalelovenio" > {self.file_path}')
        ecu.execute("zstd -f " + self.file_path)
        last_md5 = self.get_file_md5(self.file_path + ".zst", ecu)
        assert last_md5 != origin_md5, "zstd force failed"

    @pytest.mark.NVOSQ_68133
    def test_zstd_compress_cpu(self, ecu: NvosEcu):
        """test zstd with T0 to compress a file"""
        ecu.execute(f"zstd -T0 {self.file_path}", timeout=300)
        self.check_file_exist(self.file_path, ecu)
        self.check_file_exist(self.file_path + ".zst", ecu)

    @pytest.mark.NVOSQ_68134
    def test_zstd_compress_rm(self, ecu: NvosEcu):
        """test zstd with rm to compress a file"""
        ecu.execute(f"zstd --rm {self.file_path}")
        self.check_file_not_exist(self.file_path, ecu)
        self.check_file_exist(self.file_path + ".zst", ecu)

    @pytest.mark.NVOSQ_68135
    def test_zstd_decompress_sigle_file(self, ecu: NvosEcu):
        """test zstd with dc to uncompress a file"""
        origin_md5 = self.get_file_md5(self.file_path, ecu)
        ecu.execute(f"zstd --rm {self.file_path}")
        self.check_file_not_exist(self.file_path, ecu)
        self.check_file_exist(self.file_path + ".zst", ecu)
        ecu.execute(f"zstd -dc {self.file_path}.zst > {self.file_path}")
        last_md5 = self.get_file_md5(self.file_path, ecu)
        assert origin_md5 == last_md5, "zstd decompress failed"

    @pytest.mark.NVOSQ_68136
    def test_zstd_decompress_multi_file(self, ecu: NvosEcu):
        """test zstd with d to multipully uncompress files"""
        origin_md5_a = self.get_file_md5(self.file_path, ecu)
        origin_md5_b = self.get_file_md5(self.file_path_b, ecu)
        ecu.execute(f"zstd --rm {self.file_path} {self.file_path_b}")
        for file in [self.file_path, self.file_path_b]:
            self.check_file_not_exist(file, ecu)
            self.check_file_exist(file + ".zst", ecu)
        ecu.execute(f"zstd -d {self.file_path}.zst {self.file_path_b}.zst")
        last_md5_a = self.get_file_md5(self.file_path, ecu)
        last_md5_b = self.get_file_md5(self.file_path_b, ecu)
        assert origin_md5_a == last_md5_a, "zstd decompress failed"
        assert origin_md5_b == last_md5_b, "zstd decompress failed"

    @pytest.mark.NVOSQ_68137
    def test_zstd_dvf(self, ecu: NvosEcu):
        """test zstd with dvf to uncompress a file"""
        origin_md5 = self.get_file_md5(self.file_path, ecu)
        ecu.execute("zstd " + self.file_path)
        self.check_file_exist(self.file_path + ".zst", ecu)
        ecu.execute(f"zstd -dvf {self.file_path}.zst")
        last_md5 = self.get_file_md5(self.file_path, ecu)
        assert origin_md5 == last_md5, "zstd decompress failed"

    @pytest.mark.NVOSQ_68138
    def test_zstd_rm_d(self, ecu: NvosEcu):
        """test zstd with --rm and -d to uncompress a file"""
        origin_md5 = self.get_file_md5(self.file_path, ecu)
        ecu.execute("zstd --rm " + self.file_path)
        self.check_file_not_exist(self.file_path, ecu)
        self.check_file_exist(self.file_path + ".zst", ecu)
        ecu.execute(f"zstd -d --rm {self.file_path}.zst")
        last_md5 = self.get_file_md5(self.file_path, ecu)
        assert origin_md5 == last_md5, "zstd decompress failed"

    @pytest.mark.NVOSQ_68139
    def test_zstd_cpmpress_compressed_file(self, ecu: NvosEcu):
        """test zstd compress a compressed file"""

        ecu.execute("zstd --rm " + self.file_path)
        self.check_file_not_exist(self.file_path, ecu)
        self.check_file_exist(self.file_path + ".zst", ecu)
        ecu.execute(f"zstd --rm {self.file_path}.zst")
        self.check_file_not_exist(self.file_path + ".zst", ecu)
        self.check_file_exist(self.file_path + ".zst" + ".zst", ecu)

    @pytest.mark.NVOSQ_68140
    def test_zstd_uncompress_special_file(self, ecu: NvosEcu):
        """test zstd uncompress a special file"""

        ecu.execute(f"rm -rf {self.file_path} {self.file_path_b}")
        special_file = "/tmp/a.cpp.zst"
        ecu.execute(f'echo "blue sky is coming" > {special_file}')
        response = ecu.execute("zstd -d " + special_file)
        assert (
            "zstd: /tmp/a.cpp.zst: unsupported format" in response
        ), "zstd uncompress error file"

    @pytest.mark.NVOSQ_68141
    def test_zstd_compress_stdout_unzst(self, ecu: NvosEcu):
        """test zstd compress file to unzst"""

        stdout_file = "/tmp/d.py"
        ecu.execute(f"zstd -c {self.file_path} > {stdout_file}")
        self.check_file_exist(stdout_file, ecu)

    @pytest.mark.NVOSQ_68142
    def test_zstd_compress_default_time(self, ecu: NvosEcu):
        """test zstd compress file used time"""

        ecu.execute(
            f"dd if=/dev/urandom of={self.file_path_c} bs=1M count=250",
            timeout=500,
        )
        response = ecu.execute(f"time zstd {self.file_path_c}", timeout=500)
        use_time = self.get_time(response)
        self.check_file_exist(self.file_path_c + ".zst", ecu)
        self.logger.info(f"zstd comperss time:{use_time}")

    @pytest.mark.NVOSQ_68143
    def test_zstd_compress_level_time(self, ecu: NvosEcu):
        """test zstd with different level to compress file used time"""

        ecu.execute(
            f"dd if=/dev/urandom of={self.file_path_c} bs=1M count=250",
            timeout=500,
        )
        for level in [6, 12]:
            response = ecu.execute(
                "time zstd -f -" + str(level) + " " + self.file_path_c, timeout=500
            )
            use_time = self.get_time(response)
            self.check_file_exist(self.file_path_c + ".zst", ecu)
            self.logger.info(f"zstd comperss level{level} time:{use_time}")

    @pytest.mark.NVOSQ_68144
    def test_zstd_compress_high_level(self, ecu: NvosEcu):
        """test zstd with high level to compress file used time"""

        for level in [19, 22]:
            response = ecu.execute(
                "time zstd -f --ultra -" + str(level) + " " + self.file_path,
                timeout=500,
            )
            use_time = self.get_time(response)
            self.check_file_exist(self.file_path + ".zst", ecu)
            self.logger.info(f"zstd comperss level{level} time:{use_time}")

    @pytest.mark.NVOSQ_68145
    def test_zstd_with_tar_time(self, ecu: NvosEcu):
        """test zstd compress file with tar use time"""

        target_file = "/tmp/a.cpp.tar.zst"
        tar_file = "/tmp/a.cpp.tar"
        origin_md5 = self.get_file_md5(self.file_path, ecu)
        response_compress = ecu.execute(
            f"time tar -cvf {tar_file} {self.file_path}", timeout=500
        )
        use_time_compress = [self.get_time(response_compress)]
        response_compress = ecu.execute(
            f"time zstd -T0 --ultra -22 {tar_file}", timeout=500
        )
        use_time_compress.append(self.get_time(response_compress))
        use_time_compress = sum(use_time_compress)
        self.check_file_exist(target_file, ecu)
        self.logger.info(f"zstd comperss with tar use time:{use_time_compress}")
        response_uncompress = ecu.execute(
            f"time zstd -df -T0 {target_file}", timeout=500
        )
        use_time_uncompress = [self.get_time(response_uncompress)]
        response_uncompress = ecu.execute(f"time tar -xvf {tar_file}", timeout=500)
        use_time_uncompress.append(self.get_time(response_uncompress))
        use_time_uncompress = sum(use_time_uncompress)
        self.check_file_exist(self.file_path, ecu)
        self.logger.info(f"zstd uncomperss with tar use time:{use_time_uncompress}")
        last_md5 = self.get_file_md5(self.file_path, ecu)
        assert origin_md5 == last_md5, "zstd compress/uncompress error with tar"

    @staticmethod
    def check_file_exist(filepath, ecu: NvosEcu):
        """check if file exist"""
        response = ecu.execute(f"ls {filepath}")
        assert (
            "ls: " + filepath + ": No such file or directory" not in response
        ), "file is not exist!"

    @staticmethod
    def check_file_not_exist(filepath, ecu: NvosEcu):
        """check if file not exist"""
        response = ecu.execute(f"ls {filepath}")
        assert (
            "ls: " + filepath + ": No such file or directory" in response
        ), "file already exists!"

    @staticmethod
    def check_file_not_empty(filepath, ecu: NvosEcu):
        """check if file isn't empty"""

        response = ecu.execute(f"cat {filepath}")
        assert response != "", "file is empty!"

    @staticmethod
    def get_file_md5(filepath, ecu: NvosEcu):
        """get file's MD5'"""

        response = ecu.execute(f"md5sum {filepath}")
        assert (
            "md5sum: " + filepath + ": No such file or directory" not in response
        ), "file is not exist!"

        md5_response = ""
        for line in response.split("\n"):
            if filepath in line and "md5sum" not in line:
                md5_response = line
                break
        return md5_response.split(" ")[0].replace("/r", "")

    @staticmethod
    def get_time(time):
        match = re.search(r"real\s+([0-9.]+)", time)
        if match:
            use_time = float(match.group(1))
        return use_time
