import subprocess
import datetime

"""
The blacklist is used to specifically block certain processes, ex. powershell that runs every check"""
blacklist = list()
blacklist.append("powershell")
"""
activate_process_scan is responsible for querying the processes list, and providing the results in a convenient format.
It checks for duplicate processes and takes the longest running one (still limited by program runtime before sending).
"""
def activate_process_scan():
    command = "Get-Process | Where-Object { $_.SessionId -ne 0 -and $_.starttime} | Select-Object ProcessName, starttime"   # Get processes that mostly do not belong to system (SID != 0)
    query = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)                        # Execute process search

    process_list = list()                                                                                                   # List for the final processes
    requested_processes = list()                                                                                            # List for processes from query

    for line in query.stdout.splitlines():                                                                                  # Read all requested processes
        if line:
            requested_processes.append(line)                                                                                # Add all processes to a list, as long as it's not empty
    requested_processes = requested_processes[3:]                                                                           # Remove the first two info lines, to get clean data

    for ps_process in requested_processes:                                                                                  # Go through every given process
        ps_process = ps_process.split()                                                                                     # Split to deal with whitespaces
        wasReplaced = False
        for saved_process in process_list:
            if ps_process[0:len(ps_process)-2] == saved_process[0:len(ps_process)-2]:                                       # Has the process already been added? If so, make sure the bigger start_time stays (TODO THIS MIGHT BREAK MONITORING FOR APPS THAT STAY OPEN IN THE BACKGROUND EVEN WHEN CLOSED, TO CONSULT WITH ADMIN)
                time_one = ps_process[-2] + " " + ps_process[-1]                                                            # Create compatible datetime format
                time_two = saved_process[-2] + " " + saved_process[-1]                                                      # Create compatible datetime format
                time_one = datetime.datetime.strptime(time_one, '%d.%m.%Y %H:%M:%S')                                # Create datetime for comparison
                time_two = datetime.datetime.strptime(time_two, '%d.%m.%Y %H:%M:%S')                                # Create datetime for comparison
                wasReplaced = True                                                                                          # Process already exists in the list, so it will be blocked from duplicated append
                if time_one < time_two:                                                                                     # New time passed was bigger than the current one
                    count_proc_pos = 0
                    for values in process_list:                                                                             # Get index to replace old value
                        if ps_process[0:len(ps_process)-2] == values[0:len(ps_process)-2]:
                            process_list[count_proc_pos] = ps_process                                                       # Replace old value with new
                            break                                                                                           # Prevent further comparions
                        count_proc_pos += 1
        if not wasReplaced:                                                                                                 # If there was no duplicate, add to saved processes
            process_list.append(ps_process)

    final_list = list()

    for final_process in process_list:
        final_list.append([' '.join(final_process[0:len(final_process)-2]), datetime.datetime.strptime(final_process[-2] + " " + final_process[-1], '%d.%m.%Y %H:%M:%S')])     # First argument is all the process names combined, second argument is two date parts combined into one datetime
    return final_list

"""
check_processes uses current_process_list to get a current list of processes, and uses it to compare to past processes.
Returns active_processes, a list containing currently running processes, as well as disabled_processes, a list containing
currently not running processes, that were recorded beforehand.
"""
def check_processes(past_process_list):
    current_process_list = activate_process_scan()                                                                      # Refer to main process scan function to get current data
    active_processes = list()
    disabled_processes = list()
    for past_process in past_process_list:
        if past_process[0] in blacklist:
            pass
        elif past_process not in current_process_list:                                                                    # If process ran before but is not found anymore, it gets added to the disabled_processes list
            disabled_processes.append(past_process)
        else:
            active_processes.append(past_process)                                                                       # Currently running processes are added to the active_processes list

    return active_processes, disabled_processes