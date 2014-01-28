#!/usr/bin/python
import os
import sys

if os.name != 'posix':
    sys.exit('platform not supported')

import socket
import time

import push, collectors


def main():
    interval = 1
    while True:
        start_time = time.time()
        data = []
        for name, fn in collectors.iteritems():
            raw_data = fn()
            data.append(format_for_submission(name, raw_data))
        pub_data(data)
        while (start_time + interval - time.time()) > 0:
            rest_duration = start_time + interval - time.time()
            time.sleep(rest_duration)


if __name__ == '__main__':
    main()
