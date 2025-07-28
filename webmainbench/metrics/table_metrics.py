"""
Table extraction metrics for WebMainBench.
"""

from typing import Dict, Any, List
from .base import BaseMetric, MetricResult
from .teds_metrics import TEDSMetric, StructureTEDSMetric


class TableExtractionMetric(BaseMetric):
    """Metric for evaluating table extraction quality."""
    
    version = "1.0.0"
    description = "Table structure and content extraction evaluation"
    
    def _setup(self) -> None:
        """Setup the table extraction metric."""
        self.structure_weight = self.config.get('structure_weight', 0.5)
        self.content_weight = self.config.get('content_weight', 0.5)
        self.use_teds = self.config.get('use_teds', False)
        
        # Initialize TEDS metric if requested
        if self.use_teds:
            self.teds_metric = TEDSMetric("teds", self.config)
    
    def _calculate_score(self, predicted: Any, groundtruth: Any, **kwargs) -> MetricResult:
        """
        Calculate table extraction score.
        
        Args:
            predicted: Predicted table data (could be HTML, markdown, or structured data)
            groundtruth: Ground truth table data
            
        Returns:
            MetricResult with table extraction score
        """
        try:
            # Use TEDS algorithm if enabled
            if self.use_teds:
                return self.teds_metric.calculate(predicted, groundtruth, **kwargs)
            
            # Use original simple algorithm
            # Extract table structures
            pred_structure = self._extract_table_structure(predicted)
            gt_structure = self._extract_table_structure(groundtruth)
            
            # Calculate structure similarity
            structure_score = self._calculate_structure_similarity(pred_structure, gt_structure)
            
            # Calculate content similarity
            content_score = self._calculate_content_similarity(predicted, groundtruth)
            
            # Combine scores
            final_score = (
                structure_score * self.structure_weight + 
                content_score * self.content_weight
            )
            
            details = {
                "structure_score": structure_score,
                "content_score": content_score,
                "structure_weight": self.structure_weight,
                "content_weight": self.content_weight,
                "predicted_structure": pred_structure,
                "groundtruth_structure": gt_structure,
                "algorithm": "simple"
            }
            
            return MetricResult(
                metric_name=self.name,
                score=final_score,
                details=details
            )
            
        except Exception as e:
            return MetricResult.create_error_result(
                self.name, f"Table evaluation failed: {str(e)}"
            )
    
    def _extract_table_structure(self, table_data: Any) -> Dict[str, Any]:
        """Extract table structure information."""
        # This is a placeholder implementation
        # In practice, you would parse HTML tables, markdown tables, etc.
        if isinstance(table_data, str):
            # Count rows and columns from string representation
            lines = table_data.split('\n')
            table_lines = [line for line in lines if '|' in line]
            
            if not table_lines:
                return {"rows": 0, "cols": 0}
            
            # Estimate columns from the first line
            cols = len(table_lines[0].split('|')) - 1 if table_lines else 0
            rows = len(table_lines)
            
            return {"rows": rows, "cols": cols}
        
        elif isinstance(table_data, list):
            # Assuming list of dictionaries or list of lists
            if not table_data:
                return {"rows": 0, "cols": 0}
            
            rows = len(table_data)
            if isinstance(table_data[0], dict):
                cols = len(table_data[0])
            elif isinstance(table_data[0], list):
                cols = len(table_data[0])
            else:
                cols = 1
            
            return {"rows": rows, "cols": cols}
        
        else:
            return {"rows": 0, "cols": 0}
    
    def _calculate_structure_similarity(self, pred_structure: Dict, gt_structure: Dict) -> float:
        """Calculate similarity between table structures."""
        if pred_structure["rows"] == 0 and gt_structure["rows"] == 0:
            return 1.0
        
        if pred_structure["rows"] == 0 or gt_structure["rows"] == 0:
            return 0.0
        
        # Simple structure similarity based on dimensions
        row_similarity = min(pred_structure["rows"], gt_structure["rows"]) / max(pred_structure["rows"], gt_structure["rows"])
        col_similarity = min(pred_structure["cols"], gt_structure["cols"]) / max(pred_structure["cols"], gt_structure["cols"])
        
        return (row_similarity + col_similarity) / 2
    
    def _calculate_content_similarity(self, predicted: Any, groundtruth: Any) -> float:
        """Calculate similarity between table contents."""
        # Convert both to strings and calculate text similarity
        pred_text = str(predicted)
        gt_text = str(groundtruth)
        
        # Simple character-level similarity
        if not pred_text and not gt_text:
            return 1.0
        
        if not pred_text or not gt_text:
            return 0.0
        
        # Use a simple similarity measure (could be improved)
        from difflib import SequenceMatcher
        return SequenceMatcher(None, pred_text, gt_text).ratio() 