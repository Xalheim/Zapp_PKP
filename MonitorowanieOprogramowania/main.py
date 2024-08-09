import os
import csv
import datetime
import time
import keyboard
from FileSendoff import send_sessions
from ProcessScan import activate_process_scan, check_processes


def save_runtime_to_file(save_process_list, runtime_start, file_name):

    with open('AppCounterUserLogs/' + file_name, 'r') as file:                                                          # Copy over old contents
        lines = file.readlines()
        file.close()

    with open('AppCounterUserLogs/' + file_name, 'w') as file:
        file.writelines(lines)
        for save_process in save_process_list:                                                                          # Check which time is longer, if process runs longer than the Monitoring App, set value at the Monitoring App runtime
            if save_process[1] < runtime_start:
                save_process[1] = runtime_start.strftime('%Y-%m-%d %H:%M:%S')
            else:
                save_process[1] = datetime.datetime.strptime(save_process[1] + " " + save_process[2], '%Y-%m-%d %H:%M:%S')

            print(save_process)                                                                                         # TODO DEBUG PRINT
            file.writelines(f"{save_process[0]},{save_process[1]},{str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}\n")                    # Save to csv file

        file.close()


if __name__ == "__main__":

    programStartTime = datetime.datetime.now()                                                                          # Take current time for later checks

    if not os.path.isdir('AppCounterUserLogs'):                                                                         # If such folder does not exist, create a folder to keep csv files
        os.mkdir('AppCounterUserLogs')

    today_date = datetime.datetime.now().strftime("%Y-%m-%d")                                                           # Take current time for csv file naming
    file_name = f'{str(today_date)}__Runtime.csv'                                                                       # Set file name for later use and updates

    if not os.path.isfile("AppCounterUserLogs/"+file_name):                                                             # Create todays csv file if it doesn't exist yet
        with open('AppCounterUserLogs/'+file_name, 'w', newline='') as newfile:
            writer = csv.writer(newfile)
            newfile.write('')                                                                                           # Write nothing, so nothing breaks during process saving
            newfile.close()

    print(f'Loading processes...')

    process_list = activate_process_scan()                                                                              # Call function that returns current active, non-WindowsOS, processes

    print("Processes loaded.\nStarting application.\n")

    while True:                                                                                                         # Run program until ctrl is pressed, at which point it will attempt a save, send, and quit

        active_processes, disabled_processes = check_processes(process_list)                                            # Call function that analyses past and current processes
        process_list = active_processes                                                                                 # New process list consists of currently running processes
        save_runtime_to_file(disabled_processes, programStartTime, file_name)                                           # Old process list consists of past running processes that do not run anymore, Call function to save such process data to the csv file
        print(f'Active processes:\n{active_processes}\n')
        print(f'Disabled Processes:\n{disabled_processes}\n')
        if keyboard.is_pressed("ctrl"):                                                                                 # Ctrl program stop check
            print("Session monitoring stopped, attempting to save data.\n")
            save_runtime_to_file(active_processes, programStartTime, file_name)                                         # Call function to save currently running processes
            print("Data saved successfully, attempting to send data to server.\n")
            send_sessions()                                                                                             # Go to FileSendoff.py, and initiate the file sending procedure
            exit(0)

        timer = 10                                                                                                      # Set delay time
        print(f"Timer of {timer} seconds started.")
        count = 0
        while count < timer+1:                                                                                          # The Monitoring Program will run in delays to not cause performance issues
            count += 1
            time.sleep(1)
            print("Checking in {} seconds...".format(timer+1-count))
            if keyboard.is_pressed("ctrl"):                                                                             # Ctrl program stop check
                print("Session monitoring stopped, attempting to save data.\n")
                save_runtime_to_file(active_processes, programStartTime, file_name)                                     # Call function to save currently running processes
                print("Data saved successfully, attempting to send data to server.\n")
                send_sessions()                                                                                         # Go to FileSendoff.py, and initiate the file sending procedure
                exit(0)
        print(f'Slept for {timer} seconds.\nCommencing next scan.\n')
