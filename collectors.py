import psutil

collectors = {"cpu_percent": psutil.cpu_times_percent,
              "network_usage": psutil.net_io_counters}  # this is a counter; should replace with diff

