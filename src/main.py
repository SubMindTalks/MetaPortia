from pathlib import Path
from .github_fetcher import GitHubFetcher
from .code_analysis import CodeAnalyzer
from .code_generator import CodeGenerator
from .utils import load_config

def main():
    config = load_config()
    
    # Initialize components
    fetcher = GitHubFetcher(config)
    analyzer = CodeAnalyzer(config)
    generator = CodeGenerator(config)
    
    # Main processing pipeline
    repos = fetcher.fetch_repositories()
    patterns = analyzer.analyze_repositories(repos)
    generator.generate_code(patterns)

if __name__ == "__main__":
    main()