"""
Extractor factory for WebMainBench.
"""

from typing import Dict, Any, Type, List
import inspect
import importlib
import pkgutil
from .base import BaseExtractor


def extractor(name: str):
    """
    Decorator to automatically register an extractor.
    
    Args:
        name: Name to register the extractor under
    
    Example:
        @extractor("llm-webkit")
        class LlmWebkitExtractor(BaseExtractor):
            pass
    """
    def decorator(cls: Type[BaseExtractor]):
        ExtractorFactory.register(name, cls)
        return cls
    return decorator


class ExtractorFactory:
    """Factory for creating extractors."""
    
    _registry: Dict[str, Type[BaseExtractor]] = {}
    
    @classmethod
    def register(cls, name: str, extractor_class: Type[BaseExtractor]) -> None:
        """
        Register an extractor class.
        
        Args:
            name: Name to register the extractor under
            extractor_class: Extractor class to register
        """
        cls._registry[name] = extractor_class
    
    @classmethod
    def create(cls, name: str, config: Dict[str, Any] = None) -> BaseExtractor:
        """
        Create an extractor instance.
        
        Args:
            name: Name of the extractor to create
            config: Configuration for the extractor
            
        Returns:
            BaseExtractor instance
            
        Raises:
            ValueError: If extractor name is not registered
        """
        if name not in cls._registry:
            raise ValueError(f"Unknown extractor: {name}. Available: {list(cls._registry.keys())}")
        
        extractor_class = cls._registry[name]
        return extractor_class(name=name, config=config)
    
    @classmethod
    def list_available(cls) -> List[str]:
        """List all available extractor names."""
        return list(cls._registry.keys())
    
    @classmethod
    def get_info(cls, name: str) -> Dict[str, Any]:
        """
        Get information about a registered extractor.
        
        Args:
            name: Name of the extractor
            
        Returns:
            Dictionary with extractor information
        """
        if name not in cls._registry:
            raise ValueError(f"Unknown extractor: {name}")
        
        extractor_class = cls._registry[name]
        return {
            "name": name,
            "class": extractor_class.__name__,
            "module": extractor_class.__module__,
            "description": getattr(extractor_class, 'description', ''),
            "version": getattr(extractor_class, 'version', 'unknown'),
        }
    
    @classmethod
    def create_multiple(cls, extractors_config: Dict[str, Dict[str, Any]]) -> Dict[str, BaseExtractor]:
        """
        Create multiple extractors from configuration.
        
        Args:
            extractors_config: Dictionary mapping extractor names to their configs
            
        Returns:
            Dictionary mapping names to extractor instances
        """
        extractors = {}
        for name, config in extractors_config.items():
            try:
                extractor = cls.create(name, config)
                extractors[name] = extractor
            except Exception as e:
                print(f"Warning: Failed to create extractor '{name}': {e}")
                continue
        
        return extractors


    @classmethod
    def auto_discover(cls):
        """
        Automatically discover and import all extractor modules in the extractors package.
        This triggers the @extractor decorators to register the extractors.
        """
        import webmainbench.extractors as extractors_package
        
        # Get the path of the extractors package
        package_path = extractors_package.__path__
        
        # Walk through all modules in the extractors package
        for importer, modname, ispkg in pkgutil.iter_modules(package_path):
            if not ispkg and modname.endswith('_extractor'):
                try:
                    # Import the module to trigger @extractor decorators
                    importlib.import_module(f'webmainbench.extractors.{modname}')
                except ImportError as e:
                    # Silently ignore import errors for optional dependencies
                    pass


# Auto-discover extractors on module import
ExtractorFactory.auto_discover() 