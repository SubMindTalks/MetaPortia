import requests
import time
from datetime import datetime
from typing import Dict, List, Optional
import json
from collections import defaultdict


class GitHubImplementationAnalyzer:
    def __init__(self, token: Optional[str] = None, rate_limit_interval: float = 1.0):
        self.headers = {
            'Accept': 'application/vnd.github.v3+json'
        }
        if token:
            self.headers['Authorization'] = f'token {token}'
        self.rate_limit_interval = rate_limit_interval  # Time between requests in seconds

        self.implementation_languages = {
            'Python': ['.py'],
            'Rust': ['.rs'],
            'OCaml': ['.ml', '.mli'],
            'Haskell': ['.hs', '.lhs'],
            'Go': ['.go'],
            'Ruby': ['.rb'],
            'TypeScript': ['.ts'],
            'JavaScript': ['.js'],
            'C++': ['.cpp', '.hpp', '.cc', '.hh'],
            'C#': ['.cs'],
            'Java': ['.java'],
            'Kotlin': ['.kt'],
            'Swift': ['.swift'],
            'Scala': ['.scala'],
            'Clojure': ['.clj'],
            'Erlang': ['.erl'],
            'F#': ['.fs', '.fsx'],
            'Elixir': ['.ex', '.exs'],
            'Dart': ['.dart'],
            'Nim': ['.nim'],
            'Crystal': ['.cr'],
            'Zig': ['.zig']
        }

    def make_request(self, url: str, params: Dict = None) -> Optional[requests.Response]:
        """Make a request with retry logic for rate-limiting errors."""
        while True:
            try:
                response = requests.get(url, headers=self.headers, params=params)
                if response.status_code == 403 and "X-RateLimit-Remaining" in response.headers:
                    reset_time = int(response.headers.get("X-RateLimit-Reset", time.time() + 60))
                    sleep_duration = max(1, reset_time - time.time())
                    print(f"Rate limit reached. Sleeping for {sleep_duration} seconds...")
                    time.sleep(sleep_duration)
                    continue
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                print(f"Request error: {e}. Retrying in {self.rate_limit_interval} seconds...")
                time.sleep(self.rate_limit_interval)

    def get_all_forks(self, owner: str, repo: str) -> List[Dict]:
        """Fetch all forks of a repository."""
        all_forks = []
        page = 1
        per_page = 100
        while True:
            url = f'https://api.github.com/repos/{owner}/{repo}/forks'
            params = {'per_page': per_page, 'page': page}
            response = self.make_request(url, params)
            if not response:
                break
            forks = response.json()
            if not forks:
                break
            all_forks.extend(forks)
            page += 1
            time.sleep(self.rate_limit_interval)
        return all_forks

    def get_repository_tree(self, owner: str, repo: str, branch: str = 'main') -> List[Dict]:
        """Get the file tree of a repository."""
        url = f'https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1'
        response = self.make_request(url)
        if response and response.status_code == 404:
            # Retry with 'master' branch if 'main' is not found
            url = f'https://api.github.com/repos/{owner}/{repo}/git/trees/master?recursive=1'
            response = self.make_request(url)
        return response.json().get('tree', []) if response else []

    def detect_implementation_language(self, tree: List[Dict]) -> Dict[str, int]:
        """Detect implementation languages based on file extensions and sizes."""
        language_sizes = defaultdict(int)
        for item in tree:
            if item['type'] != 'blob':
                continue
            path = item['path'].lower()
            size = item['size']
            if any(x in path for x in ['/test/', '/docs/', '/examples/', '/samples/']):
                continue
            for lang, extensions in self.implementation_languages.items():
                if any(path.endswith(ext) for ext in extensions):
                    language_sizes[lang] += size
                    break
        return dict(language_sizes)

    def analyze_forks(self, owner: str, repo: str, min_size_bytes: int = 1000) -> Dict:
        """Analyze forks to detect implementation languages."""
        all_forks = self.get_all_forks(owner, repo)
        total_forks = len(all_forks)
        print(f"Total forks found: {total_forks}")
        implementations = []
        for i, fork in enumerate(all_forks, 1):
            print(f"\rAnalyzing fork {i}/{total_forks}...", end='')
            try:
                fork_owner, fork_name = fork['full_name'].split('/')
                tree = self.get_repository_tree(fork_owner, fork_name)
                language_sizes = self.detect_implementation_language(tree)
                significant_languages = {
                    lang: size for lang, size in language_sizes.items()
                    if size >= min_size_bytes
                }
                if significant_languages:
                    primary_language = max(significant_languages.items(), key=lambda x: x[1])[0]
                    implementations.append({
                        'name': fork['full_name'],
                        'url': fork['html_url'],
                        'stars': fork.get('stargazers_count', 0),
                        'last_updated': fork.get('updated_at', 'Unknown'),
                        'primary_language': primary_language,
                        'language_sizes': significant_languages,
                        'total_implementation_size': sum(significant_languages.values())
                    })
                time.sleep(self.rate_limit_interval)
            except Exception as e:
                print(f"\nError analyzing fork {fork['full_name']}: {e}")
        implementations.sort(key=lambda x: x['stars'], reverse=True)
        by_language = defaultdict(list)
        for impl in implementations:
            by_language[impl['primary_language']].append(impl)
        return {
            'total_forks': total_forks,
            'implementations': implementations,
            'by_language': dict(by_language)
        }

    def print_results(self, results: Dict) -> None:
        """Print analysis results in a readable format."""
        print("\n\nImplementations found by language:")
        for language, implementations in results['by_language'].items():
            print(f"\n{language} Implementations ({len(implementations)}):")
            print("-" * 50)
            for impl in implementations:
                print(f"Repository: {impl['name']} | Stars: {impl['stars']} | Last Updated: {impl['last_updated']}")
                print(f"  URL: {impl['url']}")
                print(
                    f"  Languages: {', '.join(f'{lang} ({size:,} bytes)' for lang, size in impl['language_sizes'].items())}")
        print(f"\nSummary: Total forks: {results['total_forks']} | Implementations: {len(results['implementations'])}")


def main():
    analyzer = GitHubImplementationAnalyzer()
    results = analyzer.analyze_forks('munificent', 'craftinginterpreters')
    analyzer.print_results(results)
    with open('language_implementations.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
        print("\nResults saved to language_implementations.json")


if __name__ == '__main__':
    main()
