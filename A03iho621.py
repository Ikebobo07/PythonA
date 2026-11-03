r"""
Burglar Alarm Bayes' Net (Figure 1).

    Burglary   Earthquake
          \     /
          Alarm
          /   \
  JohnCalls   MaryCalls

Computes P(+query | +evidence) by enumeration: add up the full joint
probability over every combination of the five variables.
"""
from itertools import product

# ---------------------------------------------------------------
# The Bayes' Net: each node lists its parents and its CPT.
# The CPT gives P(node = True | parent values).
# P(node = False | ...) is simply 1 minus that.
# ---------------------------------------------------------------
BAYES_NET = {
    "B": {"parents": [], "cpt": {(): 0.001}},
    "E": {"parents": [], "cpt": {(): 0.002}},
    "A": {
        "parents": ["B", "E"],
        "cpt": {
            (True, True): 0.95,
            (True, False): 0.94,
            (False, True): 0.29,
            (False, False): 0.001,
        },
    },
    "J": {"parents": ["A"], "cpt": {(True,): 0.90, (False,): 0.05}},
    "M": {"parents": ["A"], "cpt": {(True,): 0.70, (False,): 0.01}},
}

NODES = ["B", "E", "A", "J", "M"]


def node_probability(node, value, assignment):
    """P(node = value | its parents' values in this assignment)."""
    info = BAYES_NET[node]
    parent_values = tuple(assignment[p] for p in info["parents"])
    p_true = info["cpt"][parent_values]
    return p_true if value else 1 - p_true


def joint_probability(assignment):
    """P(b, e, a, j, m) = P(b) P(e) P(a|b,e) P(j|a) P(m|a)."""
    prob = 1.0
    for node in NODES:
        prob *= node_probability(node, assignment[node], assignment)
    return prob


def probability_of(fixed):
    """Sum the joint over every assignment that agrees with 'fixed'."""
    total = 0.0
    for values in product([True, False], repeat=len(NODES)):
        assignment = dict(zip(NODES, values))
        if all(assignment[n] == v for n, v in fixed.items()):
            total += joint_probability(assignment)
    return total


def conditional_probability(query, evidence):
    """P(+query | +evidence) = P(+query, +evidence) / P(+evidence)."""
    numerator = probability_of({query: True, evidence: True})
    denominator = probability_of({evidence: True})
    return numerator / denominator


def ask_node(prompt):
    """Keep asking until the user types one of B, E, A, J, M."""
    while True:
        print(prompt)
        answer = input().strip().upper()
        if answer in NODES:
            return answer
        print("Invalid node. Please enter one of B, E, A, J, M.")


def main():
    print("Welcome to the Burglar Alarm Bayes Net!")
    evidence = ask_node("Enter an evidence node (B, E, A, J, M):")
    query = ask_node("Enter a query node (B, E, A, J, M):")
    result = conditional_probability(query, evidence)
    print(f"The conditional probability P(+{query.lower()}|+{evidence.lower()}) is {result:.6f}")


if __name__ == "__main__":
    main()