"""
Text-based metrics for WebMainBench.
"""

from typing import Dict, Any, List
import difflib
from .base import BaseMetric, MetricResult


class EditDistanceMetric(BaseMetric):
    """Edit distance (Levenshtein distance) metric."""
    
    version = "1.0.0"
    description = "Character-level edit distance metric"
    
    def _setup(self) -> None:
        """Setup the edit distance metric."""
        self.normalize = self.config.get('normalize', True)
    
    def _calculate_score(self, predicted: str, groundtruth: str, **kwargs) -> MetricResult:
        """
        Calculate edit distance between predicted and ground truth text.
        
        Args:
            predicted: Predicted text
            groundtruth: Ground truth text
            
        Returns:
            MetricResult with edit distance score
        """
        if not isinstance(predicted, str) or not isinstance(groundtruth, str):
            return MetricResult.create_error_result(
                self.name, "Both inputs must be strings"
            )
        
        # Calculate edit distance using difflib
        distance = self._levenshtein_distance(predicted, groundtruth)
        
        # Normalize by the length of the longer string
        if self.normalize:
            max_len = max(len(predicted), len(groundtruth))
            if max_len == 0:
                score = 1.0  # Both strings are empty
            else:
                score = 1.0 - (distance / max_len)
        else:
            score = distance
        
        details = {
            "distance": distance,
            "predicted_length": len(predicted),
            "groundtruth_length": len(groundtruth),
            "normalized": self.normalize,
        }
        
        return MetricResult(
            metric_name=self.name,
            score=score,
            details=details
        )
    
    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        """Calculate Levenshtein distance between two strings."""
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = list(range(len(s2) + 1))
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]


class BLEUMetric(BaseMetric):
    """BLEU score metric for text similarity."""
    
    version = "1.0.0"
    description = "BLEU score for text similarity evaluation"
    
    def _setup(self) -> None:
        """Setup the BLEU metric."""
        try:
            from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
            self._sentence_bleu = sentence_bleu
            self._smoothing = SmoothingFunction()
        except ImportError:
            raise RuntimeError("NLTK is required for BLEU metric")
        
        self.max_n = self.config.get('max_n', 4)
        self.smoothing_method = self.config.get('smoothing_method', 'method1')
    
    def _calculate_score(self, predicted: str, groundtruth: str, **kwargs) -> MetricResult:
        """
        Calculate BLEU score between predicted and ground truth text.
        
        Args:
            predicted: Predicted text
            groundtruth: Ground truth text
            
        Returns:
            MetricResult with BLEU score
        """
        if not isinstance(predicted, str) or not isinstance(groundtruth, str):
            return MetricResult.create_error_result(
                self.name, "Both inputs must be strings"
            )
        
        # Tokenize texts (simple whitespace tokenization)
        predicted_tokens = predicted.split()
        groundtruth_tokens = groundtruth.split()
        
        if not predicted_tokens and not groundtruth_tokens:
            score = 1.0  # Both are empty
        elif not predicted_tokens or not groundtruth_tokens:
            score = 0.0  # One is empty
        else:
            # Calculate BLEU score
            smoothing_func = getattr(self._smoothing, self.smoothing_method)
            score = self._sentence_bleu(
                [groundtruth_tokens], 
                predicted_tokens,
                smoothing_function=smoothing_func
            )
        
        details = {
            "predicted_tokens": len(predicted_tokens),
            "groundtruth_tokens": len(groundtruth_tokens),
            "max_n": self.max_n,
            "smoothing_method": self.smoothing_method,
        }
        
        return MetricResult(
            metric_name=self.name,
            score=score,
            details=details
        )


class ROUGEMetric(BaseMetric):
    """ROUGE score metric for text similarity."""
    
    version = "1.0.0"
    description = "ROUGE score for text similarity evaluation"
    
    def _setup(self) -> None:
        """Setup the ROUGE metric."""
        try:
            import rouge
            self._rouge = rouge.Rouge()
        except ImportError:
            raise RuntimeError("rouge-score package is required for ROUGE metric")
        
        self.rouge_types = self.config.get('rouge_types', ['rouge-1', 'rouge-2', 'rouge-l'])
        self.use_stemmer = self.config.get('use_stemmer', True)
    
    def _calculate_score(self, predicted: str, groundtruth: str, **kwargs) -> MetricResult:
        """
        Calculate ROUGE score between predicted and ground truth text.
        
        Args:
            predicted: Predicted text
            groundtruth: Ground truth text
            
        Returns:
            MetricResult with ROUGE scores
        """
        if not isinstance(predicted, str) or not isinstance(groundtruth, str):
            return MetricResult.create_error_result(
                self.name, "Both inputs must be strings"
            )
        
        if not predicted.strip() and not groundtruth.strip():
            # Both are empty
            score = 1.0
            details = {"rouge-1": {"f": 1.0}, "rouge-2": {"f": 1.0}, "rouge-l": {"f": 1.0}}
        elif not predicted.strip() or not groundtruth.strip():
            # One is empty
            score = 0.0
            details = {"rouge-1": {"f": 0.0}, "rouge-2": {"f": 0.0}, "rouge-l": {"f": 0.0}}
        else:
            # Calculate ROUGE scores
            try:
                scores = self._rouge.get_scores(predicted, groundtruth)[0]
                # Use ROUGE-L F1 as the main score
                score = scores['rouge-l']['f']
                details = scores
            except Exception as e:
                return MetricResult.create_error_result(
                    self.name, f"ROUGE calculation failed: {str(e)}"
                )
        
        return MetricResult(
            metric_name=self.name,
            score=score,
            details=details
        ) 