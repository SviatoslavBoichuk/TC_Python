#!/usr/bin/env python

"""Application reads packets from the input file and
generates output files with packets seperated by addresantss,
according to task"""

from sys import argv
import os

# Main function return one of folowing code:
# 0 if application finished success, otherwise return -1
EXIT_SUCCESS = 0
EXIT_FAILURE = -1

# pass file name to main function
NUM_INPUT_PARAMS = 2

# map that contain addresantss and their packets"""
contacts = {'Ivan': [], 'Dmythro': [], 'Ostap': [], 'Lesya': []}
packets = []


# Check if count of input params is less then 2
def check_input_params():
    return len(argv) == NUM_INPUT_PARAMS


# Function check if file with packets exits
# If exist - return true, else return false
def check_exist(
        file_path):
    return os.path.isfile(file_path)


# Read packets from input file
def get_packets(file_name, packs):
    with open(file_name, "r") as file_obj:
        packs = file_obj.readlines()


# parse packet to addresantss
def parse_file(
        packets):

        for line in packets:
            if line.split()[-1] == 'end':
                contacts['Lesya'].append(line)

            if len(line) % 2 == 0:
                contacts['Ivan'].append(line)
            elif len(line) % 2 == 1 and line[0].isupper():
                contacts['Dmythro'].append(line)
            else:
                contacts['Ostap'].append(line)


# Write parsed packets to file
def write(file_name, packet):
    with open(file_name, "w+") as file_obj:
        for line in packet:
            line = line.rstrip("\n")
            if line != "\n":
                file_obj.write(line)


def main():
    main_return_code = EXIT_FAILURE

    if check_input_params():
        file_name = argv[1]
    else:
        print ("error")
        return EXIT_FAILURE

    if check_exist(file_name):
        # read packets from file
        get_packets(file_name, packets)
        parse_file(packets)
        write_files_name = contacts.keys()

        for out_file_name in write_files_name:
            write(out_file_name+'.txt', contacts[out_file_name])
        main_return_code = EXIT_SUCCESS
    else:
        main_return_code = EXIT_FAILURE

    return main_return_code

if __name__ == '__main__':
    main()
