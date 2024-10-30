import threading
import time

import psutil


class Monitoring:
    def __init__(self, interval=5):
        self.interval = interval
        self._monitoring = False

    def start_monitoring(self):
        self._monitoring = True
        thread = threading.Thread(target=self._monitor_resources)
        thread.start()

    def stop_monitoring(self):
        self._monitoring = False

    def _monitor_resources(self):
        while self._monitoring:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory_usage = psutil.virtual_memory().percent
            print(f"CPU Usage: {cpu_usage}%, Memory Usage: {memory_usage}%")
            time.sleep(self.interval)
