"""Strict wheel ZIP/RECORD validator. Never imports or executes wheel contents."""
import base64
import csv
import hashlib
import io
import pathlib
import re
import zipfile

class Unknown(ValueError):
    pass

def inspect(wheel: pathlib.Path, expected: str, max_bytes: int = 100_000_000):
    if not re.fullmatch('[0-9a-f]{64}', expected):
        raise Unknown('UNKNOWN: malformed external digest')
    if not wheel.is_file() or wheel.suffix != '.whl' or wheel.stat().st_size > max_bytes:
        raise Unknown('UNKNOWN: missing, invalid or oversized wheel')
    data = wheel.read_bytes()
    if hashlib.sha256(data).hexdigest() != expected:
        raise Unknown('UNKNOWN: wheel digest mismatch')
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            names = z.namelist()
            if len(names) != len(set(names)) or len(names) > 10000:
                raise Unknown('UNKNOWN: duplicate/too many ZIP entries')
            if any(n.startswith('/') or '\\' in n or any(p in ('', '.', '..') for p in n.split('/')) for n in names):
                raise Unknown('UNKNOWN: unsafe ZIP path')
            if any(i.file_size > max_bytes or i.compress_size > max_bytes for i in z.infolist()):
                raise Unknown('UNKNOWN: oversized ZIP entry')
            records = [n for n in names if n.endswith('.dist-info/RECORD')]
            if len(records) != 1:
                raise Unknown('UNKNOWN: RECORD count')
            rec = records[0]
            rows = list(csv.reader(io.StringIO(z.read(rec).decode('utf-8'))))
            if len(rows) != len(names) or len({r[0] for r in rows if len(r)==3}) != len(names):
                raise Unknown('UNKNOWN: RECORD coverage')
            for row in rows:
                if len(row) != 3 or row[0] not in names:
                    raise Unknown('UNKNOWN: malformed RECORD')
                name, digest, size = row
                if name == rec:
                    if digest or size:
                        raise Unknown('UNKNOWN: RECORD self-hash')
                    continue
                if not digest.startswith('sha256=') or not size.isdecimal():
                    raise Unknown('UNKNOWN: missing hash/size')
                payload = z.read(name)
                actual = base64.urlsafe_b64encode(hashlib.sha256(payload).digest()).rstrip(b'=').decode('ascii')
                if digest != 'sha256=' + actual or int(size) != len(payload):
                    raise Unknown('UNKNOWN: RECORD mismatch')
            return {'sha256': expected, 'entries': len(names), 'record': rec}
    except (zipfile.BadZipFile, UnicodeError, csv.Error, KeyError, RuntimeError) as exc:
        raise Unknown('UNKNOWN: malformed ZIP/RECORD') from exc
