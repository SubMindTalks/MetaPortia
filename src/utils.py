import yaml
from pathlib import Path
from typing import Dict

def load_config() -> Dict:
    """Load configuration from config.yaml."""
    config_path = Path('config.yaml')
    with open(config_path) as f:
        return yaml.safe_load(f)