#! usr/bin/python
# _*_ coding=utf-8 _*_
'''
@time: 2018/2/5 16:48
@author: jiangzeyu5
'''

import paramiko


def connect(host, username, password):
    ssh = paramiko.SSHClient()  # 仅仅是执行命令无法上传下载
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, 22, username=username, password=password, allow_agent=False, look_for_keys=False)
        return ssh
    except:
        return print('登录异常')


def sftp_down_file(server_path, local_path):
    try:
        t = paramiko.Transport((host, 22))
        t.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.get(server_path, local_path)
        t.close()
    except Exception as e:
        print(e)


def sftp_upload_file(server_path, local_path):
    try:
        t = paramiko.Transport((host, 22))
        t.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(server_path, local_path)
        t.close()
    except Exception as e:
        print(e)


def exec_commands(conn, cmd):
    stdin, stdout, stderr = conn.exec_command(cmd)
    results = stdout.readlines()  # .decode('utf-8')
    return results


def write_in(name, results):
    filename = name + '.txt'
    with open(filename, 'a', encoding='utf-8') as f:
        result = ' '.join(results)
        f.write(result)
        f.close()


if __name__ == '__main__':
    host = '10.100.60.216'                        #传入监控主机IP
    username = 'hik'                              #传入登录用户名
    password = 'Hik@cloud'                        #传入登录密码

    # 前半部单个命令测试
    # path = 'cd /dev/sda1'
    # cmd = 'df -h'
    # conn = connect(host, username, password)
    # #exec_commands(conn, path)
    # res = exec_commands(conn, cmd)
    # print(res)

    # #从服务器下载测试
    # server_path ='install_agent.sh'
    # local_path = 'C:/Users/jiangzeyu5/Desktop/install_agent.sh'
    # sftp_down_file(server_path, local_path)

    # 多命令
    conn = connect(host, username, password)               #执行connect函数，建立所在的连接
    cmd = ['date', 'free -m', 'df -h', 'top -bn 1 -i -c']  #设置监控的命令(list格式：时间、内存、磁盘空间、CPU使用情况等可扩展)
    for m in cmd:
        res = exec_commands(conn, m)                       #依次执行exec_commands函数，传入所在连接conn及监控命令m，返回结果变量res
        write_in('E:/test', res)