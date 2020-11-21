#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import argparse
import threading
from socket import *
from configparser import ConfigParser
from colorama import init,Fore
init(autoreset=True)

class PortScanner():
    def __init__(self,ip):
        print(Fore.RED + """
  ____               _    ____                                        
 |  _ \  ___   _ __ | |_ / ___|   ___  __ _  _ __   _ __    ___  _ __ 
 | |_) |/ _ \ | '__|| __|\___ \  / __|/ _` || '_ \ | '_ \  / _ \| '__|
 |  __/| (_) || |   | |_  ___) || (__| (_| || | | || | | ||  __/| |   
 |_|    \___/ |_|    \__||____/  \___|\__,_||_| |_||_| |_| \___||_|   v0.1.1
                                                                      
                                                        Author:Wiley
        """)
        print(Fore.BLUE + "[*] PortScanner Initialize...")
        self.ip = ip
        self.ports = self.ReadConfig()
        self.threads = []
    def __del__(self):
        print(Fore.BLUE + "[*] End for scanner...")

    def ReadConfig(self):
        print(Fore.BLUE + "[*] Load Config...")
        cfg = ConfigParser()
        try:
            cfg.read('config.ini')
            CfgPorts = cfg.get('config','ports')
            ports = CfgPorts.strip(',').split(',')
            return ports
        except:
            pass

    def Scanner(self,port):
        try:
            s = socket(AF_INET, SOCK_STREAM)
            s.settimeout(2)
            s.connect((self.ip, port))
            print(Fore.GREEN + "[+] " + str(port) + " is Open!",end='\n')
        except:
            pass
        s.close()

    def run(self):
        for i in self.ports:
            t = threading.Thread(target=self.Scanner, args=(int(i),),daemon=True)
            self.threads.append(t)
            t.start()
        for j in self.threads:
            j.join()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="PortScanner.py -i 192.168.1.1")
    parser.add_argument('-i', '--ip',required=True,help="Scan the IP address of the port")
    args = parser.parse_args()

    obj = PortScanner(args.ip)
    obj.run()