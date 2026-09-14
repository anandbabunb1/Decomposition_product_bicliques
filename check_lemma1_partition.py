"""Independently check the 44-block partition using only the JSON vertex parts."""

import argparse
import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path


def biclique_edges(block, key, universe, vertex_type):
    parts = block.get(key)
    if not isinstance(parts, dict):
        raise ValueError(f"{key} must specify left and right vertex parts")
    for side in ("left", "right"):
        vertices = parts.get(side)
        if not isinstance(vertices, list) or not vertices:
            raise ValueError(f"{key}.{side} must be a nonempty list")
        if any(type(vertex) is not vertex_type for vertex in vertices):
            raise ValueError(f"{key}.{side} has an incorrect vertex type")
        if len(vertices) != len(set(vertices)):
            raise ValueError(f"{key}.{side} contains repeated vertices")
        if not set(vertices) <= universe:
            raise ValueError(f"{key}.{side} contains vertices outside its graph")
    if set(parts["left"]) & set(parts["right"]):
        raise ValueError(f"{key} has overlapping vertex parts")
    return [frozenset(edge) for edge in product(parts["left"], parts["right"])]


def check_partition(data):
    vertices4 = set("abcd")
    vertices17 = set(range(1, 18))
    expected = {
        frozenset(pair4 + pair17)
        for pair4 in combinations(sorted(vertices4), 2)
        for pair17 in combinations(sorted(vertices17), 2)
    }
    print(f"Expected distinct four-vertex edges: {len(expected)}")
    if not isinstance(data, dict) or not isinstance(data.get("products"), list):
        raise ValueError("The JSON must contain a products list")
    blocks = data["products"]
    counts = Counter()
    for position, block in enumerate(blocks, 1):
        if not isinstance(block, dict):
            raise ValueError(f"Block {position} must be an object")
        try:
            edges4 = biclique_edges(block, "K4_biclique", vertices4, str)
            edges17 = biclique_edges(block, "K17_biclique", vertices17, int)
        except ValueError as error:
            raise ValueError(f"Block {position}: {error}") from error
        counts.update(edge4 | edge17 for edge4, edge17 in product(edges4, edges17))

    covered = set(counts)
    missing = expected - covered
    unexpected = covered - expected
    repeated = sum(multiplicity > 1 for multiplicity in counts.values())
    valid = len(blocks) == 44 and not missing and not unexpected and not repeated
    print(f"Product blocks: {len(blocks)} (required: 44)")
    print(f"Distinct four-vertex edges generated: {len(covered)}")
    print(f"Total edge occurrences: {sum(counts.values())}")
    print(f"Missing edges: {len(missing)}")
    print(f"Unexpected edges: {len(unexpected)}")
    print(f"Edges covered more than once: {repeated}")
    print("PASS: The 44 blocks form an exact partition." if valid else
          "FAIL: The blocks do not form the required 44-block partition.")
    return valid


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("json_file", nargs="?", default="lemma1_biclique_products.json")
    args = parser.parse_args()
    try:
        data = json.loads(Path(args.json_file).read_text(encoding="utf-8"))
        return 0 if check_partition(data) else 1
    except (OSError, ValueError) as error:
        print(f"FAIL: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
