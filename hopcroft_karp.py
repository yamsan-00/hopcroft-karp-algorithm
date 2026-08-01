"""Hopcroft-Karp algorithm for maximum-cardinality matching in bipartite graphs.

Clean, importable re-implementation of the algorithm in visualize.py, without
any side-effects or plot code, so it can be unit-tested and reused.

Input format (graph dict):
    {
        "U": ["u1", ...],      # left vertex set
        "V": ["v1", ...],      # right vertex set
        "edges": {"u1": ["v1", "v2"], ...}   # adjacency, U -> V
    }

Returns:
    matching_size : int
    pair_U        : dict {u -> v or None}
    pair_V        : dict {v -> u or None}
"""

from collections import deque

INF = float("inf")


def _bfs(graph, pair_U, pair_V, dist):
    queue = deque()
    for u in graph["U"]:
        if pair_U[u] is None:
            dist[u] = 0
            queue.append(u)
        else:
            dist[u] = INF
    dist[None] = INF
    while queue:
        u = queue.popleft()
        if dist[u] < dist[None]:
            for v in graph["edges"][u]:
                if dist[pair_V[v]] == INF:
                    dist[pair_V[v]] = dist[u] + 1
                    queue.append(pair_V[v])
    return dist[None] != INF


def _dfs(graph, u, pair_U, pair_V, dist):
    if u is not None:
        for v in graph["edges"][u]:
            if dist[pair_V[v]] == dist[u] + 1:
                if _dfs(graph, pair_V[v], pair_U, pair_V, dist):
                    pair_V[v] = u
                    pair_U[u] = v
                    return True
        dist[u] = INF
        return False
    return True


def hopcroft_karp(graph):
    pair_U = {u: None for u in graph["U"]}
    pair_V = {v: None for v in graph["V"]}
    dist = {}
    matching = 0
    while _bfs(graph, pair_U, pair_V, dist):
        for u in graph["U"]:
            if pair_U[u] is None:
                if _dfs(graph, u, pair_U, pair_V, dist):
                    matching += 1
    return matching, pair_U, pair_V
