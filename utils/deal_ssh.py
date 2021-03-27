#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : deal_ssh.py
# @Author: itnoobzzy
# @Date  : 2021/3/23
# @Desc  : 连接主机操作工具类

import paramiko


class SSHConnection:
    """SSH连接主机操作工具类"""

    def __init__(self, host='', port=22, username='', pwd=''):
        self.host = host
        self.port = port
        self.username = username
        self.pwd = pwd
        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.host, self.port, self.username, self.pwd)  # 连接服务器
        self.ssh_sftp = self.ssh.open_sftp()

    def close(self):
        """断开连接"""
        self.ssh_sftp.close()
        self.ssh.close()

    def upload(self, local_path, target_path):
        """
        上传文件
        :param local_path: 本地路径
        :param target_path: 远程路径
        :return:
        """
        self.ssh_sftp.put(local_path, target_path)

    def download(self, remote_path, local_path):
        """
        下载文件
        :param remote_path: 远程路径
        :param local_path: 本地路径
        :return:
        """
        self.ssh_sftp.get(remote_path, local_path)

    def cmd(self, command):
        """
        执行主机命令
        :param command: 命令
        :return:
        """
        stdin, stdout, stderr = self.ssh.exec_command(command)
        try:
            result = stdout.read().decode('gbk', errors='ignore')
        except:
            result = stdout.read().decode('utf-8', errors='ignore')
        return result


if __name__ == '__main__':
    ssh = SSHConnection(host='127.0.0.1', port=22, username='root', pwd='')
    # # git@github.com:itnoobzzy/auto_test_scripts_rep.git@master-test_hello-test_hello.sh
    # print(ssh)
    # # self.ssh.cmd(f"cd {SCRIPT_PATH};git clone {git_path};git checkout {branch}")
    # print(ssh.cmd("cd /home;git clone git@github.com:itnoobzzy/auto_test_scripts_rep.git;"))



