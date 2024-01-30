import os
import sys

command = "python3 cifar10_example.py --config-file configs/cifar10_config.json"

# make sure to set up config file and cifar10 file accordingly

try:
    for _ in range(60):
        if os.system(command) != 0:
            print("Command failed, exiting.")
            sys.exit(1)
except KeyboardInterrupt:
    print("Interrupted by user, exiting.")
    sys.exit(1)