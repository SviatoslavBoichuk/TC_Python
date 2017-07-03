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
FILE_READ_MODE = "r"
FILE_WRITE_MODE = "w+"
FILE_EXTEND = '.txt'
END_STR = 'end'
NEW_LINE_SYMBOL = '\n'

# pass file name to main function
NUM_INPUT_PARAMS = 2

# map that contain addresantss and their packets"""
contacts = {'Ivan': [], 'Dmytro': [], 'Ostap': [], 'Lesya': []}


# Check if count of input params is less then 2
def check_input_params():
    return len(argv) == NUM_INPUT_PARAMS


# Function check if file with packets exits
# If exist - return true, else return false
def check_exist(
        file_path):
    return os.path.isfile(file_path)


# Read packets from input file
def get_packets(file_name):
    packets = []
    with open(file_name, FILE_READ_MODE) as file_obj:
        packets = [packet.rstrip(NEW_LINE_SYMBOL) for packet in file_obj.readlines() if packet != NEW_LINE_SYMBOL]
    return packets


# parse packet to addresantss
def parse_file(
        packets):

        # if packet is no Ivan, or Dmytro or Lesya, then
        # this packet if for Ostap
        flag = False

        for line in packets:
            if line.split()[-1] == END_STR:
                flag = True
                contacts['Lesya'].append(line)
            if len(line) % 2 == 0:
                flag = True
                contacts['Ivan'].append(line)
            if len(line) % 2 == 1 and line[0].isupper():
                flag = True
                contacts['Dmytro'].append(line)
            if not flag:
                contacts['Ostap'].append(line)
            flag = False


# Write parsed packets to file
def write(file_name, packet):
    with open(file_name, FILE_WRITE_MODE) as file_obj:
        file_obj.writelines([(p + NEW_LINE_SYMBOL) for p in packet])


def main():
    main_return_code = EXIT_FAILURE

    # if user didn't pass
    # file name to program, we stop execute
    if check_input_params():
        file_name = argv[1]
    else:
        print("Missing param: [file_name], program close!")
        return EXIT_FAILURE

    if check_exist(file_name):
        # read packets from file
        packets = get_packets(file_name)
        # parse packets
        parse_file(packets)

        # write parsed packets to dest. files
        write_files_name = contacts.keys()
        for out_file_name in write_files_name:
            write((out_file_name + FILE_EXTEND), contacts[out_file_name])
        main_return_code = EXIT_SUCCESS
    else:
        main_return_code = EXIT_FAILURE

    return main_return_code

if __name__ == '__main__':
    main()
