# main.py
from program_synthesizer import ProgramSynthesizer, print_render_tree

# Function for testing with input-output examples
def test_synthesizer(synthesizer):
    examples = [
        ('"1/17/16-1/18/17"', 1, '"1/17/16"'),
        ('"1/17/16-1/18/17"', 2, '"1/18/17"'),
        ('"01/17/2016-01/18/2017"', 1, '"01/17/2016"'),
        ('"01/17/2016-01/18/2017"', 2, '"01/18/2017"'),
    ]

    for example in examples:
        input_str, output_index, expected_output = example
        program = synthesizer.generate_program_of_size(5)
        fitness = synthesizer.evaluate_program(program, expected_output)
        synthesizer.update_probabilistic_model(program, fitness)
        print(f"Input: {input_str}, Output Index: {output_index}, Expected Output: {expected_output}")
        print(f"Generated Program: {program}")
        print(f"Evaluation Fitness: {fitness}")
        print()

# Example usage
if __name__ == "__main__":
    # Define a grammar
    grammar = {
        'S': ['arg', 'concat', 'replace'],
        'arg': ['"a"', '"b"', '"c"', '"d"'],
        'concat': ['(concat S S)'],
        'replace': ['(replace S S S)'],
    }

    # Create an instance of ProgramSynthesizer
    synthesizer = ProgramSynthesizer(grammar)

    # Perform guided bottom-up search
    synthesizer.guided_bottom_up_search(max_iterations=3)

    # Access the generated programs
    print("Generated Programs:")
    for i, program in enumerate(synthesizer.generated_programs, start=1):
        print(f"{i}. {program}")

    # Test with input-output examples
    test_synthesizer(synthesizer)
