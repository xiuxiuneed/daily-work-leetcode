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


port = 22
hostname = '10.110.192.196'
username = 'nio'
password = 'NIO3200#'

ssh_client = ssh_connect(hostname, port, username, password)
if ssh_client:
    print("SSH已经建立")
    chan = ssh_client.invoke_shell()
    chan.send('telnet 172.20.10.1\n')
    time.sleep(5)
    output = ''
    while not chan.exit_status_ready():
        if chan.recv_ready():
            output += chan.recv(1024).decode('utf-8')
    chan.send('ls -hlR\n')
    time.sleep(5)

    chan.send('^]\n')
    chan.send('exit\n')

    ssh_client.close()
    print("SSH 连接已关闭")
else:
    print("无法建立 SSH 连接")
