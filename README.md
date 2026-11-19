# DNS Resolver Performance Metrics

Measuring DNS resolver latency from an Indian hostel network: Google (8.8.8.8), Cloudflare (1.1.1.1) and Quad9 (9.9.9.9), over plain DNS (UDP) and DNS over HTTPS (DoH), for Indian and international websites.

Paper (preprint): **A Comparative Study on Different DNS Transports for Different Resolvers**
DOI: https://doi.org/10.5281/zenodo.XXXXXXX](https://doi.org/10.5281/zenodo.24358433

## What this does
- Queries 142 domains (74 international, 68 Indian) through each resolver and transport, in random order each round.
- Logs timestamp, resolver, transport, website, latency, success, rcode and number of answers.
- Analyses the data: median, p95, p99, CDF, paired Wilcoxon tests, Indian vs international, hour of day, slow queries.

## Files
| File | Description |
|---|---|
| `doh.py` | Collects the measurements |
| `results_v2_final.csv` | Final dataset (28,116 queries, 17-18 Oct 2026) |
| `analysis.ipynb` | Analysis and figures |
| `hourly.png , india_vs_intl.png , median_bar.png`| Figures used in the paper |

## Run it
```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install "dnspython[doh]" pandas numpy scipy matplotlib jupyter
python doh.py
jupyter notebook analysis.ipynb
```

## Method notes
- DoH is measured on a reused HTTP/2 connection after a warm-up query, so TLS handshake time is excluded.
- Failed queries are kept in the data.
