#!/usr/bin/env python

"""Application reads packets from the input file and
generates output files with packets seperated by addresantss,
according to task"""

from my_functions_lib import *
from packet_storage_class import PacketStorage

# Main function return one of folowing code:
# 0 if application finished success, otherwise return -1
EXIT_SUCCESS = 0
EXIT_FAILURE = -1

ENCODE = 'utf-8'

def main():
    main_return_code = EXIT_FAILURE

    # if user didn't pass
    # file name to program, we stop execute
    if check_input_params():
        file_name = argv[1]
    else:
        print("Missing param: [file_name], program closed!")
        return EXIT_FAILURE

    if check_exist(file_name):

        # read json file
        json_data = None
        if check_exist(ADDRESSANTS_IP_FILE):
            json_data = read_dest_ip_addresses(ADDRESSANTS_IP_FILE)

        # create contact list
        contacts = []
        for user in json_data.items():
            name, ip = user
            contacts.append(PacketStorage(name.encode(ENCODE), ip.encode(ENCODE)))

        # read packets from file
        packets = get_packets(file_name)
        # parse packets and save them to addresants
        parse_file(packets, contacts)

        # write packets to destination file
        # and send packets to addressants
        for user in contacts:
            write((user.get_addressant_name() + FILE_EXTEND), user.get_addressant_packets())
            user.send_packets()

        main_return_code = EXIT_SUCCESS
    else:
        main_return_code = EXIT_FAILURE

    return main_return_code

if __name__ == '__main__':
    main()
