# Run395 theorem: finite-oracle non-identifiability

For any finite S in an infinite input domain D, choose z outside S. Let f:D->{0,1} and define g(x)=f(x) for x!=z, g(z)=1-f(z). Then f and g agree on every x in S but differ at z. Therefore a finite test oracle alone cannot prove general semantic equivalence or universal absence of a module's behavioral effect.

Executable cross-module witness: A baseline adjust(x)=x; A reference adjust(x)=x+(a if x==99 else 0). B reference calls adjust and adds b. All frozen inputs 1,2,3 see no A contribution, but x=99 does. Sixty-four seeded CPython witnesses confirm the predicted difference.

Mechanical-coupling witness: A reference adds a TOKEN constant, B reference imports TOKEN to repair targets. B-reference/A-baseline aborts at import, but a compatibility-only TOKEN shim makes B sufficient on all frozen cases. Thus import-time ablation failure alone does not demonstrate independent behavioral necessity.

These results are bounded to the stated observation boundary. Import-time side effects, reflection and dynamic state can invalidate a shim's global neutrality; missing evidence must be UNKNOWN.