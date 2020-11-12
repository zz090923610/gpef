import paramiko
import logging

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y:%H:%M:%S',
                    level=logging.INFO)


class SSHHdl:
    def __init__(self, host, username, rsa_key_path):
        self.key = paramiko.RSAKey.from_private_key_file(rsa_key_path)
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(host, username=username, pkey=self.key, timeout=10)
        self.stdin = None
        self.stdout = None
        self.stderr = None
        self.logger = logging.getLogger('SSHHdl')

    def exec_cmd(self, cmd):
        try:
            self.stdin, self.stdout, self.stderr = self.client.exec_command(cmd, timeout=5)
            for line in self.stdout:
                self.logger.info(line.strip('\n'))
        except Exception as e:
            self.logger.error("on exec %s, %s" % (cmd, e))

    def heart_beat(self):
        self.logger.info("SSHHdl heat beat")
        try:
            self.stdin, self.stdout, self.stderr = self.client.exec_command("ls /tmp", timeout=5)
        except Exception as e:
            self.logger.error("SSHHdl heat beat failed, %s" % (e))

    def write(self, content):
        if self.stdin is not None:
            self.stdin.write(content)
        else:
            self.logger.error("stdin not open, unable to write")

    def scp_rl(self, local_path, remote_path):
        ftp_client = self.client.open_sftp()
        ftp_client.get(local_path, remote_path)
        ftp_client.close()

    def scp_lr(self, local_path, remote_path):
        ftp_client = self.client.open_sftp()
        ftp_client.put(local_path, remote_path)
        ftp_client.close()

    def close(self):
        self.client.close()
