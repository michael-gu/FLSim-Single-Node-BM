import os
import sys
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("dataset", help="dataset")
parser.add_argument("mode", help="Mode to run the script in. 'true' or 'test'.")
parser.add_argument("range_value", type=int, nargs='?', default=1, help="The range value to use in the loop.")
args = parser.parse_args()

# Set the command based on the mode argument
dataset = str(args.dataset)
if args.mode == "true":
    command = "sudo python3 " + dataset + "_example.py --config-file configs/" + dataset + "_config_with_feature.json"
    try:
        os.chdir('../examples')
        for _ in range(args.range_value):
            if os.system(command) != 0:
                print("Command failed, exiting.")
                sys.exit(1)
    except KeyboardInterrupt:
        print("Interrupted by user, exiting.")
        sys.exit(1)
elif args.mode == "false":
    command = "sudo python3 " + dataset + "_example.py --config-file configs/" + dataset + "_config_without_feature.json"
    try:
        os.chdir('../examples')
        for _ in range(args.range_value):
            if os.system(command) != 0:
                print("Command failed, exiting.")
                sys.exit(1)
    except KeyboardInterrupt:
        print("Interrupted by user, exiting.")
        sys.exit(1)
else:
    print(f"Invalid mode: {args.mode}")
    sys.exit(1)