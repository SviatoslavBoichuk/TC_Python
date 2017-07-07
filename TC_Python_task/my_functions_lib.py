import json
import os
import re
from sys import argv
from c_module import ReadDataFromFile
from packet_storage_class import  PacketStorage

#Open file modes
FILE_READ_MODE = "r"
FILE_WRITE_MODE = "w+"

FILE_EXTEND = '.txt'
END_STR = 'end'
NEW_LINE_SYMBOL = '\n'
ADDRESSANTS_IP_FILE = 'addressants.json'
NUM_INPUT_PARAMS = 2


def check_input_params():
    """Check if count of input params is less then 2"""
    return len(argv) == NUM_INPUT_PARAMS


def check_exist(
        file_path):
    """Function check if file with packets exits
    If exist - return true, else return false"""
    return os.path.isfile(file_path)


def read_dest_ip_addresses(file_name):
    """Read addressants names and their IP addresses from json file"""
    with open(file_name) as ip_file:
        json_data = json.load(ip_file)
        return json_data


# Read packets from input file
def get_packets(file_name):
    """Read packets from @file_name file"""
    packets = []
    packets = [line for line in (ReadDataFromFile(file_name)).split("\n") if line !='']
    return packets


def parse_file(
        packets, contacts):
        """parse packet to addresantss
        if packet is no Ivan, or Dmytro or Lesya, then
        this packet if for Ostap"""
        flag = False
        for line in packets:
            if re.match('^.*?\s{}$'.format(END_STR), line):
                flag = True
                contacts[3].add_packet(line)
            if re.match('^([^\n]{2})+$', line):
                flag = True
                contacts[0].add_packet(line)
            if re.match('^[A-Z]+.*?$', line) and not re.match('^([^\n]{2})+$', line):
                flag = True
                contacts[2].add_packet(line)
            if not flag:
                contacts[1].add_packet(line)
            flag = False


def write(file_name, packet):
    """Write parsed packets to file"""
    with open(file_name, FILE_WRITE_MODE) as file_obj:
        file_obj.writelines([(p + NEW_LINE_SYMBOL) for p in packet])
