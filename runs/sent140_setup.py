import os
import sys

try:
    os.chdir('../examples')
    if os.system("chmod +x get_data.sh") != 0:
        print("get_data.sh permissions change failed, exiting.")
        sys.exit(1)
    if os.system("sudo ./get_data.sh") != 0:
        print("get_sent140_data failed, exiting")
        sys.exit(1)
except KeyboardInterrupt:
    print("Interrupted by user, exiting.")
    sys.exit(1)

