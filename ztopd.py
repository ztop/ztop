#!/usr/bin/python
import os
import sys

if os.name != 'posix':
    sys.exit('platform not supported')

import time

import push, collectors


def main():
    interval = 1
    while True:
        start_time = time.time()
        data = []

        # run collectors, push
        for name, fn in collectors.collectors.iteritems():
            columns, values = fn()
            data.append(push.format_for_submission(name, columns, values))
        push.pub_data(data)

        # rest until the next loop
        while (start_time + interval - time.time()) > 0:
            rest_duration = start_time + interval - time.time()
            time.sleep(rest_duration)


if __name__ == '__main__':
    main()
