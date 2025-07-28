"""
TEDS (Tree-Edit Distance based Similarity) metrics for WebMainBench.

Based on the paper:
"Image-based table recognition: data, model, and evaluation" by IBM Research.

The TEDS algorithm represents tables as tree structures and calculates 
similarity using tree edit distance.
"""

from typing import Dict, Any, List, Optional
import re
from lxml import etree, html
from lxml.html import HtmlElement
from bs4 import BeautifulSoup
from .base import BaseMetric, MetricResult


class TEDSMetric(BaseMetric):
    """TEDS (Tree-Edit Distance based Similarity) metric for table evaluation."""
    
    version = "1.0.0"
    description = "Table evaluation using Tree-Edit Distance based Similarity (TEDS)"
    
    def _setup(self) -> None:
        """Setup the TEDS metric."""
        self.structure_only = self.config.get('structure_only', False)
        self.ignore_nodes = self.config.get('ignore_nodes', ['tbody', 'thead', 'tfoot'])
    
    def _calculate_score(self, predicted: Any, groundtruth: Any, **kwargs) -> MetricResult:
        """
        Calculate TEDS score between predicted and ground truth tables.
        
        Args:
            predicted: Predicted table (HTML string, markdown, or structured data)
            groundtruth: Ground truth table
            
        Returns:
            MetricResult with TEDS score
        """
        try:
            # Convert inputs to HTML format
            pred_html = self._normalize_to_html(predicted)
            gt_html = self._normalize_to_html(groundtruth)
            
            # Parse HTML to tree structures
            pred_tree = self._parse_html_table(pred_html)
            gt_tree = self._parse_html_table(gt_html)
            
            if pred_tree is None and gt_tree is None:
                # Both are empty/invalid tables
                return MetricResult(
                    metric_name=self.name,
                    score=1.0,
                    details={"note": "Both tables are empty or invalid"}
                )
            
            if pred_tree is None or gt_tree is None:
                # One is empty/invalid
                return MetricResult(
                    metric_name=self.name,
                    score=0.0,
                    details={"note": "One table is empty or invalid"}
                )
            
            # Calculate tree edit distance
            edit_distance = self._tree_edit_distance(pred_tree, gt_tree)
            
            # Calculate TEDS score
            max_nodes = max(self._count_nodes(pred_tree), self._count_nodes(gt_tree))
            teds_score = 1.0 - (edit_distance / max_nodes) if max_nodes > 0 else 1.0
            
            details = {
                "edit_distance": edit_distance,
                "predicted_nodes": self._count_nodes(pred_tree),
                "groundtruth_nodes": self._count_nodes(gt_tree),
                "max_nodes": max_nodes,
                "structure_only": self.structure_only,
                "algorithm": "TEDS"
            }
            
            return MetricResult(
                metric_name=self.name,
                score=max(0.0, min(1.0, teds_score)),  # Clamp to [0, 1]
                details=details
            )
            
        except Exception as e:
            return MetricResult.create_error_result(
                self.name, f"TEDS calculation failed: {str(e)}"
            )
    
    def _normalize_to_html(self, table_data: Any) -> str:
        """Convert various table formats to HTML."""
        if table_data is None:
            return ""
        
        if isinstance(table_data, str):
            # If it's already HTML
            if '<table' in table_data.lower():
                return table_data
            
            # If it's markdown table
            if '|' in table_data:
                return self._markdown_to_html(table_data)
            
            # Plain text
            return f"<table><tr><td>{table_data}</td></tr></table>"
        
        elif isinstance(table_data, list):
            # Convert list of dicts or list of lists to HTML
            return self._list_to_html(table_data)
        
        else:
            # Convert to string and wrap in table
            return f"<table><tr><td>{str(table_data)}</td></tr></table>"
    
    def _markdown_to_html(self, markdown: str) -> str:
        """Convert markdown table to HTML."""
        lines = [line.strip() for line in markdown.split('\n') if line.strip()]
        table_lines = [line for line in lines if '|' in line]
        
        if not table_lines:
            return ""
        
        html_parts = ["<table>"]
        
        # Skip separator line (usually contains dashes)
        data_lines = [line for line in table_lines if not re.match(r'^[\s\|\-:]+$', line)]
        
        for i, line in enumerate(data_lines):
            cells = [cell.strip() for cell in line.split('|') if cell.strip()]
            if cells:
                tag = "th" if i == 0 else "td"
                html_parts.append(f"<tr>{''.join(f'<{tag}>{cell}</{tag}>' for cell in cells)}</tr>")
        
        html_parts.append("</table>")
        return ''.join(html_parts)
    
    def _list_to_html(self, data: List) -> str:
        """Convert list data to HTML table."""
        if not data:
            return ""
        
        html_parts = ["<table>"]
        
        for item in data:
            if isinstance(item, dict):
                cells = list(item.values())
            elif isinstance(item, list):
                cells = item
            else:
                cells = [str(item)]
            
            html_parts.append(f"<tr>{''.join(f'<td>{cell}</td>' for cell in cells)}</tr>")
        
        html_parts.append("</table>")
        return ''.join(html_parts)
    
    def _parse_html_table(self, html_str: str) -> Optional[Dict]:
        """Parse HTML table into tree structure."""
        if not html_str.strip():
            return None
        
        try:
            # Use BeautifulSoup for more robust HTML parsing
            soup = BeautifulSoup(html_str, 'html.parser')
            table = soup.find('table')
            
            if table is None:
                return None
            
            return self._element_to_tree(table)
        
        except Exception:
            return None
    
    def _element_to_tree(self, element) -> Dict:
        """Convert HTML element to tree structure."""
        tree = {
            'tag': element.name,
            'attrs': dict(element.attrs) if hasattr(element, 'attrs') else {},
            'text': element.get_text(strip=True) if not self.structure_only else "",
            'children': []
        }
        
        # Skip ignored nodes
        if element.name in self.ignore_nodes:
            for child in element.children:
                if hasattr(child, 'name') and child.name:
                    tree['children'].extend(self._element_to_tree(child)['children'])
        else:
            for child in element.children:
                if hasattr(child, 'name') and child.name:
                    tree['children'].append(self._element_to_tree(child))
        
        return tree
    
    def _count_nodes(self, tree: Dict) -> int:
        """Count total nodes in tree."""
        if tree is None:
            return 0
        
        count = 1  # Current node
        for child in tree.get('children', []):
            count += self._count_nodes(child)
        
        return count
    
    def _tree_edit_distance(self, tree1: Dict, tree2: Dict) -> float:
        """
        Calculate tree edit distance using dynamic programming.
        
        This is a simplified version of the tree edit distance algorithm.
        For production use, consider using more sophisticated algorithms.
        """
        if tree1 is None and tree2 is None:
            return 0.0
        if tree1 is None:
            return float(self._count_nodes(tree2))
        if tree2 is None:
            return float(self._count_nodes(tree1))
        
        # Check if nodes are the same
        if self._nodes_equal(tree1, tree2):
            # Nodes are equal, calculate cost for children
            children1 = tree1.get('children', [])
            children2 = tree2.get('children', [])
            
            return self._list_edit_distance(children1, children2)
        else:
            # Nodes are different, calculate minimum cost
            # Option 1: Replace tree1 with tree2
            cost_replace = 1.0 + self._list_edit_distance(
                tree1.get('children', []), 
                tree2.get('children', [])
            )
            
            # Option 2: Delete tree1 and insert tree2
            cost_delete_insert = (
                float(self._count_nodes(tree1)) + 
                float(self._count_nodes(tree2))
            )
            
            return min(cost_replace, cost_delete_insert)
    
    def _list_edit_distance(self, list1: List, list2: List) -> float:
        """Calculate edit distance between two lists of trees."""
        m, n = len(list1), len(list2)
        
        # Initialize DP matrix
        dp = [[0.0] * (n + 1) for _ in range(m + 1)]
        
        # Base cases
        for i in range(1, m + 1):
            dp[i][0] = dp[i-1][0] + self._count_nodes(list1[i-1])
        
        for j in range(1, n + 1):
            dp[0][j] = dp[0][j-1] + self._count_nodes(list2[j-1])
        
        # Fill DP matrix
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                # Cost of substitution
                subst_cost = self._tree_edit_distance(list1[i-1], list2[j-1])
                
                # Cost of deletion
                del_cost = self._count_nodes(list1[i-1])
                
                # Cost of insertion
                ins_cost = self._count_nodes(list2[j-1])
                
                dp[i][j] = min(
                    dp[i-1][j-1] + subst_cost,  # Substitute
                    dp[i-1][j] + del_cost,      # Delete
                    dp[i][j-1] + ins_cost       # Insert
                )
        
        return dp[m][n]
    
    def _nodes_equal(self, node1: Dict, node2: Dict) -> bool:
        """Check if two tree nodes are equal."""
        if node1['tag'] != node2['tag']:
            return False
        
        # Compare important attributes
        attrs1 = node1.get('attrs', {})
        attrs2 = node2.get('attrs', {})
        
        # Check colspan and rowspan
        important_attrs = ['colspan', 'rowspan']
        for attr in important_attrs:
            if attrs1.get(attr) != attrs2.get(attr):
                return False
        
        # Compare text content if not structure_only
        if not self.structure_only:
            if node1.get('text', '') != node2.get('text', ''):
                return False
        
        return True


class StructureTEDSMetric(TEDSMetric):
    """Structure-only TEDS metric (S-TEDS)."""
    
    def _setup(self) -> None:
        """Setup S-TEDS metric."""
        super()._setup()
        self.structure_only = True
        self.name = "s_teds"
        self.description = "Structure-only Tree-Edit Distance based Similarity (S-TEDS)" 