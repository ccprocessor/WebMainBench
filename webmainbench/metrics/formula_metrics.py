"""
Formula extraction metrics for WebMainBench.
"""

from typing import Dict, Any, List
from .base import BaseMetric, MetricResult


class FormulaExtractionMetric(BaseMetric):
    """Metric for evaluating mathematical formula extraction."""
    
    version = "1.0.0"
    description = "Mathematical formula extraction evaluation"
    
    def _setup(self) -> None:
        """Setup the formula extraction metric."""
        self.syntax_weight = self.config.get('syntax_weight', 0.6)
        self.semantic_weight = self.config.get('semantic_weight', 0.4)
    
    def _calculate_score(self, predicted: Any, groundtruth: Any, **kwargs) -> MetricResult:
        """
        Calculate formula extraction score.
        
        Args:
            predicted: Predicted formula (LaTeX, MathML, or text)
            groundtruth: Ground truth formula
            
        Returns:
            MetricResult with formula extraction score
        """
        try:
            # Extract formulas from the content
            pred_formulas = self._extract_formulas(predicted)
            gt_formulas = self._extract_formulas(groundtruth)
            
            # Calculate syntax similarity
            syntax_score = self._calculate_syntax_similarity(pred_formulas, gt_formulas)
            
            # Calculate semantic similarity (placeholder)
            semantic_score = self._calculate_semantic_similarity(pred_formulas, gt_formulas)
            
            # Combine scores
            final_score = (
                syntax_score * self.syntax_weight + 
                semantic_score * self.semantic_weight
            )
            
            details = {
                "syntax_score": syntax_score,
                "semantic_score": semantic_score,
                "predicted_formulas": pred_formulas,
                "groundtruth_formulas": gt_formulas,
                "num_predicted": len(pred_formulas),
                "num_groundtruth": len(gt_formulas),
            }
            
            return MetricResult(
                metric_name=self.name,
                score=final_score,
                details=details
            )
            
        except Exception as e:
            return MetricResult.create_error_result(
                self.name, f"Formula evaluation failed: {str(e)}"
            )
    
    def _extract_formulas(self, content: Any) -> List[str]:
        """Extract mathematical formulas from content."""
        import re
        
        if not isinstance(content, str):
            content = str(content)
        
        formulas = []
        
        # Extract LaTeX-style formulas
        latex_patterns = [
            r'\$\$([^$]+)\$\$',  # Display math
            r'\$([^$]+)\$',      # Inline math
            r'\\begin\{equation\}(.*?)\\end\{equation\}',  # Equation environment
            r'\\begin\{align\}(.*?)\\end\{align\}',        # Align environment
        ]
        
        for pattern in latex_patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            formulas.extend(matches)
        
        # Extract MathML formulas
        mathml_pattern = r'<math[^>]*>(.*?)</math>'
        mathml_matches = re.findall(mathml_pattern, content, re.DOTALL | re.IGNORECASE)
        formulas.extend(mathml_matches)
        
        return formulas
    
    def _calculate_syntax_similarity(self, pred_formulas: List[str], gt_formulas: List[str]) -> float:
        """Calculate syntax similarity between formula lists."""
        if not pred_formulas and not gt_formulas:
            return 1.0
        
        if not pred_formulas or not gt_formulas:
            return 0.0
        
        # Simple approach: calculate pairwise similarities and find best matches
        from difflib import SequenceMatcher
        
        total_score = 0.0
        max_count = max(len(pred_formulas), len(gt_formulas))
        
        # Find best matches
        used_gt = set()
        for pred_formula in pred_formulas:
            best_score = 0.0
            best_idx = -1
            
            for i, gt_formula in enumerate(gt_formulas):
                if i in used_gt:
                    continue
                
                score = SequenceMatcher(None, pred_formula, gt_formula).ratio()
                if score > best_score:
                    best_score = score
                    best_idx = i
            
            if best_idx >= 0:
                used_gt.add(best_idx)
                total_score += best_score
        
        return total_score / max_count
    
    def _calculate_semantic_similarity(self, pred_formulas: List[str], gt_formulas: List[str]) -> float:
        """Calculate semantic similarity between formulas."""
        # This is a placeholder for semantic similarity
        # In practice, you might use symbolic math libraries to parse and compare
        # the mathematical meaning of formulas
        
        if not pred_formulas and not gt_formulas:
            return 1.0
        
        if not pred_formulas or not gt_formulas:
            return 0.0
        
        # For now, just return syntax similarity as a proxy
        return self._calculate_syntax_similarity(pred_formulas, gt_formulas) 