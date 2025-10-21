def gini_index(utilities: list[float]) -> float:
    """
    Calculate Gini index for fairness measurement
    """
    n = len(utilities)
    if n == 0:
        return 0.0
    
    mean_u = sum(utilities) / n
    if mean_u == 0:
        return 0.0
        
    num = sum(abs(ui - uj) for ui in utilities for uj in utilities)
    return num / (2 * n**2 * mean_u)