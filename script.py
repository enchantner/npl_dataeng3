import queue
from threading import Thread
import os
import requests
class DownloadThread(Thread):
    import os 
    def __init__(self, queue, name):
        super().__init__()
        self.queue = queue
        self.name = name
   
    def run(self):
        while True:
            url = self.queue.get()
            fname = os.path.basename(url)
           
            res = requests.get(url, stream=True)
            res.raise_for_status()        
       
            with open(fname, "wb") as savefile:
                for chunk in res.iter_content(1024):
                    savefile.write(chunk)
                   
            self.queue.task_done()
            print(f"{self.name} finished downloading {url} !")
 
 
def main(urls):
    q = queue.Queue()
    threads = [DownloadThread(q, f"Thread {i + 1}") for i in range(5)]
    for t in threads:
        # not waiting for child threads
        t.setDaemon(True)
        t.start()
   
    for url in urls:
        q.put(url)
       
    q.join()  # all cheeki-breeki
 
main([
    "http://www.irs.gov/pub/irs-pdf/f1040.pdf",
    "http://www.irs.gov/pub/irs-pdf/f1040a.pdf",
    "http://www.irs.gov/pub/irs-pdf/f1040ez.pdf",
    "http://www.irs.gov/pub/irs-pdf/f1040es.pdf",
    "http://www.irs.gov/pub/irs-pdf/f1040sb.pdf"
])
