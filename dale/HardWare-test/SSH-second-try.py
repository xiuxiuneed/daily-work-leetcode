import paramiko
import time
def ssh_connect(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, password=password)
        print("SSH connection established with " + hostname)
        # 保持连接
        while True:
            stdin,stdout,stderr = client.exec_command("echo 'keep alive'")
            time.sleep(5)

    except paramiko.AuthenticationException as auth_exception:
        print("身份验证失败:", str(auth_exception))
    except paramiko.SSHException as ssh_exception:
        print("SSH 连接错误:", str(ssh_exception))
    except paramiko.Exception as e:
        print("错误:", str(e))
    finally:
        client.close()

hostname = '10.160.254.23'
port = 22
username = 'nio'
password = 'NIO3200#'

ssh_client = ssh_connect(hostname, username, password)
# if ssh_client:
#     print("SSH已经建立")
#     command = [
#         # "ps",  # 列出当前目录中的文件和文件夹
#         # "pwd",  # 显示当前工作目录的路径
#         # "whoami",  # 显示当前用户
#         # "df -h",
#         # ""
#         # "nmap - p "
#     ]
#     for command in command:
#         stdin, stdout, stderr = ssh_client.exec_command(command)
#         print(f"执行命令{command}")
#         print(stdout.read().decode())
#
#     # ssh_client.close()
#     print("SSH 连接已关闭")
# else:
#     print("无法建立 SSH 连接")