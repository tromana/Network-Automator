#!/usr/bin/env python

import telnetlib
import threading
import os.path
import subprocess
import time
import sys


def connection_details():
    '''
    Construct Telnet Connection parameters for devices
    :return:
    '''
    global ip_list
    global port_list
    global ips
    global ports

    #All the VM's running locally needs port number along with IP's
    ips = []
    ports = []

    ip_file = raw_input("Enter IP List : ")

    ip_file = open(ip_file, 'r')
    ip_file.seek(0)
            
    #Read all IP's from the file
    ip_list = ip_file.readlines()

    for item in ip_list:
        ips.append(item.strip().split(':')[0])
    #forming ports list
    for item in ip_list:
        ports.append(item.strip().split(':')[1])

    #print ips
    #print ports

    ip_file.close()


def cmd_is_valid():

    '''
    Function to check if the command path is valid
    :return:
    '''
    global cmd_file

    while True:
        cmd_file = raw_input("Input Command File: ")

        #check if the file exists
        if os.path.isfile(cmd_file) == True:
            print("\nPushing Commands to device(s)...\n")
            break

        else:
            print("\nFile %s does not exist! Please enter a valid File Name again!\n" % cmd_file)
            continue

def open_telnet_conn(ip,port):
    '''
    Telnet Connect handler for devices

    :param ip: <ip address from IP list>
    :param port: <port from Port list>
    :return:
    '''
    try:
        #telnet parameters
        username = 'teopy'
        password = 'python'

        connection_timeout = 5
        reading_timeout = 5
        
        #Connecting to device.
        connect_handle = telnetlib.Telnet(ip, port, connection_timeout)

        router_output = connect_handle.read_until("Username:", reading_timeout)
        connect_handle.write(username + "\n")

        router_output = connect_handle.read_until("Password:", reading_timeout)
        connect_handle.write(password + "\n")
        time.sleep(1)	
        
        #set term length
        connect_handle.write("terminal length 0\n")
        time.sleep(1)
        
        #Global Config section
        connect_handle.write("\n")
        connect_handle.write("configure terminal\n")
        time.sleep(1)

        #invoke command validator to check validate the commands
        cmd_is_valid()

        cmd_lst = open(cmd_file, 'r')
            
        #Starting from the beginning of the file
        cmd_lst.seek(0)
        
        #Writing each line in the file to the device
        for each_line in cmd_lst.readlines():
            connect_handle.write(each_line + '\n')
            time.sleep(2)

        cmd_lst.close()
        
        #Test for reading command output
        router_output = connect_handle.read_very_eager()
        print router_output
        
        #Closing the connection
        connect_handle.close()
        
    except IOError:
        print "Input error! Please check username, password and file name."



def create_threads():
    
    for ip,port in zip(ips,ports):
        print("Connecting ip:%s and Port:%s" % (ip,port))
        open_telnet_conn(ip,port)   #args is a tuple with a single element
        #th.start()
        #threads.append(th)
        

#Creating threads
#def create_threads():
#   threads = []
#    for ip,port in zip(ips,ports):
#        print("Connecting ip:%s and Port:%s" % (ip,port))
#        th = threading.Thread(target = open_telnet_conn, args = (ip,port))   #args is a tuple with a single element
#        th.start()
#        threads.append(th)
#        
#   for th in threads:
#        th.join()

#Calling threads creation function
create_threads()

#End of program
