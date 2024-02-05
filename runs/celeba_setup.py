import os
import sys

try:
    os.chdir('..')
    if os.system("pip install gdown") != 0:
        sys.exit(1)
    if os.system("export PATH=$PATH:/usr/local/bin") != 0:
        sys.exit(1)
    if os.system("source ~/.bashrc") != 0:
        sys.exit(1)
    os.chdir('examples')
    if os.system("git clone https://github.com/TalwalkarLab/leaf.git") != 0:
        sys.exit(1)
    if os.system("cd leaf/data/celeba || exit") != 0:
        sys.exit(1)
    if os.system("mkdir data") != 0:
        sys.exit(1)
    if os.system("cd data") != 0:
        sys.exit(1)
    if os.system("mkdir raw") != 0:
        sys.exit(1)
    if os.system("cd raw") != 0:
        sys.exit(1)
    if os.system("gdown --id 1ddExVxD2eVXxBjLWiAMzuknSdsPk-kIC -O identity_CelebA.txt") != 0:
        sys.exit(1)
    if os.system("gdown --id 1ZMxD7fcgID_LdMwAHy5x2OjqlkzCLY2X -O list_attr_celeba.txt") != 0:
        sys.exit(1)
    if os.system("gdown --id 1VAWOZ6aFn6jE4tbhc8brIMeIxSU1HOm6 -O image_align_celeba.zip") != 0:
        sys.exit(1)
    if os.system("unzip image_align_celeba.zip") != 0:
        sys.exit(1)
    if os.system("./preprocess.sh --sf 1.0 -k 0 -iu 1 -s niid -t 'user' --tf 0.90 --spltseed 1") != 0:
        sys.exit(1)
except KeyboardInterrupt:
    print("Interrupted by user, exiting.")
    sys.exit(1)