import paramiko
import time

def ssh_connect(hostname, port, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname,port=port, username=username, password=password)
        return client
    except paramiko.AuthenticationException as auth_exception:
        print("身份验证失败:", str(auth_exception))
    except paramiko.SSHException as ssh_exception:
        print("SSH 连接错误:", str(ssh_exception))
    except paramiko.Exception as e:
        print("错误:", str(e))

# SSH 连接参数
hostname = '10.110.192.196'
username = 'nio'
password = 'NIO3200#'

# SSH 连接
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, username=username, password=password)
if ssh:
    print("连接成功")

# 执行 telnet 命令并输入指令
chan = ssh.invoke_shell()
chan.send('telnet 172.20.10.1\n')
time.sleep(5)
chan.send('ls -hlR\n')
chan.send('exit\n')
# 接收返回信息
output = ''
while not chan.exit_status_ready():
    if chan.recv_ready():
        output += chan.recv(1024).decode('utf-8')

# 打印返回信息
print(output)

# 关闭 SSH 连接
ssh.close()