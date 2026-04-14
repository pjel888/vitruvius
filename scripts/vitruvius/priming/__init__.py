"""Per-Layer Embeddings priming subpackage (Sprint R — Stream Y1+).

Every module in this package is loaded on demand, behind a
``features.y_*`` flag. Importing ``vitruvius.priming`` alone MUST NOT
import any submodule — it is a shell. Call sites that need a priming
helper do an explicit ``from vitruvius.priming.context_vector import ...``
inside a ``features.is_enabled("y_contextual_priming")`` branch.
"""
