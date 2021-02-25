import paramiko
import time
from pysnmp.hlapi import *

# 交换机信息
ip = "192.168.137.100"
username = "python"
password = "Huawei12#$"

# ssh 登陆

ssh = paramiko.client.SSHClient()
ssh.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
ssh.connect(hostname=ip, port=22, username=username, password=password)
print(ip+"登陆成功！")

# 打开channel,输入配置

cli = ssh.invoke_shell()
cli.send('N\n')
time.sleep(0.5)
cli.send('screen-length 0 temporary\n')
time.sleep(0.5)

# 进入系统视图

cli.send("system-view immediately\n")
time.sleep(0.5)
# 读取配置逐行写入

# 建立snmp通道
UdpTransportTarget((ip,161))
g = getCmd(SnmpEngine(),

# 获取设备主机名
UsmUserData("admin", "Huawei12#$", "Huawei12#$", authProtocol=usmHMACSHAAuthProtocol, privProtocol=usmAesCfb128Protocol),
    UdpTransportTarget((ip, 161)),
    ContextData(),
    ObjectType(ObjectIdentity("SNMPv2-MIB", "sysName",0)))
errirIndication, errorStatus, errorIndex, varBinds=next(g)
for i in varBinds:
    print(i)
    print(str(i).split("=")[1].strip())
dis_this = cli.recv(999999).decode()
ssh.close()
