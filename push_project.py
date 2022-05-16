import paramiko
from decouple import config

BASE_COMMAND = "source /home/c/ci34005/django_lock/myenv/bin/activate &&" \
               " cd /home/c/ci34005/django_lock/public_html/ttlock/ "
COMMAND = [
    " && git pull",
    " && pip install -r requirements.txt",
    " && python manage.py migrate"
]

host = config("HOST_TIME_WEB")
user = config("USER_TIME_WEB")
secret = config("SECRET_TIME_WEB")
port = config("PORT_TIME_WEB")


def run_command(command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Подключение
    client.connect(hostname=host, username=user, password=secret, port=port)
    stdin, stdout, stderr = client.exec_command(command)
    # # Читаем результат
    data = stdout.read().decode() + stderr.read().decode()

    print(data)
    client.close()


def done_command(command=""):
    if not command:
        # Выполнение команды
        for el in COMMAND:
            command += el
    run_command(BASE_COMMAND + command)


if __name__ == '__main__':
    done_command()
