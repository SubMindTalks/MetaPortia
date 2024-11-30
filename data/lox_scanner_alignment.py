import requests
import os
from github import Github
import ast
import re
from Bio import pairwise2
from Bio.Cluster import kcluster
from Bio import Align
import numpy as np
from typing import List, Dict, Tuple
import pandas as pd
from pathlib import Path


class CodeNormalizer:
    def __init__(self):
        # Define common code words that shouldn't be stemmed
        self.code_words = {
            'while', 'for', 'if', 'else', 'elif', 'try', 'except', 'finally',
            'class', 'def', 'return', 'yield', 'break', 'continue', 'pass',
            'raise', 'with', 'as', 'import', 'from', 'global', 'nonlocal'
        }

    def remove_comments_and_docstrings(self, code: str) -> str:
        """Remove comments and docstrings from Python code."""
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                # Remove docstrings
                if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                    if ast.get_docstring(node):
                        node.body = node.body[1:]

            # Convert back to string and remove comments
            cleaned = ast.unparse(tree)
            cleaned = re.sub(r'#.*$', '', cleaned, flags=re.MULTILINE)
            return cleaned
        except:
            # Fallback if parsing fails
            return code

    def remove_type_annotations(self, code: str) -> str:
        """Remove type annotations from Python code."""
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.AnnAssign):
                    node.annotation = None
                elif isinstance(node, ast.FunctionDef):
                    node.returns = None
                    for arg in node.args.args:
                        arg.annotation = None
            return ast.unparse(tree)
        except:
            return code

    def simple_stem(self, word: str) -> str:
        """Very simple stemming rules for code."""
        if word in self.code_words:
            return word

        # Remove common suffixes
        suffixes = ['ing', 'ed', 'er', 'ers', 'tion', 'ations', 'ment', 'ments']
        for suffix in suffixes:
            if word.endswith(suffix) and len(word) > len(suffix) + 2:
                return word[:-len(suffix)]
        return word

    def tokenize(self, text: str) -> List[str]:
        """Simple tokenization for code."""
        # Split on whitespace and punctuation
        tokens = re.findall(r'[a-zA-Z_]\w*|[^\w\s]', text)
        return tokens

    def normalize_text(self, code: str) -> str:
        """Normalize code text using simple string processing."""
        # Tokenize
        tokens = self.tokenize(code)
        # Lowercase and stem
        normalized = [self.simple_stem(token.lower()) for token in tokens]
        # Join without whitespace
        return ''.join(normalized)

    def process_code(self, code: str) -> str:
        """Apply all normalization steps."""
        code = self.remove_comments_and_docstrings(code)
        code = self.remove_type_annotations(code)
        code = self.normalize_text(code)
        return code


class GithubScanner:
    def __init__(self, token: str):
        self.github = Github(token)

    def find_craftinginterpreters_repos(self) -> List[Dict]:
        """Find Python repositories implementing craftinginterpreters."""
        query = "craftinginterpreters language:python"
        repositories = []

        for repo in self.github.search_repositories(query):
            repositories.append({
                'full_name': repo.full_name,
                'url': repo.html_url,
                'default_branch': repo.default_branch
            })

        return repositories

    def get_scanner_class(self, repo_info: Dict) -> str:
        """Extract scanner class code from a repository."""
        try:
            # Common paths where scanner might be located
            possible_paths = [
                f"scanner.py",
                f"src/scanner.py",
                f"lox/scanner.py",
                f"craftinginterpreters/scanner.py"
            ]

            base_url = f"https://raw.githubusercontent.com/{repo_info['full_name']}/{repo_info['default_branch']}"

            for path in possible_paths:
                response = requests.get(f"{base_url}/{path}")
                if response.status_code == 200:
                    content = response.text
                    # Basic check if it contains a scanner class
                    if "class Scanner" in content:
                        # Extract just the Scanner class
                        scanner_match = re.search(r'class\s+Scanner.*?(?=class|\Z)',
                                                  content, re.DOTALL)
                        if scanner_match:
                            return scanner_match.group(0)
                        return content

            return ""
        except:
            return ""


