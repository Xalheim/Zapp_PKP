import paramiko
import os

"""
send_sessions function is responsible for sending sessions to a remote host.
The user will have to input the username and password for the remote host (ip at later implementation).
The function attempts to create a directory for the files if one does not exist.
Afterwards it sends over all the data stored locally, and upon being successfully sent, it removes it from the PC.
"""
def send_sessions():
    host = "192.168.197.150"                                                                                            # TODO upon server setup, set host ip to "input" function instead of static variable
    username = input("Podaj login: ")
    password = input("Podaj haslo: ")

    client = paramiko.client.SSHClient()                                                                                # Setup functionality for SSH connection
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())                                                        # Tell paramiko what to do if there's no host key policy
    client.connect(host, username=username, password=password)                                                          # Initialize connection to server

    _stdout = client.exec_command('if [ -d "/var/www/html/glpi/plugins/softplg/UserSessions" ]; then echo "1"; else echo "0"; fi')[1]                      # Check if directory for user sessions exists
    doesUserSessionsExist = _stdout.read().decode()                                                                     # This functioon will read output from server
    dirExists = False
    if int(doesUserSessionsExist[0]) == 1:
        dirExists = True

    if not dirExists:
        print("UserSessions directory does not exist. Please make sure that the softplg plugin is installed in the GLPI agent.")
        client.close()
        raise FileNotFoundError

    else:                                                                                                               # Main code for file sending
        filesToBeSend = os.listdir("./AppCounterUserLogs")                                                              # Check if files exist
        if len(filesToBeSend) > 0:
            print(f'List of currently stored files:')
            for filename in filesToBeSend:
                print(filename)                                                                                         # Information for the user about how many files need to be sent
        else:
            print("No files to be sent.\n")

        for file in filesToBeSend:                                                                                      # For every file in the directory, go through contents and send to the server
            with open('AppCounterUserLogs/' + file, 'r') as csvfile:
                sessions = csvfile.readlines()
                print(f"Trying to send file {file}.\n")
                for element in sessions:
                    element = element.replace("\n", "")
                    _stdout = client.exec_command("cd /var/www/html/glpi/plugins/softplg/UserSessions; pwd; echo "+str(element)+" >> "+str(username)+"__"+str(file))[1]  # Set directory to UserSessions, send data (element) to file (username__file) TODO Needs write privileges for everyone, potential point of attack for hostile party
                    print(_stdout.read().decode())
                csvfile.close()
            os.remove('AppCounterUserLogs/' + file)                                                                     # Remove file if successful TODO delete after some time

        print("Successfully finished task\nShutting down")
        client.close()                                                                                                  # Sever connection to server
