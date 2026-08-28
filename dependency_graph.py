"""
Arceus Phase 2: Dependency Graph Builder
Takes FK relationships from schema introspection and produces a
topologically sorted generation order (parents before children).
Detects and flags circular / self-referencing FKs instead of guessing.
"""
import json
from collections import defaultdict, deque
from schema_introspector import introspect


def build_dependency_graph(schema: dict) -> dict:
    """
    Build an adjacency list from FK relationships.
    Returns {
        "graph": {table: [tables it depends on]},
        "self_refs": [list of self-referencing FKs],
        "circular": [list of cycles detected],
        "unique_constraints": {table: [{constraint, columns}]},
    }
    """
    fks = schema["foreign_keys"]
    all_tables = set(schema["tables"].keys())

    # adjacency: table -> set of tables it DEPENDS ON (must be generated first)
    depends_on: dict[str, set[str]] = {t: set() for t in all_tables}
    self_refs: list[dict] = []

    for fk in fks:
        child = fk["child_table"]
        parent = fk["parent_table"]

        if child == parent:
            # Self-referencing FK — flag it, don't add to graph
            self_refs.append({
                "table": child,
                "column": fk["child_column"],
                "references": fk["parent_column"],
                "constraint": fk["constraint_name"],
            })
            continue

        depends_on[child].add(parent)

    return {
        "graph": {t: sorted(list(deps)) for t, deps in depends_on.items()},
        "self_refs": self_refs,
        "unique_constraints": schema.get("unique_constraints", {}),
    }


def topological_sort(graph: dict[str, list[str]]) -> tuple[list[str], list[list[str]]]:
    """
    Kahn's algorithm for topological sort.
    Returns (sorted_order, cycles_found).
    If cycles_found is non-empty, the sort is partial and the remaining
    tables are reported as part of a cycle.
    """
    # Build in-degree map
    in_degree: dict[str, int] = {t: 0 for t in graph}
    reverse: dict[str, list[str]] = defaultdict(list)

    for table, deps in graph.items():
        for dep in deps:
            in_degree[table] += 1  # table depends on dep
            reverse[dep].append(table)

    # Start with tables that have no dependencies
    queue: deque[str] = deque()
    for t in sorted(in_degree.keys()):  # sorted for deterministic output
        if in_degree[t] == 0:
            queue.append(t)

    sorted_order: list[str] = []
    while queue:
        node = queue.popleft()
        sorted_order.append(node)
        for dependent in sorted(reverse[node]):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)

    # Detect cycles: any table with in_degree > 0 is in a cycle
    cycles: list[list[str]] = []
    remaining = [t for t in graph if t not in sorted_order]
    if remaining:
        cycles.append(remaining)

    return sorted_order, cycles


def get_generation_order(schema: dict) -> dict:
    """
    Main entry point: returns the full dependency analysis.
    """
    dep_info = build_dependency_graph(schema)
    generation_order, cycles = topological_sort(dep_info["graph"])

    return {
        "generation_order": generation_order,
        "dependency_graph": dep_info["graph"],
        "self_referencing_fks": dep_info["self_refs"],
        "circular_dependencies": cycles,
        "unique_constraints": dep_info["unique_constraints"],
        "flags": _build_flags(dep_info["self_refs"], cycles),
    }


def _build_flags(self_refs: list, cycles: list) -> list[str]:
    """Build human-readable warning flags."""
    flags = []
    for sr in self_refs:
        flags.append(
            f"⚠️  SELF-REFERENCING FK: {sr['table']}.{sr['column']} "
            f"references {sr['table']}.{sr['references']} "
            f"(constraint: {sr['constraint']}). "
            f"This column will need special handling — not auto-resolved."
        )
    for cycle in cycles:
        flags.append(
            f"🔴 CIRCULAR DEPENDENCY: tables {cycle} form a cycle. "
            f"Cannot determine safe generation order — manual intervention required."
        )
    return flags


if __name__ == "__main__":
    schema = introspect()
    result = get_generation_order(schema)
    print(json.dumps(result, indent=2, default=str))