class SequenceAnalyzer:
    def __init__(self):
        self.aligner = Align.PairwiseAligner()
        self.aligner.mode = 'global'

    def align_sequences(self, sequences: List[str]) -> Tuple[List[str], np.ndarray]:
        """Perform multiple sequence alignment on normalized code."""
        n = len(sequences)
        scores = np.zeros((n, n))

        # Compute pairwise alignment scores
        for i in range(n):
            for j in range(i + 1, n):
                score = self.aligner.align(sequences[i], sequences[j]).score
                scores[i, j] = score
                scores[j, i] = score

        return sequences, scores

    def cluster_sequences(self, scores: np.ndarray, k: int = 3) -> Tuple[List[int], List[List[int]]]:
        """Cluster sequences based on alignment scores."""
        # Convert similarity scores to distances
        max_score = np.max(scores)
        distances = max_score - scores

        # Perform k-means clustering
        clusterid, error, nfound = kcluster(distances, nclusters=k)

        # Group sequences by cluster
        clusters = [[] for _ in range(k)]
        for i, cluster_id in enumerate(clusterid):
            clusters[cluster_id].append(i)

        return clusterid, clusters

    def find_common_subsequences(self, sequences: List[str], min_length: int = 10) -> List[str]:
        """Find common subsequences across all sequences in a cluster."""
        if not sequences:
            return []

        def find_substring_positions(s: str, sub: str) -> List[int]:
            positions = []
            start = 0
            while True:
                pos = s.find(sub, start)
                if pos == -1:
                    break
                positions.append(pos)
                start = pos + 1
            return positions

        # Start with the shortest sequence to reduce search space
        base = min(sequences, key=len)
        common_subs = []

        # Try all possible substrings of the base sequence
        for length in range(min_length, len(base) + 1):
            for start in range(len(base) - length + 1):
                substr = base[start:start + length]

                # Check if this substring appears in all sequences
                if all(substr in seq for seq in sequences):
                    common_subs.append(substr)

        # Sort by length, longest first
        return sorted(common_subs, key=len, reverse=True)

    def generate_template(self, sequences: List[str], cluster_indices: List[int]) -> str:
        """Generate a template from the most common sequence patterns in a cluster."""
        if not cluster_indices:
            return ""

        cluster_sequences = [sequences[i] for i in cluster_indices]

        # Find common subsequences
        common_subs = self.find_common_subsequences(cluster_sequences)

        if not common_subs:
            return sequences[cluster_indices[0]]  # Fallback to first sequence

        # Take the top most common subsequences that cover most of the code
        template_parts = common_subs[:5]  # Adjust number as needed

        # Join the parts with placeholders
        template = "..."
        for part in template_parts:
            template += part + "..."

        return template


def main():
    # Initialize components
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise ValueError("Please set GITHUB_TOKEN environment variable")

    github_scanner = GithubScanner(github_token)
    code_normalizer = CodeNormalizer()
    sequence_analyzer = SequenceAnalyzer()

    # Find repositories
    print("Finding repositories...")
    repos = github_scanner.find_craftinginterpreters_repos()

    # Extract and normalize scanner code
    print("Extracting and normalizing scanner code...")
    normalized_scanners = []
    repo_info = []
    for repo in repos:
        code = github_scanner.get_scanner_class(repo)
        if code:
            normalized = code_normalizer.process_code(code)
            normalized_scanners.append(normalized)
            repo_info.append(repo)

    # Perform sequence alignment and clustering
    print("Performing sequence analysis...")
    sequences, scores = sequence_analyzer.align_sequences(normalized_scanners)
    cluster_ids, clusters = sequence_analyzer.cluster_sequences(scores)

    # Generate templates for each cluster
    print("Generating templates...")
    templates = []
    for cluster in clusters:
        template = sequence_analyzer.generate_template(sequences, cluster)
        templates.append(template)

    # Create results directory
    Path("results").mkdir(exist_ok=True)

    # Save results
    with open("results/templates.txt", "w") as f:
        for i, template in enumerate(templates):
            f.write(f"=== Cluster {i} Template ===\n")
            f.write(template)
            f.write("\n\n")

    # Create a DataFrame with results
    results_df = pd.DataFrame({
        'repository': [repo['full_name'] for repo in repo_info],
        'cluster': cluster_ids,
        'code_length': [len(seq) for seq in sequences]
    })
    results_df.to_csv("results/analysis_results.csv", index=False)

    # Save the original code samples
    with open("results/original_samples.txt", "w") as f:
        for i, (repo, code) in enumerate(zip(repo_info, normalized_scanners)):
            f.write(f"=== Sample {i} from {repo['full_name']} ===\n")
            f.write(code)
            f.write("\n\n")


if __name__ == "__main__":
    main()