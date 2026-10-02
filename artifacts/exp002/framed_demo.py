def policy(auth, owner, blocked):
    _lattice_v0 = auth and (not blocked)
    _lattice_v1 = _lattice_v0 and owner
    _lattice_v2 = _lattice_v1
    _lattice_v3 = not blocked
    return (_lattice_v3, _lattice_v1, _lattice_v2)
