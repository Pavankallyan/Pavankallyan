import sys
import re
from collections import deque
import copy

class Literal:
    def __init__(self, negated, predicate, terms):
        self.negated = negated
        self.predicate = predicate
        self.terms = terms

    def __eq__(self, other):
        return (self.negated == other.negated and
                self.predicate == other.predicate and
                self.terms == other.terms)

    def __hash__(self):
        return hash((self.negated, self.predicate, tuple(self.terms)))

    def __repr__(self):
        return f"{'-' if self.negated else ''}{self.predicate}({', '.join(self.terms)})"

class Clause:
    def __init__(self, literals, parents=None):
        self.literals = frozenset(literals)
        self.parents = parents or []
        self.id = None

    def __eq__(self, other):
        return self.literals == other.literals

    def __hash__(self):
        return hash(self.literals)

    def __repr__(self):
        if not self.literals:
            return '<empty>'
        return ' | '.join(sorted(str(lit) for lit in self.literals))

class TheoremProver:
    def __init__(self):
        self.clauses = []
        self.clause_map = {}
        self.set_of_support = deque()
        self.resolution_steps = []
        self.resolution_count = 0

    def parse_input(self, input_lines):
        clause_strs = [line.strip() for line in input_lines if line.strip()]
        query_mode = False
        for clause_str in clause_strs:
            if '---' in clause_str:
                query_mode = True
                continue
            literals = self.parse_clause(clause_str)
            clause = Clause(literals)
            if clause not in self.clause_map:
                self.clauses.append(clause)
                self.clause_map[clause] = len(self.clauses)
                clause.id = len(self.clauses)
            if query_mode:
                self.set_of_support.append(clause)

    def parse_clause(self, clause_str):
        literals = []
        for lit_str in clause_str.split('|'):
            lit_str = lit_str.strip()
            if not lit_str:
                continue
            negated = lit_str.startswith('-')
            predicate_start = 1 if negated else 0
            predicate_end = lit_str.find('(')
            predicate = lit_str[predicate_start:predicate_end]
            terms = lit_str[predicate_end+1:-1].replace(' ', '').split(',')
            literals.append(Literal(negated, predicate, terms))
        return literals

    def standardize_literals(self, literals, suffix):
        var_map = {}
        new_literals = []
        for lit in literals:
            new_terms = []
            for term in lit.terms:
                # Only standardize variables (starting with lowercase)
                if re.match(r'^[a-z]', term):
                    if term not in var_map:
                        var_map[term] = f"{term}_{suffix}"
                    new_terms.append(var_map[term])
                else:
                    new_terms.append(term)
            new_literals.append(Literal(lit.negated, lit.predicate, new_terms))
        return new_literals

    def unify(self, t1, t2, substitution):
        t1 = substitution.get(t1, t1)
        t2 = substitution.get(t2, t2)
        if t1 == t2:
            return substitution
        # if t1 is a variable (lowercase initial)
        if re.match(r'^[a-z]', t1):
            substitution[t1] = t2
            return substitution
        if re.match(r'^[a-z]', t2):
            substitution[t2] = t1
            return substitution
        return None

    def resolve(self, clause1, clause2):
        # Create local standardized copies of both clauses using distinct suffixes.
        std_literals1 = self.standardize_literals(list(clause1.literals), f"{clause1.id}")
        std_literals2 = self.standardize_literals(list(clause2.literals), f"{clause2.id}")
        # Work with lists for resolution
        for i, lit1 in enumerate(std_literals1):
            for j, lit2 in enumerate(std_literals2):
                if lit1.predicate != lit2.predicate or lit1.negated == lit2.negated:
                    continue
                substitution = {}
                valid = True
                # Try to unify the terms of these two literals
                for t1, t2 in zip(lit1.terms, lit2.terms):
                    substitution = self.unify(t1, t2, substitution)
                    if substitution is None:
                        valid = False
                        break
                if not valid:
                    continue
                # Build resolvent from original (non-standardized) literals
                new_literals = set()
                # Include all literals from clause1 except the one resolved on
                for k, orig_lit in enumerate(clause1.literals):
                    # Standardize the original literal with the same suffix as used in std_literals1
                    std_lit = self.standardize_literals([orig_lit], f"{clause1.id}")[0]
                    if std_lit == lit1:
                        continue
                    # Apply substitution to the original literal terms
                    new_terms = [substitution.get(term, term) for term in orig_lit.terms]
                    new_literals.add(Literal(orig_lit.negated, orig_lit.predicate, new_terms))
                # Include all literals from clause2 except the one resolved on
                for k, orig_lit in enumerate(clause2.literals):
                    std_lit = self.standardize_literals([orig_lit], f"{clause2.id}")[0]
                    if std_lit == lit2:
                        continue
                    new_terms = [substitution.get(term, term) for term in orig_lit.terms]
                    new_literals.add(Literal(orig_lit.negated, orig_lit.predicate, new_terms))
                yield Clause(list(new_literals), parents=[clause1, clause2])

    def run_resolution(self):
        visited = set()
        while self.set_of_support:
            current = self.set_of_support.popleft()
            if current.id in visited:
                continue
            visited.add(current.id)

            for clause in self.clauses:
                if clause == current:
                    continue
                for resolvent in self.resolve(current, clause):
                    self.resolution_count += 1
                    if not resolvent.literals:
                        if resolvent not in self.clause_map:
                            self.clauses.append(resolvent)
                            self.clause_map[resolvent] = len(self.clauses)
                        self.resolution_steps.append((current, clause, resolvent))
                        return True
                    if resolvent not in self.clause_map:
                        self.clauses.append(resolvent)
                        self.clause_map[resolvent] = len(self.clauses)
                        self.set_of_support.append(resolvent)
                        self.resolution_steps.append((current, clause, resolvent))
        return False

    def print_output(self, success):
        print("Input Clauses:")
        for idx, clause in enumerate(self.clauses, 1):
            print(f"{idx}: {clause}")

        print("\nResolution steps:")
        if not success:
            print("No proof exists.")
            return

        for step in self.resolution_steps:
            c1_id = self.clause_map[step[0]]
            c2_id = self.clause_map[step[1]]
            result_id = self.clause_map[step[2]]
            print(f"{c1_id} and {c2_id} give {result_id}: {step[2]}")

        print(f"\n{self.resolution_count} total resolutions")

def main():
    prover = TheoremProver()
    input_lines = sys.stdin.readlines()
    prover.parse_input(input_lines)
    success = prover.run_resolution()
    prover.print_output(success)

if __name__ == "__main__":
    main()
