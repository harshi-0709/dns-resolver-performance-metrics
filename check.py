import dns.message, dns.query
q = dns.message.make_query("o-o.myaddr.l.google.com", "TXT")
print(dns.query.https(q, "https://cloudflare-dns.com/dns-query", timeout=5).answer)
print(dns.query.https(q, "https://dns.quad9.net/dns-query", timeout=5).answer)