import ast
import random
import string
import astor


class PythonObfuscator:
    def __init__(self):
        # Keep track of name mappings for consistency
        self.name_mappings = {}
        # Characters to use for random names (avoid l, I, O for readability)
        self.name_chars = string.ascii_letters.replace('l', '').replace('I', '').replace('O', '')
        # Names that shouldn't be obfuscated
        self.protected_names = {
            'self', 'cls', '__init__', '__main__', '__name__', 'Exception',
            'True', 'False', 'None', 'print', 'range', 'len', 'str', 'int',
            'float', 'list', 'dict', 'set', 'tuple'
        }
        # Counter for generating unique names
        self.name_counter = 0

    def generate_name(self) -> str:
        """Generate a new random single-character name."""
        while True:
            # First try single characters
            if self.name_counter < len(self.name_chars):
                name = self.name_chars[self.name_counter]
                self.name_counter += 1
                return name
            # If we run out of single characters, use combinations
            else:
                name = random.choice(self.name_chars) + str(self.name_counter)
                self.name_counter += 1
                return name

    def get_obfuscated_name(self, original_name: str) -> str:
        """Get or create an obfuscated name for a given original name."""
        if original_name in self.protected_names:
            return original_name

        if original_name not in self.name_mappings:
            self.name_mappings[original_name] = self.generate_name()
        return self.name_mappings[original_name]

    class NameObfuscator(ast.NodeTransformer):
        """AST transformer for obfuscating names."""

        def __init__(self, obfuscator):
            self.obfuscator = obfuscator

        def visit_Name(self, node):
            node.id = self.obfuscator.get_obfuscated_name(node.id)
            return node

        def visit_FunctionDef(self, node):
            # Obfuscate function name
            node.name = self.obfuscator.get_obfuscated_name(node.name)

            # Remove return type annotation
            node.returns = None

            # Process arguments
            if node.args:
                # Remove type annotations from arguments
                for arg in node.args.args:
                    arg.annotation = None
                    arg.id = self.obfuscator.get_obfuscated_name(arg.id)

            # Remove docstring if it exists
            if ast.get_docstring(node):
                node.body = node.body[1:]

            # Continue processing child nodes
            node = self.generic_visit(node)
            return node

        def visit_ClassDef(self, node):
            # Obfuscate class name
            node.name = self.obfuscator.get_obfuscated_name(node.name)

            # Remove docstring if it exists
            if ast.get_docstring(node):
                node.body = node.body[1:]

            # Continue processing child nodes
            node = self.generic_visit(node)
            return node

        def visit_Attribute(self, node):
            # Obfuscate attribute names except for special methods
            if not (isinstance(node.attr, str) and node.attr.startswith('__')):
                node.attr = self.obfuscator.get_obfuscated_name(node.attr)
            return self.generic_visit(node)

    class CommentAndTypeRemover(ast.NodeTransformer):
        """AST transformer for removing comments and type hints."""

        def visit_AnnAssign(self, node):
            # Convert type-annotated assignments to regular assignments
            return ast.Assign(targets=[node.target], value=node.value)

        def visit_Expr(self, node):
            # Remove standalone strings (likely comments)
            if isinstance(node.value, ast.Str):
                return None
            return node

    def obfuscate(self, source_code: str) -> str:
        """
        Obfuscate the given Python source code.

        Args:
            source_code: The source code to obfuscate

        Returns:
            The obfuscated source code
        """
        # Parse the source code into an AST
        tree = ast.parse(source_code)

        # Remove comments and type hints
        tree = self.CommentAndTypeRemover().visit(tree)

        # Obfuscate names
        tree = self.NameObfuscator(self).visit(tree)

        # Fix any missing locations
        ast.fix_missing_locations(tree)

        # Generate obfuscated source code
        return astor.to_source(tree)


# Example usage
if __name__ == "__main__":
    # Sample code to obfuscate
    sample_code = '''
    class Calculator:
        """A simple calculator class."""

        def __init__(self, initial_value: int = 0):
            """Initialize the calculator."""
            self.value: int = initial_value

        def add(self, x: int) -> int:
            """Add a number to the current value."""
            # Add the number
            self.value += x
            return self.value

        def get_value(self) -> int:
            """Return the current value."""
            return self.value

    def main():
        # Create calculator
        calc = Calculator(10)
        result = calc.add(5)
        print(f"Result: {result}")
    '''

    obfuscator = PythonObfuscator()
    obfuscated_code = obfuscator.obfuscate(sample_code)
    print("Original code:")
    print(sample_code)
    print("\nObfuscated code:")
    print(obfuscated_code)