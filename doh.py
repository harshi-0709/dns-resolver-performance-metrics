import time
import httpx2 as httpx
import dns.message
import dns.query
import csv
from datetime import datetime
import random
import os

file_exists = os.path.exists("results_v2.csv")
with open("websites.txt") as f:
    websites = [line.strip() for line in f if line.strip()]

resolvers = [
    ("google",     "udp", "8.8.8.8"),
    ("cloudflare", "udp", "1.1.1.1"),
    ("quad9",      "udp", "9.9.9.9"),
    ("google",     "doh", "https://dns.google/dns-query"),
    ("cloudflare", "doh", "https://cloudflare-dns.com/dns-query"),
    ("quad9",      "doh", "https://dns.quad9.net/dns-query"),
]

client = httpx.Client(http2=True)
for name, transport, target in resolvers:
    if transport == "doh":
        question = dns.message.make_query("example.com", 'A')
        try:
            dns.query.https(question, target, timeout=5, session=client)
        except Exception:
            pass

with open("results_v2.csv", "a", newline="") as f:
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow(["timestamp", "resolver", "transport", "website", "latency_ms", "success", "rcode", "num_answers"])
    for website in websites:
        random.shuffle(resolvers)
        for name, transport, target in resolvers:
            question = dns.message.make_query(website, 'A')
            start = time.perf_counter()
            try:
                if transport == "udp":
                    answer = dns.query.udp(question, target, timeout=3)
                else:
                    answer = dns.query.https(question, target, timeout=5, session=client)
                success = True
                rcode = answer.rcode()
                num_answers = len(answer.answer)
            except Exception:
                success = False
                rcode = None
                num_answers = None
            end = time.perf_counter()
            if success:
                latency = (end - start) * 1000
            else:
                latency = None
            writer.writerow([datetime.now().isoformat(), name, transport, website, latency, success, rcode, num_answers])