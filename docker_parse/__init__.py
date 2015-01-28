#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import json
import subprocess, sys

def main():
    if len(sys.argv) < 2:
        print("Please specific container name!")
        sys.exit()
    
    try:
        cmd = ["docker", "inspect"]
        cmd.extend(sys.argv[1:])
        output = subprocess.check_output(cmd, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        sys.exit()
    
    infos = json.loads(output)
    for info in infos:
        name = info['Name'][1:]
        conf = info['Config']
        hconf = info['HostConfig']
        volumes = ''; ports = ''

        if len(hconf["Binds"]) > 0:
            volumes = ' -v ' + ' -v '.join(hconf['Binds'])
        if len(hconf["PortBindings"]) > 0:
            for k, v in hconf['PortBindings'].items():
                for hv in v:
                    ports += ' -p '
                    if 'HostIp' in hv:
                        ports += hv['HostIp'] + ':'
                    if 'HostPort' in hv: 
                        ports += hv['HostPort'] + ':'
                    ports += k
                
        print('docker run --name {name} -d {volumes} {ports} {image}'.format(
            name = name, volumes = volumes, ports = ports, image = conf['Image']))

if __name__ == "__main__":
    main()