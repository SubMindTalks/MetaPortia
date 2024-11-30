from github import Github

class GitHubFetcher:
    def __init__(self, token):
        self.github = Github(token)

    def fetch_repos(self, query, max_results=10):
        repos = self.github.search_repositories(query=query)
        return [{"name": repo.full_name, "url": repo.clone_url} for repo in repos[:max_results]]
