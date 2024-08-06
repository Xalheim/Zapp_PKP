import paramiko
import os


def send_sessions():
    host = "192.168.197.150"
    username = input("Podaj login: ")
    password = input("Podaj haslo: ")

    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=username, password=password)

    _stdout = client.exec_command('if [ -d "UserSessions" ]; then echo "1"; else echo "0"; fi')[1]
    doesUserSessionsExist = _stdout.read().decode()
    dirExists = False
    if int(doesUserSessionsExist[0]) == 1:
        dirExists = True

    if not dirExists:
        print("UserSessions directory does not exist. Creating directory.")
        _stdout = client.exec_command('mkdir UserSessions')[1]
        print(_stdout.read().decode())
        print("Successfully created UserSessions directory")
        dirExists = True

    if dirExists:
        filesToBeSend = os.listdir("./AppCounterUserLogs")
        if len(filesToBeSend) > 0:
            print(f'List of current files to be sent out:')
            for filename in filesToBeSend:
                print(filename)
        else:
            print("No files to be sent.\n")

        for file in filesToBeSend:                                       # For every file in the directory, go through contents and send to GLPI, remove afterwards
            with open('AppCounterUserLogs/' + file, 'r') as csvfile:
                sessions = csvfile.readlines()
                sessions = sessions[1:]             # TODO delete after removing the username from session files

                for element in sessions:
                    element = element.replace("\n", "")
                    _stdout = client.exec_command("cd ./UserSessions; pwd; echo "+str(element)+" >> "+str(file))[1]

                csvfile.close()
            os.remove('AppCounterUserLogs/' + file)

        print("Successfully finished task\nShutting down")
        client.close()
