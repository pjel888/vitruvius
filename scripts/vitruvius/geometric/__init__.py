"""Sprint GEOM — Geometric Constraint Engine (phase-15).

Narrow slice shipped today:
  * :mod:`vitruvius.geometric.inequality_compiler` — Parameter →
    Z3 expression compiler + ``check_compliance`` SAT/UNSAT verdict
    for a set of parameter proposals.
  * :mod:`vitruvius.geometric.envelope_2d` — shapely-based 2D
    buildable envelope generator (lot polygon minus setbacks).

GEOM.3 full 3D envelope generator and GEOM.4 multimodal IoU audit
are deferred until ``trimesh`` and ``cvxpy`` land on the ops host.
"""
