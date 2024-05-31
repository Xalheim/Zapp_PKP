import os
import csv
import psutil
import datetime
import time
import keyboard


def check_process_runtime(process_name):
    for proc in psutil.process_iter(['pid', 'name', 'create_time']):  # loop checks every process running
        if proc.info['name'] == process_name:
            return True, datetime.datetime.fromtimestamp(proc.info['create_time'])  # returns True if process exists and time of process activation
    return False, None


def save_runtime_to_file(app_name, runtime_start, file_name):

    app_name = process_name_list[process_list.index(app_name)].split(";")[0]    # Change name back to licensed one

    with open('AppCounterUserLogs/' + file_name, 'r') as file:
        lines = file.readlines()

    with open('AppCounterUserLogs/' + file_name, 'w') as file:  # file update
        file.writelines(lines)
        file.writelines(f"{app_name},{str(runtime_start)},{str(datetime.datetime.now())}\n")


def load_runtimes_from_file(file_name):
    try:
        with open('AppCounterUserLogs/' + file_name, 'r') as file:
            times = [line.strip().split(",")[3] for line in file.readlines()]
            return times
    except FileNotFoundError:
        return []


if __name__ == "__main__":

    if not os.path.isdir('AppCounterUserLogs'):
        os.mkdir('AppCounterUserLogs')

    if not os.path.isfile('RuntimeAddonData.csv'):
        print("RuntimeAddonData.csv does not exist, please read processes from GLPI Agent")  # processes have not been dowloaded from GLPI agent, have to download processes and reset app
        exit(1)

    with open("RuntimeAddonData.csv", 'r') as csvfile:
        output = [line.strip() for line in csvfile.readlines()]         # read all processes from csv file
        username = output[0]
        process_name_list = output[1:]

    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    file_name = f'{str(username)}__{str(today_date)}__Runtime.csv'

    if not os.path.isfile("AppCounterUserLogs/"+file_name):     # TODO in the actual app make a timer that reloads process_list periodically
        with open('AppCounterUserLogs/'+file_name, 'w', newline='') as newfile:
            writer = csv.writer(newfile)
            newfile.write(username+'\n')

    if not os.path.isfile('ProcessConverter.csv'):
        print("ProcessConverter.csv does not exist")
        exit(1)

    with open('ProcessConverter.csv', 'r') as csvfile:      # Convert licenses to executable names
        NameToExecList = [line.strip() for line in csvfile.readlines()]

    print(f'Loaded user {username}, loading processes...\n')

    process_list = []

    try:
        for process_name in process_name_list:
            for line in NameToExecList:
                if process_name == line.split(";")[0]:
                    process = line.split(";")[1]
                    print(process)
                    process_list += [process]   # TODO, for some reason it appends the \n
    except NameError:
        print("A Process Name exists that has not been found in the ProcessConverter.csv list, please update to newest version to accomodate the new license\n")

    process_count = len(process_list)

    running_apps = [False] * process_count
    past_apps = [False] * process_count
    current_runtime = [0] * process_count
    past_time = [0] * process_count

    for process in process_list:
        position = process_list.index(process)
        running_apps[position], current_runtime[position] = check_process_runtime(process)

    print("\nStarting application.\n")

    while True:

        for process in process_list:
            process_index = process_list.index(process)

            if not running_apps[process_index] and past_apps[process_index]:  # if process is off but it was active before, commence save
                past_apps[process_index] = False
                save_runtime_to_file(process, past_time[process_index], file_name)
                print(f'{process} has closed. Runtime saved to {file_name}.\n')

            past_apps[process_index] = running_apps[process_index]
            past_time[process_index] = current_runtime[process_index]
            running_apps[process_index], current_runtime[process_index] = check_process_runtime(process)

            if keyboard.is_pressed("space"):    # TODO Make functional app stop (final exec)
                for process_final in process_list:
                    process_index_final = process_list.index(process_final)
                    if running_apps[process_index_final]:
                        save_runtime_to_file(process_final, past_time[process_index_final], file_name)
                        print(f'{process_final} has closed. Runtime saved to {file_name}.\n')
                print("Stopping application\n")
                exit(0)
        time.sleep(1)
        print()
