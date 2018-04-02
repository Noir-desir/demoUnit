#! usr/bin/python
# _*_ coding=utf-8 _*_
'''
@time: 2018/2/6 14:30
@author: jiangzeyu5
'''

import paramiko


class SSHConnect():
    def __init__(self, host, usr, pwd):
        self._host = host
        self._usr = usr
        self._pwd = pwd
        self._transpot = None
        self._sftp =None
        self._client = None
        self._connect()

    def _connect(self):
        # 定义私有方法，外部无法访问
        try:
            transport = paramiko.Transport((self._host, 22))
            transport.connect(username=self._usr, password=self._pwd)
            self._transpot = transport
        except Exception as e:
            print('登陆异常', e)

    def download(self, server_path, local_path):
        try:
            if self._sftp is None:
                self._sftp = paramiko.SFTPClient.from_transport(self._transpot)
            self._sftp.get(server_path, local_path)
        except Exception as e:
            print(e)

    def upload(self,server_path, local_path):
        try:
            if self._sftp is None:
                self._sftp = paramiko.SFTPClient.from_transport(self._transpot)
            self._sftp.put(local_path, server_path)
        except Exception as e:
            print(e)

    def exec_command(self, command):
        if self._client is None:
            self._client = paramiko.SSHClient()
            self._client._transport = self._transpot
        stdin, stdout, stderr = self._client.exec_command(command)
        results = stdout.readlines()  # .decode('utf-8')
        if len(results) > 0:
            result = ' '.join(results)    #将结果链接成字符串
            print(result)
            return result
        err = stderr.readlines()
        if len(err) > 0:
            print(err)
            return err

    def close(self):
        if self._transpot:
            self._transpot.close()
        if self._client:
            self._client.close()

    def write_in(self, name, result):
        filename = name + '.txt'
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(result+'\n'+'~'*10+'\n')
            f.close()

if __name__ == '__main__':

    host = '10.100.60.XX'
    usr = 'XXX'
    pwd = 'XXX'


    #conn._download('install_agent.sh', 'C:/Users/jiangzeyu5/Desktop/install_agent.sh')

    conn = SSHConnect(host, usr, pwd)
    cmd = ['date', 'free -m', 'df -h', 'top -bn 1 -i -c', 'ls']  # 'cat /proc/meminfo'
    for m in cmd:
        res = conn.exec_command(m)
        conn.write_in('name', m+'\n'+res)

    # conn = SSHConnect(host, usr, pwd)
    # conn.exec_command('cd /home;pwd')
    # conn.write_in('name')
    # conn.exec_command('pwd')
    # conn.write_in('name')
    #
    # conn.close()