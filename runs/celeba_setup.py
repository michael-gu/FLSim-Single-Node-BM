import os
import sys

try:
    os.chdir('../examples')
    if os.system("git clone https://github.com/TalwalkarLab/leaf.git") != 0:
        sys.exit(1)
    if os.system("cd leaf/data/celeba || exit") != 0:
        sys.exit(1)
    if os.system("./preprocess.sh --sf 1.0 -k 0 -iu 1 -s niid -t 'user' --tf 0.90 --spltseed 1") != 0:
        sys.exit(1)
except KeyboardInterrupt:
    print("Interrupted by user, exiting.")
    sys.exit(1)