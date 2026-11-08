# K-SYNTH-1 Run574: hardlink confinement counterexample

Executed six assertions on local Linux CPython using temporary directories. A hardlink under an authorized root refers to an inode also accessible through an outside-root path. Path.resolve() remains inside the root because a hardlink is not a symlink. O_NOFOLLOW permits opening it. In-place writing through the authorized alias changes the outside-root file. By contrast, writing a new staged inode and os.replace on the alias leaves the outside-root hardlink unchanged in this static setup. This does not establish secure atomic transactions: concurrency, directory descriptor races, mount aliases, crash consistency, and permission boundaries are not resolved.

All 6/6 assertions passed. No production repair qualification, model inference, or semantic-IR superiority. Two qualified independent real repairs remain. All 89 reserved issues sealed. Next: implement descriptor-relative isolated staging and multi-file commit/recovery contract; prioritize prospective real multi-source qualification rather than repeated synthetic examples.

Local archive SHA256: 16e5266d1d72d5c71c28634393ba2a81e8129c1d55fb7ad6b2c7fbc88011bd8a.
