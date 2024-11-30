class CodeGenerator:
    def __init__(self):
        self.generated_code = ""

    def generate(self, ast):
        for statement in ast:
            if statement["type"] == "DEFINE":
                self.generated_code += f"{statement['var_name']} = {statement['value']}\n"

    def save(self, output_file):
        with open(output_file, "w") as f:
            f.write(self.generated_code)
