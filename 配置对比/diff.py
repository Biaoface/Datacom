# -*- coding: utf-8 -*
import paramiko 
import time 
import difflib 
import re

ip = '192.168.137.100' 
username='python' 
password='Huawei12#$'

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

def ssh_config(ip, username, password):
    ssh = paramiko.client.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ip, port=22, username=username, password=password)
    print(ip+"login ssuccesfull")

    cli = ssh.invoke_shell()
    cli.send("sys\n")
    time.sleep(0.5)
    cli.send('screen-length 0 temporary\n')
    time.sleep(0.5)
    cli.send("int g1/0/2\n")
    time.sleep(0.5)
    cli.send("ip add 1.1.1.2 24\n")
    time.sleep(0.5)
    cli.send("comm\n")
    dis_cu = cli.recv(999999).decode()
    ssh.close()
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
    with open (r'D:\\OneDrive\\5.code\\mygithub\\DATACOM\\配置对比\\result.html',"w") as f:
        f.writelines(result)
    print()

if __name__ == "__main__":
    output=get_config(ip, username, password)
    config = re.findall(r'(<CE1>display cu[\d\D]+<CE1>$)',output)
    with open(r'D:\\OneDrive\\5.code\\mygithub\\DATACOM\\配置对比\\file1','w') as f: 
        f.writelines(config[0])
    ssh_config(ip,username,password)
    output = get_config(ip,username,password)
    config = re.findall(r'(<CE1>display cu[\d\D]+<CE1>$)',output)
    with open(r'D:\\OneDrive\\5.code\\mygithub\\DATACOM\\配置对比\\file2','w') as f: 
        f.writelines(config[0])
    compare_files(r'D:\\OneDrive\\5.code\\mygithub\\DATACOM\\配置对比\\file1',r'D:\\OneDrive\\5.code\\mygithub\\DATACOM\\配置对比\\file2',r'D:\\OneDrive\\5.code\\mygithub\\DATACOM\\配置对比\\result.html')
