"""Self-contained Run445 negative witness; no external dependencies."""
from urllib.parse import urlsplit

def host_port(authority, op):
    h, _, p = getattr(authority, op)(':')
    return h or '127.0.0.1', int(p) if p else 5000

def cookie_host(authority, op):
    return getattr(authority, op)(':')[0]

def truth(authority):
    u = urlsplit('//' + authority)
    return u.hostname, 5000 if u.port is None else u.port

def main():
    authorities = ['node.example', 'node.example:8080', '[2001:db8::1]', '[2001:db8::1]:8080']
    for authority in authorities:
        correct_host, correct_port = truth(authority)
        for op in ('partition', 'rpartition'):
            try:
                actual = host_port(authority, op)
            except ValueError:
                actual = 'ValueError'
            print(authority, op, 'app=', actual, 'cookie=', cookie_host(authority, op),
                  'expected=', (correct_host, correct_port))
    assert host_port('node.example', 'partition') == ('node.example', 5000)
    try:
        host_port('node.example', 'rpartition')
    except ValueError:
        pass
    else:
        raise AssertionError('rpartition no-port regression not reproduced')
    assert host_port('[2001:db8::1]:8080', 'rpartition')[0] != truth('[2001:db8::1]:8080')[0]
    # (A1*B1)-(A1*B0)-(A0*B1)+(A0*B0) = (A1-A0)*(B1-B0).
    for a0 in (0, 1):
        for a1 in (0, 1):
            for b0 in (0, 1):
                for b1 in (0, 1):
                    assert a1*b1-a1*b0-a0*b1+a0*b0 == (a1-a0)*(b1-b0)
    print('PASS: no-port regression, bracketed IPv6 mismatch, 16 algebraic identities')

if __name__ == '__main__':
    main()
