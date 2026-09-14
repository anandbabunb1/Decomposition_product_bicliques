# A 44-block decomposition of E(K₄) × E(K₁₇)

This repository contains an explicit decomposition of $E(K_4)\times E(K_{17})$ into **44 products of biclique edge sets**, together with an independent Python verifier. The construction accompanies Lemma 1 of *New bounds on the Graham–Pollak theorem for hypergraphs* by Anand Babu.

## Mathematical description

Use disjoint vertex sets

$$
V(K_4)=\{a,b,c,d\},\qquad V(K_{17})=\{1,2,\ldots,17\}.
$$

Each product block has the form

$$
\mathcal B_t=E(K_{A_t,B_t})\times E(K_{C_t,D_t}),
$$

where $A_t,B_t\subseteq V(K_4)$ and $C_t,D_t\subseteq V(K_{17})$ are nonempty, with the two parts of each biclique disjoint. Here $K_{A,B}$ denotes the complete bipartite graph with vertex parts $A$ and $B$.

An element of a block can equivalently be represented as an unordered four-vertex edge containing one vertex from each of its four parts. The target consists of all four-vertex edges containing exactly two vertices from each of the two vertex sets. There are

$$
\binom{4}{2}\binom{17}{2}=6\cdot136=816
$$

such edges. The verifier checks that each belongs to exactly one of the 44 blocks.

## Files

| File | Purpose |
| --- | --- |
| `lemma1_biclique_products.json` | Lists the vertex parts of all 44 product blocks and records their relation to the manuscript construction. |
| `check_lemma1_partition.py` | Independently expands the blocks and checks that they form the required partition. |

The verifier does not require the manuscript, LaTeX, or any external Python packages.

## Requirements

- Python 3.
- Both files listed above, downloaded into the same directory.

No package installation or virtual environment is needed.

## Running the verifier

Open a terminal in the directory containing the two files.

On macOS or Linux:

```bash
python3 check_lemma1_partition.py
```

On Windows, using the Python launcher:

```powershell
py -3 check_lemma1_partition.py
```

If your Python 3 installation uses the command `python`, use that instead.

To specify a different JSON file or its location:

```bash
python3 check_lemma1_partition.py path/to/blocks.json
```

The default JSON filename is resolved relative to the terminal's current directory, not the script's directory. To run from elsewhere, provide paths to both files.

For command-line help:

```bash
python3 check_lemma1_partition.py --help
```

## Expected output

For the supplied construction, the verifier prints:

```text
Expected distinct four-vertex edges: 816
Product blocks: 44 (required: 44)
Distinct four-vertex edges generated: 816
Total edge occurrences: 816
Missing edges: 0
Unexpected edges: 0
Edges covered more than once: 0
PASS: The 44 blocks form an exact partition.
```

The process exits with status `0` for a valid partition and `1` for a failed check, invalid JSON data, or a file-reading error. Invalid command-line arguments are handled separately by Python's argument parser.

## What is checked?

The verifier:

1. Constructs the target set of all 816 edges directly from the fixed vertex sets.
2. Checks that each biclique has two nonempty parts, with valid vertex types and labels, no repeated vertices within a part, and no overlap between its parts.
3. Expands every product block into unordered four-vertex edges and counts their multiplicities.
4. Checks that there are exactly 44 blocks, no missing or unexpected edges, and no edges covered more than once.

The result is computed from the `products` array. The verifier does **not** rely on the JSON's stored `verification`, `product_count`, or `vertex_labels` metadata, nor on the source-graph descriptions or block IDs.

This verifies the explicit finite partition; it does not prove that 44 is the minimum possible number of blocks or verify the manuscript's subsequent asymptotic arguments.

## JSON format

The top-level `products` array contains objects such as the following first block:

```json
{
  "id": 1,
  "source_graph": "G_1",
  "source_biclique_index": 1,
  "K4_biclique": {
    "left": ["a", "b"],
    "right": ["c", "d"]
  },
  "K17_biclique": {
    "left": [2],
    "right": [1, 4, 5, 6, 10]
  }
}
```

Vertices of $K_4$ are strings; vertices of $K_{17}$ are integers, not quoted strings. Each `left` and `right` array specifies a vertex part, not an edge list. The example above generates $2\cdot2\cdot1\cdot5=20$ four-vertex edges.

The JSON also records the relabeling from the manuscript: the original $K_{17}$ labels $a,\ldots,h$ become $10,\ldots,17$, while the $K_4$ labels $1,2,3,4$ become $a,b,c,d$.
