# -*- coding: utf-8 -*
import paramiko 
from ncclient import manager 
from ncclient import operations 
import time 
import difflib 
import re

ip = '192.168.137.100' 
ssh_user = 'python'
ssh_password = 'Huawei12#$'
netconf_port = '830'
netconf_user = 'netconf'
netconf_password = 'Huawei12#$'
filename='D:\\OneDrive\\5.code\\mygithub\\DATACOM\\综合实验\\netconf.txt'

def get_config(ip, username, password):
    ssh = paramiko.client.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ip, port=22, username=username, password=password)
    print(ip+"login ssuccesfull")
    cli = ssh.invoke_shell()
    cli.send("N\n")
    time.sleep(0.5)
    cli.send('screen-length 0 temporary\n')
    time.sleep(0.5)
    cli.send("display cu\n")
    time.sleep(2)
    dis_cu = cli.recv(999999).decode()
    return (dis_cu)
    ssh.close()


class ssh():
    def ssh_connect(ip,username,password):
        ssh = paramiko.client.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        ssh.connect(hostname=ip,port=22,username=username,password=password)
        print(ip+' login succesfully')
        return ssh
    def ssh_config(file,ip,username,password):
        a = ssh.ssh_connect(ip,username,password)
        cli = a.invoke_shell()
        cli.send('sys\n')   
        time.sleep(0.5)
        cli.send('screen-length 0 \n')
        time.sleep(0.5)
        f = open(file,'r')
        config_list = f.readlines()
        for i in config_list:
            cli.send(i)
            time.sleep(0.5)    
        dis_this = cli.recv(999999).decode()
        print ("netconf预配置完成")
        a.close()

def huawei_connect(host, port, user, password):
    return manager.connect(host=host, 
                        port=port, 
                        username=user, 
                        password=password, 
                        hostkey_verify = False, 
                        device_params={'name': "huawei"}, 
                        allow_agent = False, 
                        look_for_keys = False)
#NETCONF 发送 XML 数据，配置设备接口 IP 地址HCIP-Datacom-Network Automation Developer 实验指导手册 第 32 页
CREATE_INTERFACE = '''<config> 
    <ethernet xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0"> 
        <ethernetIfs> 
            <ethernetIf operation="merge"> 
                <ifName>GE1/0/2</ifName> 
                <l2Enable>disable</l2Enable>
            </ethernetIf> 
        </ethernetIfs>
    </ethernet> 
    <ifm xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0"> 
        <interfaces> 
            <interface operation="merge"> 
                <ifName>GE1/0/2</ifName>
                <ifDescr>Config by NETCONF</ifDescr> 
                <ifmAm4> 
                    <am4CfgAddrs> 
                        <am4CfgAddr operation="create"> 
                            <subnetMask>255.255.255.0</subnetMask> 
                            <addrType>main</addrType>
                            <ifIpAddr>192.168.2.1</ifIpAddr> 
                        </am4CfgAddr> 
                    </am4CfgAddrs>
                </ifmAm4> 
            </interface>
        </interfaces> 
    </ifm> 
</config>'''

def read_file(filename):
    try:
        with open(filename,'r') as f:
            return f.readlines()
    except IOError:
        print('%s未找到该文件'%filename)
        sys.exit(1)
def compare_files(file1, file2, out_file):
    file1_content = read_file(file1)
    file2_content = read_file(file2)
    d = difflib.HtmlDiff()
    result = d.make_file(file1_content,file2_content)
    with open (r'D:\\OneDrive\\5.code\\mygithub\\DATACOM\\综合实验\\result.html',"w") as f:
        f.writelines(result)
    print()
if __name__ == "__main__":
    # 获取当前配置
    output=get_config(ip, ssh_user, ssh_password)
    config = re.findall(r'(<ce12800>display cu[\d\D]+<ce12800>$)',output)
    with open(r'D:\\OneDrive\\5.code\\mygithub\\DATACOM\\综合实验\\conf1','w') as f: 
        f.writelines(config[0])
    
    
    # netconf配置
    ssh.ssh_config(filename,ip,ssh_user,ssh_password) 
    time.sleep(1)
    m = huawei_connect(ip,netconf_port,netconf_user,netconf_password) 
    m.edit_config(target='running',config=CREATE_INTERFACE)   

    # 再次获取配置
    output=get_config(ip, ssh_user, ssh_password)
    config = re.findall(r'(<ce12800>display cu[\d\D]+<ce12800>$)',output)
    with open(r'D:\\OneDrive\\5.code\\mygithub\\DATACOM\\综合实验\\conf2','w') as f: 
        f.writelines(config[0])

    # 对比配置
    compare_files(r'D:\\OneDrive\\5.code\\mygithub\\DATACOM\\综合实验\\conf1',r'D:\\OneDrive\\5.code\\mygithub\\DATACOM\\综合实验\\conf2', r'D:\\OneDrive\\5.code\\mygithub\\DATACOM\\综合实验\\result.html')
