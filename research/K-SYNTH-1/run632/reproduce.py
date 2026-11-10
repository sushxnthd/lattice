import itertools, json
counts = dict(admissible=0, naive=0, genuine=0, naive_false_positive=0)
witness = None
for bits in itertools.product((0,1), repeat=12):
    base,a,b,full = (bits[i:i+3] for i in range(0,12,3))
    if not (base[2] and a[2] and b[2] and full[2] and
            not all(base[:2]) and not all(a[:2]) and not all(b[:2]) and all(full[:2])):
        continue
    counts["admissible"] += 1
    naive = any(full[i] and not a[i] and not b[i] for i in range(2))
    genuine = any(not base[i] and full[i] and not a[i] and not b[i] for i in range(2))
    counts["naive"] += bool(naive)
    counts["genuine"] += bool(genuine)
    counts["naive_false_positive"] += bool(naive and not genuine)
    if naive and not genuine and witness is None:
        witness = dict(base=base,a=a,b=b,full=full)
assert counts == dict(admissible=27, naive=21, genuine=15, naive_false_positive=6)
print(json.dumps(dict(counts=counts,witness=witness), indent=2))
