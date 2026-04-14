from __future__ import annotations

from dataclasses import dataclass

import community as community_louvain
import networkx as nx

from .contract import GraphSnapshot


@dataclass(frozen=True)
class Community:
    community_id: int
    node_ids: tuple[str, ...]
    summary: str


@dataclass(frozen=True)
class CommunityReport:
    communities: tuple[Community, ...]
    modularity: float


def _to_undirected(snapshot: GraphSnapshot) -> nx.Graph:
    g = nx.Graph()
    for node in snapshot.nodes:
        g.add_node(node.id)
    for edge in snapshot.edges:
        g.add_edge(edge.from_id, edge.to_id)
    return g


def _summarize(cid: int, node_ids: tuple[str, ...]) -> str:
    head = ", ".join(node_ids[:5])
    return f"Community {cid}: {head}"


def detect_communities(
    snapshot: GraphSnapshot,
    *,
    random_state: int = 0,
) -> CommunityReport:
    if not snapshot.nodes:
        return CommunityReport(communities=(), modularity=0.0)

    graph = _to_undirected(snapshot)
    partition = community_louvain.best_partition(graph, random_state=random_state)

    # Group node ids by raw community label.
    by_label: dict[int, list[str]] = {}
    for node_id, label in partition.items():
        by_label.setdefault(label, []).append(node_id)

    # Deterministic relabel: sort communities by their smallest member id.
    ordered = sorted(
        by_label.items(),
        key=lambda kv: sorted(kv[1])[0] if kv[1] else "",
    )

    communities: list[Community] = []
    for new_id, (_, members) in enumerate(ordered):
        sorted_members = tuple(sorted(members))
        communities.append(
            Community(
                community_id=new_id,
                node_ids=sorted_members,
                summary=_summarize(new_id, sorted_members),
            )
        )

    modularity = float(community_louvain.modularity(partition, graph))
    return CommunityReport(communities=tuple(communities), modularity=modularity)
