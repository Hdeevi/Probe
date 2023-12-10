# pcfg.py
class ProbabilisticContextFreeGrammar:
    def __init__(self, grammar):
        self.productions = {}

    def update_probabilities(self, syntax_tree, fitness):
        self.count_productions(syntax_tree, fitness)
        self.calculate_probabilities()

    def count_productions(self, node, fitness):
        if node.children:
            nonterminal = node.name
            if nonterminal not in self.productions:
                self.productions[nonterminal] = {}
            production = ' '.join(child.name for child in node.children)
            if production not in self.productions[nonterminal]:
                self.productions[nonterminal][production] = fitness
            else:
                self.productions[nonterminal][production] += fitness
            for child in node.children:
                self.count_productions(child, fitness)

    def calculate_probabilities(self):
        for nonterminal, productions in self.productions.items():
            total_count = sum(productions.values())
            probabilities = {p: count / total_count if total_count != 0 else 0 for p, count in productions.items()}
            self.productions[nonterminal] = probabilities

        print("Updated Probabilities:")
        for nonterminal, probabilities in self.productions.items():
            print(f"{nonterminal}: {probabilities}")
