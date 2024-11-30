import argparse
from src.lexer import Lexer
from src.parser import Parser
from src.codeGenerator import CodeGenerator
from src.utils import load_data, analyze_results

def main():
    parser = argparse.ArgumentParser(description="MetaPortia DSL Analysis Tool")
    parser.add_argument("--file", type=str, help="Path to the input file")
    parser.add_argument("--github", action="store_true", help="Pull data from GitHub")
    args = parser.parse_args()

    if args.file:
        print(f"Processing file: {args.file}")
        data = load_data(args.file)
        tokens = Lexer().tokenize(data)
        ast = Parser().parse(tokens)
        CodeGenerator().generate(ast)
        analyze_results(ast)

    if args.github:
        print("Pulling data from GitHub...")
        # GitHub data pull logic
        pull_github_data()

def pull_github_data():
    # Placeholder for GitHub API integration
    print("GitHub data integration coming soon.")

if __name__ == "__main__":
    main()
