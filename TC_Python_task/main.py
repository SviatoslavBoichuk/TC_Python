#!/usr/bin/env python

import os.path

EXIT_SUCCESS = 0
EXIT_FAILURE = -1

contacts = {'Ivan': [], 'Dmythro': [], 'Ostap': [], 'Lesya': []}
packets = []


def check_exist(
        file_path):
    return os.path.isfile(file_path)


def get_packets(file_name):
    with open(file_name, "r") as file_obj:
        packets = file_obj.readlines()


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


def write(file_name, packet):
    with open(file_name, "w+") as file_obj:
        for line in packet:
            file_obj.write(line)


def main():
    main_return_code = EXIT_FAILURE

    file_name = "message.txt"

    if check_exist(file_name):
        get_packets(file_name)
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
