import yaml
from pathlib import Path
from typing import Dict

def load_config() -> Dict:
    """Load configuration from config.yaml."""
    config_path = Path('config.yaml')
    with open(config_path) as f:
        return yaml.safe_load(f)

        # Define a function to load data from data.yaml
        def load_data() -> Dict:
            """Load data from data.yaml."""
            data_path = Path('data.yaml')
            with open(data_path) as f:
                return yaml.safe_load(f)
