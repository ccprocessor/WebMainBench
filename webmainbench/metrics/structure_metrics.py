"""
Structure-based metrics for WebMainBench.
"""

from typing import Dict, Any, List
from .base import BaseMetric, MetricResult


class StructureMetric(BaseMetric):
    """Metric for evaluating content structure preservation."""
    
    version = "1.0.0"
    description = "Content structure and hierarchy evaluation"
    
    def _setup(self) -> None:
        """Setup the structure metric."""
        self.hierarchy_weight = self.config.get('hierarchy_weight', 0.4)
        self.order_weight = self.config.get('order_weight', 0.3)
        self.completeness_weight = self.config.get('completeness_weight', 0.3)
    
    def _calculate_score(self, predicted: Any, groundtruth: Any, **kwargs) -> MetricResult:
        """
        Calculate structure preservation score.
        
        Args:
            predicted: Predicted content_list or structured content
            groundtruth: Ground truth content_list or structured content
            
        Returns:
            MetricResult with structure score
        """
        try:
            # Convert inputs to content_list format
            pred_structure = self._extract_structure(predicted)
            gt_structure = self._extract_structure(groundtruth)
            
            # Calculate hierarchy similarity
            hierarchy_score = self._calculate_hierarchy_similarity(pred_structure, gt_structure)
            
            # Calculate order preservation
            order_score = self._calculate_order_similarity(pred_structure, gt_structure)
            
            # Calculate completeness
            completeness_score = self._calculate_completeness(pred_structure, gt_structure)
            
            # Combine scores
            final_score = (
                hierarchy_score * self.hierarchy_weight +
                order_score * self.order_weight +
                completeness_score * self.completeness_weight
            )
            
            details = {
                "hierarchy_score": hierarchy_score,
                "order_score": order_score,
                "completeness_score": completeness_score,
                "predicted_blocks": len(pred_structure),
                "groundtruth_blocks": len(gt_structure),
            }
            
            return MetricResult(
                metric_name=self.name,
                score=final_score,
                details=details
            )
            
        except Exception as e:
            return MetricResult.create_error_result(
                self.name, f"Structure evaluation failed: {str(e)}"
            )
    
    def _extract_structure(self, content: Any) -> List[Dict[str, Any]]:
        """Extract structure information from content."""
        if isinstance(content, list):
            # Assume it's already a content_list
            return content
        
        elif isinstance(content, str):
            # Try to infer structure from markdown-like text
            lines = content.split('\n')
            structure = []
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Detect headers
                if line.startswith('#'):
                    level = len(line) - len(line.lstrip('#'))
                    text = line.lstrip('#').strip()
                    structure.append({
                        "type": "heading",
                        "content": text,
                        "level": level
                    })
                # Detect lists
                elif line.startswith(('- ', '* ', '+ ')) or line.lstrip().startswith(('1. ', '2. ')):
                    structure.append({
                        "type": "list_item",
                        "content": line.lstrip('- * + ').lstrip('0123456789. ')
                    })
                # Regular paragraphs
                else:
                    structure.append({
                        "type": "paragraph",
                        "content": line
                    })
            
            return structure
        
        else:
            return []
    
    def _calculate_hierarchy_similarity(self, pred_structure: List[Dict], gt_structure: List[Dict]) -> float:
        """Calculate similarity in hierarchical structure."""
        if not pred_structure and not gt_structure:
            return 1.0
        
        if not pred_structure or not gt_structure:
            return 0.0
        
        # Extract hierarchy patterns
        pred_hierarchy = self._extract_hierarchy_pattern(pred_structure)
        gt_hierarchy = self._extract_hierarchy_pattern(gt_structure)
        
        # Calculate similarity using sequence matching
        from difflib import SequenceMatcher
        return SequenceMatcher(None, pred_hierarchy, gt_hierarchy).ratio()
    
    def _extract_hierarchy_pattern(self, structure: List[Dict]) -> str:
        """Extract a pattern representing the hierarchical structure."""
        pattern = []
        for item in structure:
            item_type = item.get('type', 'text')
            if item_type == 'heading':
                level = item.get('level', 1)
                pattern.append(f'H{level}')
            elif item_type == 'list_item':
                pattern.append('L')
            elif item_type == 'table':
                pattern.append('T')
            else:
                pattern.append('P')  # Paragraph or other
        
        return ''.join(pattern)
    
    def _calculate_order_similarity(self, pred_structure: List[Dict], gt_structure: List[Dict]) -> float:
        """Calculate similarity in content ordering."""
        if not pred_structure and not gt_structure:
            return 1.0
        
        if not pred_structure or not gt_structure:
            return 0.0
        
        # Extract content for comparison
        pred_contents = [item.get('content', '') for item in pred_structure]
        gt_contents = [item.get('content', '') for item in gt_structure]
        
        # Calculate longest common subsequence ratio
        lcs_length = self._lcs_length(pred_contents, gt_contents)
        max_length = max(len(pred_contents), len(gt_contents))
        
        return lcs_length / max_length if max_length > 0 else 1.0
    
    def _lcs_length(self, seq1: List[str], seq2: List[str]) -> int:
        """Calculate longest common subsequence length."""
        if not seq1 or not seq2:
            return 0
        
        m, n = len(seq1), len(seq2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if seq1[i-1] == seq2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
        return dp[m][n]
    
    def _calculate_completeness(self, pred_structure: List[Dict], gt_structure: List[Dict]) -> float:
        """Calculate how complete the extracted structure is."""
        if not gt_structure:
            return 1.0  # No ground truth to compare against
        
        if not pred_structure:
            return 0.0  # Nothing extracted
        
        # Simple ratio of extracted blocks to ground truth blocks
        return min(len(pred_structure) / len(gt_structure), 1.0) 