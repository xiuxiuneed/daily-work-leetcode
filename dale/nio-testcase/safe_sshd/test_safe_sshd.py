"""Safe SSHD test"""
import time
from base64 import b64decode
import logging
import re
import socket
import pytest
import paramiko
from niotest.platform.nvos.common.ecu.base import NvosEcu
from nlib.platform.utils.macro import Macro

# pylint: disable=line-too-long, too-many-instance-attributes, too-many-arguments
# pylint: disable=attribute-defined-outside-init
# pylint: disable=W0703, W0201


@pytest.mark.NVOS_73797
@pytest.mark.run_only_if_function_support(
    {"SEL4", "IS_HW"},
    reason="Safe SSHD test is supprot hardware",
)
class TestSafeSSHD:
    """Test Safe SSHD"""

    @classmethod
    def setup_class(cls):
        """setup for test"""

        cls.logger = logging.getLogger("SafeSSHLog")
        cls.acore_up_flag = "Uds.service"
        cls.safeos_hostname = "172.20.1.1"
        cls.safeos_port = 3333
        cls.username = "cm9vdA=="
        cls.password = "I0xAblQxbmc+PHUj"
        cls.safeos_username = b64decode(cls.username).decode("ascii")
        cls.safeos_password = b64decode(cls.password).decode("ascii")
        cls.safe_pid = "1"

    @pytest.mark.NVOSQ_67520
    def test_safe_showmem_excute(self, ecu: NvosEcu):
        """test safe ssh showmem execute"""

        self._reboot_and_assert(ecu)
        commands = [
            "efc safe_showmem -o {path_pty}",
            "efc safe_showmem -o {path_pty} -a",
            "efc safe_showmem -o {path_pty} -d",
            "efc safe_showmem -p {pid} -o {path_pty}",
            "efc safe_showmem -o {path_pty} -?",
        ]
        commands_outputs = self.ssh_connect_and_execute_commands(commands)
        assert commands_outputs is not None, "Failed to connect to the host."

        for command in commands_outputs:
            if "-?" not in command:
                assert "Total" in commands_outputs[command]
                if "-a" in command:
                    assert "PID" in commands_outputs[command]
                if "-d" in command:
                    assert "UntypedTotal" in commands_outputs[command]
                if "-p" in command:
                    assert "ELF" in commands_outputs[command]
            else:
                assert "Usage" in commands_outputs[command]

    @pytest.mark.NVOSQ_67521
    def test_safe_ps_excute(self, ecu: NvosEcu):
        """test safe ssh ps execute"""

        commands = [
            "efc safe_ps -o {path_pty}",
            "efc safe_ps -o {path_pty} -T",
            "efc safe_ps -o {path_pty} -f",
            "efc safe_ps -o {path_pty} -?",
        ]
        commands_outputs = self.ssh_connect_and_execute_commands(commands)
        assert commands_outputs is not None, "Failed to connect to the host."

        for command in commands_outputs:
            if "-?" not in command:
                assert "file" in commands_outputs[command]
                if "-T" in command:
                    assert "file-1" in commands_outputs[command]
                if "-f" in command:
                    assert "PGID" in commands_outputs[command]
            else:
                assert "Usage" in commands_outputs[command]

    @pytest.mark.NVOSQ_67522
    def test_safe_locktrace_excute(self, ecu: NvosEcu):
        """test safe ssh locktrace execute"""

        commands = [
            "efc safe_locktrace -p {pid} -o {path_pty}",
            "efc safe_locktrace -o {path_pty} -?",
        ]
        commands_outputs = self.ssh_connect_and_execute_commands(commands)
        assert commands_outputs is not None, "Failed to connect to the host."

        for command in commands_outputs:
            if "-?" not in command:
                assert "memory map" in commands_outputs[command]
            else:
                assert "Usage" in commands_outputs[command]

    @pytest.mark.NVOSQ_67523
    def test_safe_top_excute(self, ecu: NvosEcu):
        """test safe ssh top execute"""

        commands = [
            "efc safe_top -o {path_pty} -t 1",
            "efc safe_top -p {pid} -o {path_pty} -t 1",
            "efc safe_top -s 10 -o {path_pty} -t 1",
            "efc safe_top -o {path_pty} -?",
        ]
        commands_outputs = self.ssh_connect_and_execute_commands(commands)
        assert commands_outputs is not None, "Failed to connect to the host."

        for command in commands_outputs:
            if "-?" not in command:
                assert "Tasks" in commands_outputs[command]
                if "-p" in command:
                    assert "file" in commands_outputs[command]
                if "-s" in command:
                    assert "time-1" in commands_outputs[command]
            else:
                assert "Usage" in commands_outputs[command]

    @pytest.mark.NVOSQ_67524
    def test_fsless_mode_after_fs_failure(self, ecu: NvosEcu):
        """test safe ssh after fs failure"""

        ecu.kill("extfs", -11)
        commands = [
            "efc safe_locktrace -p {pid} -o {path_pty}",
            "efc safe_top -o {path_pty} -t 1",
            "efc safe_ps -o {path_pty}",
            "efc safe_showmem -o {path_pty}",
        ]
        commands_outputs = self.ssh_connect_and_execute_commands(commands)
        assert commands_outputs is not None, "Failed to connect to the host."

        for command in commands_outputs:
            if "locktrace" in command:
                assert "memory map" in commands_outputs[command]
            if "top" in command:
                assert "Tasks" in commands_outputs[command]
            if "ps" in command:
                assert "extfs" not in commands_outputs[command]
            if "showmem" in command:
                assert "Total" in commands_outputs[command]

        self.logger.info("hard reset and wait acore up")
        time.sleep(10)
        self._hard_reset_and_assert(ecu)

    @pytest.mark.NVOSQ_67525
    def test_sshd_password_eorror(self, ecu: NvosEcu):
        """test safe ssh password error"""

        passwords = ["123456789000", "#L@nT1ng><u#da", "#L@nT1ng"]

        for password in passwords:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                client.connect(
                    self.safeos_hostname,
                    port=self.safeos_port,
                    username=self.safeos_username,
                    password=password,
                    timeout=60,
                    look_for_keys=False,
                )
                shell = client.invoke_shell()
                time.sleep(1)
                output1 = shell.recv(1024).decode("utf-8").strip()
                match = re.search(r"(/dev/pts/\d+)", output1)
                path_pty = match.group(1) if match else None
                if path_pty is not None:
                    assert False, f"Connected with incorrect password: {password}"
            except paramiko.AuthenticationException:
                self.logger.info(
                    f"Password error and connection failed for '{password}': Authentication failed."
                )
            client.close()
            self.logger.info("wait for next connect")
            time.sleep(10)
        self._reboot_and_assert(ecu)

    @pytest.mark.NVOSQ_67526
    def test_fsless_mode_execute_performance(self):
        """test fsless mode excute performance"""

        commands = [
            "efc safe_locktrace -p {pid} -o {path_pty}",
            "efc safe_top -o {path_pty} -t 1",
            "efc safe_ps -o {path_pty}",
            "efc safe_showmem -o {path_pty}",
        ]
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            self.safeos_hostname,
            port=self.safeos_port,
            username=self.safeos_username,
            password=self.safeos_password,
            look_for_keys=False,
        )
        shell = client.invoke_shell()
        time.sleep(1)
        output1 = shell.recv(1024).decode("utf-8").strip()
        match = re.search(r"(/dev/pts/\d+)", output1)
        path_pty = match.group(1) if match else None
        if path_pty:
            commands = [
                cmd.format(path_pty=path_pty, pid=self.safe_pid) for cmd in commands
            ]
            for command in commands:
                shell.send(command + "\n")
                time.sleep(1)
                start_time = time.time()
                output2 = self._get_full_output(shell)
                if "locktrace" in command:
                    assert "memory map" in output2
                if "top" in command:
                    assert "Tasks" in output2
                if "ps" in command:
                    assert "file" in output2
                if "showmem" in command:
                    assert "Total" in output2
                end_time = time.time()
                self.logger.info(f"{command} execute time: {end_time - start_time}")
        client.close()

    @pytest.mark.NVOSQ_67527
    def test_multi_user_concurrent_login(self, ecu: NvosEcu):
        """test ssh concurrent login"""

        def _concurrent_ssh_connect():
            """Connect through paramiko"""

            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(
                self.safeos_hostname,
                port=self.safeos_port,
                username=self.safeos_username,
                password=self.safeos_password,
                timeout=60,
                look_for_keys=False,
            )
            shell = client.invoke_shell()
            time.sleep(1)
            output1 = shell.recv(1024).decode("utf-8").strip()
            match = re.search(r"(/dev/pts/\d+)", output1)
            path_pty = match.group(1) if match else None
            return path_pty

        path_pty = _concurrent_ssh_connect()
        self.logger.info("connect first time")
        assert "/dev/pts" in path_pty, "can not connect with low latency network"
        self.logger.info("connect first time successfully")

        try:
            time.sleep(10)
            self.logger.info("try connect second time")
            path_pty2 = _concurrent_ssh_connect()
            if path_pty2 is not None:
                assert False, "error with concurrent connect"

        except (ConnectionResetError, socket.timeout, TimeoutError) as second_connect:
            self.logger.info(f"second connect refused: {second_connect}")
        except paramiko.ssh_exception.SSHException as second_connect:
            assert "Error reading SSH protocol banner" in str(second_connect)
            self.logger.info(f"second connect refused: {second_connect}")

        self._reboot_and_assert(ecu)

    @pytest.mark.NVOSQ_67528
    def test_low_latency_network_connection(self, ecu: NvosEcu):
        """test ssh with latency network"""

        Macro.subprocess_execute(
            "sudo tc qdisc add dev eno1 root handle 1: htb default 12"
        )
        Macro.subprocess_execute(
            "sudo tc class add dev eno1 parent 1: classid 1:1 htb rate 100kbps ceil 100kbps"
        )
        Macro.subprocess_execute(
            "sudo tc filter add dev eno1 protocol ip parent 1:0 prio 1 u32 match ip dport 3333 0xffff flowid 1:1"
        )
        Macro.subprocess_execute(
            "sudo tc filter add dev eno1 protocol ip parent 1:0 prio 1 u32 match ip sport 3333 0xffff flowid 1:1"
        )
        _, result = Macro.subprocess_execute("sudo tc qdisc show dev eno1")
        assert "htb" in result

        path_pty = self.ssh_connect(
            self.safeos_password,
        )
        assert "/dev/pts" in path_pty, "can not connect with low latency network"

        Macro.subprocess_execute("sudo tc qdisc del dev eno1 root")

    @pytest.mark.parametrize("connect_count", [5, 10])
    @pytest.mark.NVOSQ_67529
    def test_fsless_mode_repeated_entry(self, ecu: NvosEcu, connect_count: int):
        """test ssh entry times"""

        self._reboot_and_assert(ecu)
        result = "ready"
        successful_connections = 0
        for attempt in range(connect_count):
            if "Connection refused" in result:
                self.logger.info(
                    f"test_fsless_mode_repeated_entry: Connection refused after {attempt} attempts."
                )
                break

            time.sleep(10)
            try:
                path_pty = self.ssh_connect(self.safeos_password)
                assert path_pty is not None, "Connection failed: pty path is None"
                assert "/dev/pts" in path_pty, "Invalid pty path returned."

                successful_connections += 1
                self.logger.info(
                    f"Successfully connected on attempt {attempt + 1}: {path_pty}"
                )
            except paramiko.ssh_exception.NoValidConnectionsError:
                result = "Connection refused"

        self.logger.info(
            f"Total successful connections: {successful_connections} out of {connect_count}"
        )

    @pytest.mark.NVOSQ_67530
    @pytest.mark.parametrize("execute_count", [30])
    def test_execute_commands_multiple_times(self, ecu: NvosEcu, execute_count: int):
        """test execute stress safe sshd"""

        self._reboot_and_assert(ecu)
        commands = [
            "efc safe_locktrace -p {pid} -o {path_pty}",
            "efc safe_top -o {path_pty} -t 1",
            "efc safe_ps -o {path_pty} -T",
            "efc safe_showmem -o {path_pty}",
        ]

        commands_outputs = self.ssh_connect_and_execute_commands(
            commands * execute_count
        )
        assert commands_outputs is not None, "Failed to connect to the host."

        for command in commands_outputs:
            if "locktrace" in command:
                assert "memory map" in commands_outputs[command]
            if "top" in command:
                assert "Tasks" in commands_outputs[command]
            if "ps" in command:
                assert "file" in commands_outputs[command]
            if "showmem" in command:
                assert "Total" in commands_outputs[command]
            time.sleep(0.1)

    def _reboot_and_assert(self, ecu: NvosEcu):
        """assert after reboot reset"""

        ecu.execute(command="reboot")
        ecu.serial.platform.wait_until_serial_output_match(self.acore_up_flag, 50)
        time.sleep(15)
        response = ecu.serial.platform.send_command_get_response("uptime")
        assert "System" in response
        self.logger.info("wait until safe_sshd up")
        time.sleep(80)

    def _hard_reset_and_assert(self, ecu: NvosEcu):
        """assert after hard reset"""

        ecu.power_hard_reset()
        ecu.serial.platform.wait_until_serial_output_match(self.acore_up_flag, 50)
        time.sleep(15)
        out = ecu.ssh.client.execute(command="uptime")
        assert "System" in out
        self.logger.info("wait until safe_sshd up")
        time.sleep(80)

    def ssh_connect(self, password, timeout=60):
        """Connect through paramiko"""

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            self.safeos_hostname,
            port=self.safeos_port,
            username=self.safeos_username,
            password=password,
            timeout=timeout,
            look_for_keys=False,
        )
        shell = client.invoke_shell()
        time.sleep(1)
        output1 = shell.recv(1024).decode("utf-8").strip()
        match = re.search(r"(/dev/pts/\d+)", output1)
        path_pty = match.group(1) if match else None
        client.close()
        return path_pty

    def ssh_connect_and_execute_commands(self, commands):
        """connect and excute command through paramiko"""

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        timeout = 60
        client.connect(
            self.safeos_hostname,
            port=self.safeos_port,
            username=self.safeos_username,
            password=self.safeos_password,
            timeout=timeout,
            look_for_keys=False,
        )
        shell = client.invoke_shell()
        time.sleep(1)
        output1 = shell.recv(1024).decode("utf-8").strip()

        match = re.search(r"(/dev/pts/\d+)", output1)
        path_pty = match.group(1) if match else None

        commands_outputs = {}
        if path_pty:
            commands = [
                cmd.format(path_pty=path_pty, pid=self.safe_pid) for cmd in commands
            ]

            for command in commands:
                shell.send(command + "\n")
                self.logger.info(f"now run command is: {command}")
                time.sleep(1)
                output2 = self._get_full_output(shell)
                commands_outputs[command] = output2

        client.close()
        return commands_outputs

    @staticmethod
    def _get_full_output(shell):
        output = ""
        while True:
            time.sleep(0.5)
            if shell.recv_ready():
                part = shell.recv(1024).decode("utf-8")
                output += part
            else:
                break
        return output.strip()
