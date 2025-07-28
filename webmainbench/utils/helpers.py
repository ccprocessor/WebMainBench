"""
Helper functions for WebMainBench.
"""

import logging
import sys
from typing import Dict, Any, List
from pathlib import Path


def setup_logging(level: str = "INFO", log_file: str = None) -> None:
    """
    Setup logging configuration.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional log file path
    """
    log_level = getattr(logging, level.upper(), logging.INFO)
    
    # Configure logging format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Setup handlers
    handlers = [logging.StreamHandler(sys.stdout)]
    
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file))
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
    )


def validate_config(config: Dict[str, Any], required_keys: List[str]) -> bool:
    """
    Validate configuration dictionary.
    
    Args:
        config: Configuration dictionary
        required_keys: List of required keys
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(config, dict):
        return False
    
    missing_keys = [key for key in required_keys if key not in config]
    if missing_keys:
        print(f"Missing required configuration keys: {missing_keys}")
        return False
    
    return True


def format_results(results: Dict[str, Any], precision: int = 4) -> str:
    """
    Format evaluation results for display.
    
    Args:
        results: Results dictionary
        precision: Number of decimal places
        
    Returns:
        Formatted string
    """
    lines = []
    
    # Overall metrics
    if 'overall_metrics' in results:
        lines.append("=== Overall Metrics ===")
        for metric, score in results['overall_metrics'].items():
            if isinstance(score, (int, float)):
                lines.append(f"{metric}: {score:.{precision}f}")
            else:
                lines.append(f"{metric}: {score}")
        lines.append("")
    
    # Category metrics
    if 'category_metrics' in results and results['category_metrics']:
        lines.append("=== Category Metrics ===")
        for category, metrics in results['category_metrics'].items():
            lines.append(f"\n{category}:")
            for metric, score in metrics.items():
                if isinstance(score, (int, float)):
                    lines.append(f"  {metric}: {score:.{precision}f}")
                else:
                    lines.append(f"  {metric}: {score}")
        lines.append("")
    
    # Error analysis
    if 'error_analysis' in results and results['error_analysis']:
        lines.append("=== Error Analysis ===")
        error_info = results['error_analysis']
        lines.append(f"Success Rate: {error_info.get('success_rate', 0):.2%}")
        lines.append(f"Failed Samples: {error_info.get('failed_count', 0)}")
        
        if 'common_errors' in error_info:
            lines.append("\nCommon Errors:")
            for error_type, count in error_info['common_errors'].items():
                lines.append(f"  {error_type}: {count}")
    
    return "\n".join(lines) 