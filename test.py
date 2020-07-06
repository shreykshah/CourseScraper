import sys
import time

print(("percent complete"), end='\r')
time.sleep(0.5)

for i in range(200):
    print("  " + (str('%.1f' % (i / 200 *100)) +  " percent complete"), end='\r')

    # sys.stdout.flush()
    time.sleep(0.5)

print("\ntests")
