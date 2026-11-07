# Run566: abrupt-completion override counterexamples

Eight executable CPython examples test try/finally control-flow behavior. All eight assertions pass. A finally block can replace a pending return or exception with return, break, continue or another exception. Mutation of an already selected mutable return object remains observable, whereas rebinding a scalar local does not alter the selected return value. Nested finally blocks can override multiple pending completions.

IR consequence: soundness-scoped dataflow analysis must represent pending completion kind and value separately from the current environment and emit UNKNOWN for unsupported exception/control-flow constructs. The ordinary AST-action baseline must receive information-equivalent source facts and share the compiler/oracle.

Local executable SHA256 957c7fb036d7dbee95fd3882c5061e4ad842a7074b80877d99067af4783fbf22; raw JSON SHA256 003edde2aab7ddbff679b28cac6b19db9c9b912a84fda8fca918041df40841a5; archive SHA256 f123e5a10405e4da21e7b43e0bdbf79a9a79fd2bf8fe98f71c396ad5412a7442. Full local archive includes source, raw cases, report and manifest. GitHub raw mirroring remains incomplete.

Synthetic counterexamples only: no new production qualification, model inference, or superiority claim. Two qualified real tasks remain; 89 reserved tasks sealed.