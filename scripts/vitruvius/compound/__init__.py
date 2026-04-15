"""Sprint Z — Compound AI Evolution (phase-12) modules.

Houses the narrow-slice subset of the Sprint Z streams that lands
in the autonomous unblock pass:
  * :mod:`adversarial` — Stream S2 Proposer/Inspector/Adjudicator swarm
  * :mod:`dspy_compiler` — Stream S5 DSPy prompt compilation

Streams S1 (neuro-symbolic Datalog), S3 (differential dataflow), and
S4 (Wasm spatial kernel) ship later — S1+S4 need a Rust crate, S3
needs a streaming dataflow runtime that's still on the deferred list.
"""
