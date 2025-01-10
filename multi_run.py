import os
import time

time_period = 60 * 10 # 10 minutes
# set the time_period to 60 * 60 for 1 hour
# set the time_period to 60 * 60 * 24 for 1 day
# set the time_period to 60 * 60 * 24 * 7 for 1 week
# set the time_period to 60 * 60 * 24 * 30 for 1 month
# set it as you like

while True:
    print('[+] --- Starting the script' + '\n')
    start_time = time.time()
    os.system('python single_run.py')
    elapsed_time = time.time() - start_time
    print(f'[+] --- Script finished. Taken {elapsed_time} seconds' + '\n')
    print(f'[+] --- Waiting for {max(0, time_period - elapsed_time)} seconds' + '\n')

    time.sleep(max(0, time_period - elapsed_time))
