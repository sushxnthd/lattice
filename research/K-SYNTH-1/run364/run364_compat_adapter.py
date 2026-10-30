# Run364 POST-OUTCOME compatibility adapter (not a frozen historical source arm).
# Reuses baseline connection-pool method rather than copying the reference helper.
# Scope: public HTTP/HTTPS URL same-host decisions; behavior outside this scope UNKNOWN.
def _is_same_host(url, scheme, host, port):
    pool_type = HTTPSConnectionPool if scheme == 'https' else HTTPConnectionPool
    pool = pool_type(host, port)
    try:
        return pool.is_same_host(url)
    finally:
        pool.close()
