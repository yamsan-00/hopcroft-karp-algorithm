"""Unit tests for hopcroft_karp.hopcroft_karp."""
from hopcroft_karp import hopcroft_karp


def _g(U, V, edges):
    return {"U": list(U), "V": list(V),
            "edges": {u: list(vs) for u, vs in edges.items()}}


def test_empty_graph():
    size, pU, pV = hopcroft_karp(_g([], [], {}))
    assert size == 0 and pU == {} and pV == {}


def test_single_edge():
    g = _g(["u1"], ["v1"], {"u1": ["v1"]})
    size, pU, pV = hopcroft_karp(g)
    assert size == 1 and pU["u1"] == "v1" and pV["v1"] == "u1"


def test_textbook_instance_size_4():
    g = _g(["a", "b", "c", "d", "e"], ["A", "B", "C", "D"], {
        "a": ["A", "C"], "b": ["B", "C", "D"], "c": ["A", "B", "C"],
        "d": ["C", "D"], "e": ["A", "C", "D"]})
    size, pU, pV = hopcroft_karp(g)
    assert size == 4
    matched = [pU[u] for u in g["U"] if pU[u] is not None]
    assert len(matched) == len(set(matched))


def test_complete_balanced_graph():
    n = 5
    g = _g([f"u{i}" for i in range(n)], [f"v{i}" for i in range(n)],
           {f"u{i}": [f"v{j}" for j in range(n)] for i in range(n)})
    assert hopcroft_karp(g)[0] == n


def test_disconnected_components():
    g = _g(["u1", "u2"], ["v1", "v2"], {"u1": ["v1"], "u2": ["v1"]})
    assert hopcroft_karp(g)[0] == 1


def test_pair_consistency():
    g = _g(["u1", "u2"], ["v1", "v2"], {"u1": ["v1", "v2"], "u2": ["v1"]})
    size, pU, pV = hopcroft_karp(g)
    for u, v in pU.items():
        if v is not None:
            assert pV[v] == u
    for v, u in pV.items():
        if u is not None:
            assert pU[u] == v
