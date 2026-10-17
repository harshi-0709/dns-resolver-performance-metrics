import time 
import dns.message
import dns.query
import csv
from datetime import datetime
import random 
import os
file_exists = os.path.exists("results.csv")
with open("websites.txt") as f:
    websites = [line.strip() for line in f if line.strip()]
resolvers=["8.8.8.8","1.1.1.1","9.9.9.9"]
with open("results.csv", "a", newline="") as f:
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow(["timestamp", "resolver", "website", "latency_ms","success","rcode","num_answers"])
    for website in websites:
        random.shuffle(resolvers)
        for resolver in resolvers:
                question =dns.message.make_query(website,'A')
                start=time.perf_counter()
                try:
                    answer = dns.query.udp(question, resolver, timeout=3)
                    success = True
                    rcode=answer.rcode()
                    num_answers = len(answer.answer)
                except Exception:
                    success = False
                    rcode=None
                    num_answers = None    
                end=time.perf_counter()
                if success:
                    latency=(end-start)*1000
                else:
                    latency=None   
                writer.writerow([datetime.now().isoformat(),resolver,website,latency,success,rcode,num_answers])

           
   


