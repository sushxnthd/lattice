# Run522: descriptor-relative source snapshot counterexample

Executed ten directed Linux/POSIX tests of a bounded descriptor-relative source reader. All passed. O_NOFOLLOW and directory descriptors rejected parent/leaf symlinks and prevented a directory-name swap after opening from redirecting the read. Raw test results and executable prototype are preserved in local SHA-verified archive run522.zip (SHA-256 2cfd8061dfff874a736cb3b928bde4f228cf65c8b44665fb6227f90377c73802).

LIMITATION: This is not a production-grade freeze oracle. Initial root path, concurrent file writes, hardlinks, mount replacement, provenance, and snapshot consistency are not solved. No real repair qualified, no model inference. Two qualified tasks; 89 reserved issues sealed.
