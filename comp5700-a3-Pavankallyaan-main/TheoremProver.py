import sys
import re
from copy import deepcopy

class Literal:
    def __init__(self, negated, predicate, terms):
        self.negated = negated
        self.predicate = predicate
        self.terms = terms

    def __repr__(self):
        return f"{'-' if self.negated else ''}{self.predicate}({', '.join(self.terms)})"

class TheoremProver:
    def __init__(self):
        self.clauses = []
        self.unifications_attempted = 0

    def parse_input(self, input_lines):
        for line in input_lines:
            line = line.strip()
            if line:
                self.clauses.append(self.parse_clause(line))

    def parse_clause(self, clause_str):
        literals = []
        for lit_str in clause_str.split("|"):
            lit_str = lit_str.strip()
            negated = lit_str.startswith('-')
            predicate_start = 1 if negated else 0
            predicate_end = lit_str.find('(')
            predicate = lit_str[predicate_start:predicate_end].strip()
            terms_str = lit_str[predicate_end+1:-1].strip()
            terms = [t.strip() for t in terms_str.split(',')]
            literals.append(Literal(negated, predicate, terms))
        return literals

    def unify_term(self, term1, term2, substitution):
        term1 = substitution.get(term1, term1)
        term2 = substitution.get(term2, term2)
        if term1 == term2:
            return substitution
        if re.match(r'^[a-z]', term1):
            substitution[term1] = term2
            return substitution
        if re.match(r'^[a-z]', term2):
            substitution[term2] = term1
            return substitution
        return None

    def unify_literals(self, lit1, lit2):
        if lit1.predicate != lit2.predicate or lit1.negated == lit2.negated:
            return None
        if len(lit1.terms) != len(lit2.terms):
            return None
        substitution = {}
        for t1, t2 in zip(lit1.terms, lit2.terms):
            sub = self.unify_term(t1, t2, substitution)
            if sub is None:
                return None
            substitution = sub
        return substitution

    def apply_substitution(self, clause, substitution):
        new_clause = []
        for lit in clause:
            new_terms = []
            for term in lit.terms:
                new_term = substitution.get(term, term)
                new_terms.append(new_term)
            new_lit = Literal(lit.negated, lit.predicate, new_terms)
            new_clause.append(new_lit)
        return new_clause

    def find_unifications(self):
        unified_pairs = []
        if len(self.clauses) != 2:
            return unified_pairs
        clause1, clause2 = self.clauses
        for lit1 in clause1:
            for lit2 in clause2:
                self.unifications_attempted += 1
                substitution = self.unify_literals(lit1, lit2)
                if substitution is not None:
                    new_clause1 = self.apply_substitution(clause1, substitution)
                    new_clause2 = self.apply_substitution(clause2, substitution)
                    unified_pairs.append((new_clause1, new_clause2))
        return unified_pairs

    def print_results(self, unified_pairs):
        print("Input Clauses:")
        for idx, clause in enumerate(self.clauses, 1):
            print(f"{idx}. {' | '.join(map(str, clause))}")
        print("\nUnified Clauses:")
        for pair in unified_pairs:
            clause1_str = ' | '.join(map(str, pair[0]))
            clause2_str = ' | '.join(map(str, pair[1]))
            print(f"{clause1_str}\n{clause2_str}\n")
        print(f"Attempted {self.unifications_attempted} unifications.")

def main():
    prover = TheoremProver()
    input_lines = [line.strip() for line in sys.stdin if line.strip()]
    prover.parse_input(input_lines)
    unified_pairs = prover.find_unifications()
    prover.print_results(unified_pairs)

if __name__ == "__main__":
    main()