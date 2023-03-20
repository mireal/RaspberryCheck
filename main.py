from win10toast import ToastNotifier
import subprocess
import paramiko
from config import hostname, port, username, password, scriptdir

toaster = ToastNotifier()


# SSH connection
def check_script():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, port=port, username=username, password=password)

    stdin, stdout, stderr = ssh.exec_command("ps -aux | grep main.py")  # Check for the script

    output = stdout.read().decode()  # Read the output
    ssh.close()
    return output


# Ping RPi
response = subprocess.Popen(["ping", "-n", "2", "-w", "500", hostname], stdout=subprocess.PIPE).stdout.read().decode(
    "cp866")

# print(response)


if "Приблизительное время приема-передачи" in response:

    output = check_script()

    if scriptdir in output:
        message = "The script is running."
    else:
        message = "Warning! The script is not running."

    toaster.show_toast("RPi is up and running.", message, duration=60)

else:
    toaster.show_toast("RPi is not responding!", "Something Wrong", duration=60)
