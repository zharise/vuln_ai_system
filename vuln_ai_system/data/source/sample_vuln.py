import subprocess

def handler(cmd):
    return subprocess.check_output(cmd, shell=True)

