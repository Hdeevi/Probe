# program_synthesizer.py
import random
from anytree import Node, RenderTree
from pcfg import ProbabilisticContextFreeGrammar

class ProgramSynthesizer:
    def __init__(self, grammar):
        self.grammar = grammar
        self.pcfg = ProbabilisticContextFreeGrammar(grammar)
# List to store generated programs
        self.generated_programs = []  

    def guided_bottom_up_search(self, max_iterations=10):
        for _ in range(max_iterations):
            program = self.generate_program_of_size(5)
            expected_output = '"1/17/16"'  
            fitness = self.evaluate_program(program, expected_output)
            if fitness is not None:
                self.update_probabilistic_model(program, fitness)
# Storing the generated program
                self.generated_programs.append(program)  

    def generate_program_of_size(self, size):
        non_terminal = 'S'
        program = self.expand_symbol(non_terminal, size)
        program = self.remove_concat_replace(program)
        print(f"Generated Program: {program}")
        return program

    def expand_symbol(self, symbol, size):
        if size <= 0 or symbol not in self.grammar:
            return symbol

        production = random.choice(self.grammar[symbol])
        subexpressions = [self.expand_symbol(s, size - 1) for s in production.split()]
        return ' '.join(subexpressions)

    def remove_concat_replace(self, program):
        return ' '.join(token for token in program.split() if token not in {'concat', 'replace'})

    def evaluate_program(self, program, expected_output):
        if not program:
            print("Empty program. Skipping evaluation.")
            return None

        matching_characters = sum(c1 == c2 for c1, c2 in zip(program, expected_output))
        fitness = matching_characters / len(expected_output)
        print(f"Evaluating program: {program}, Fitness: {fitness}")
        return fitness

    def update_probabilistic_model(self, program, fitness):
        syntax_tree = self.generate_syntax_tree(program)
        if syntax_tree is not None:
            print(f"Syntax Tree:")
            print_render_tree(syntax_tree)
            self.pcfg.update_probabilities(syntax_tree, fitness)

    def generate_syntax_tree(self, program):
        if not program:
            print("Empty program. Skipping syntax tree generation.")
            return None

        root = Node("Root")
        symbols = program.split()
        self._build_syntax_tree(root, symbols)
        return root

    def _build_syntax_tree(self, parent, symbols):
        concat_node = None
        replace_node = None
        skip_next_symbols = False

        for symbol in symbols:
            if skip_next_symbols:
                skip_next_symbols = False
                continue

            if symbol == 'concat':
                concat_node = Node(symbol, parent=parent)
                skip_next_symbols = True
            elif symbol == 'replace':
                replace_node = Node(symbol, parent=parent)
                skip_next_symbols = True
            elif concat_node is not None and replace_node is not None:
                Node(symbol, parent=parent)
            elif concat_node is not None:
                Node(symbol, parent=concat_node)
            elif replace_node is not None:
                Node(symbol, parent=replace_node)
            elif symbol in self.grammar:
                child = Node(symbol, parent=parent)
                self._build_syntax_tree(child, self.grammar[symbol][0].split())
            else:
                Node(symbol, parent=parent)

def print_render_tree(tree):
    for pre, fill, node in RenderTree(tree):
        print(f"{pre}{node.name}")
