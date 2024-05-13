import telnetlib

HOST = "10.160.254.23"
PORT = 23  # 默认 Telnet 端口
USERNAME = "nio"
PASSWORD = "NIO3200#"

# 创建 Telnet 连接
tn = telnetlib.Telnet(HOST, PORT)

# 登录认证
tn.read_until(b"login: ")
tn.write(USERNAME.encode('utf-8') + b"\n")
tn.read_until(b"Password: ")
tn.write(PASSWORD.encode('utf-8') + b"\n")

# 执行命令
commands = [
    "ps",       # 列出当前目录中的文件和文件夹
    "pwd",      # 显示当前工作目录的路径
    "whoami",   # 显示当前用户
    "df -h",    # 显示磁盘使用情况
]

for command in commands:
    tn.write(command.encode('utf-8') + b"\n")
    result = tn.read_until(b"$").decode('utf-8')  # 读取输出结果，假设命令提示符为"$"
    print(f"Command: {command}")
    print(result)

# 关闭 Telnet 连接
tn.close()