import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.algorithms.rga_enhanced import rga_enhanced_algorithm
from app.algorithms.rga import rga_algorithm
from app.algorithms.rga_plus import rga_plus_algorithm
from app.utils.utility_function import gini_index, social_welfare

def test_rga_enhanced():
    """
    Test the enhanced RGA algorithm and compare it with the original algorithms
    """
    print("Testing Enhanced RGA Algorithm...")
    
    # Run the enhanced RGA algorithm
    try:
        enhanced_result = rga_enhanced_algorithm()
        print(f"Enhanced RGA completed successfully!")
        print(f"Algorithm: {enhanced_result.algorithm}")
        print(f"Number of assignments: {len(enhanced_result.assignments)}")
        print(f"Gini Index: {enhanced_result.metrics['gini']:.4f}")
        print(f"Social Welfare: {enhanced_result.metrics['social_welfare']:.4f}")
        
        # Compare with original RGA
        original_result = rga_algorithm()
        print(f"\nOriginal RGA:")
        print(f"Gini Index: {original_result.metrics['gini']:.4f}")
        print(f"Social Welfare: {original_result.metrics['social_welfare']:.4f}")
        
        # Compare with RGA++
        rga_plus_result = rga_plus_algorithm()
        print(f"\nRGA++:")
        print(f"Gini Index: {rga_plus_result.metrics['gini']:.4f}")
        print(f"Social Welfare: {rga_plus_result.metrics['social_welfare']:.4f}")
        
        # Determine which algorithm performed best in terms of fairness (lower Gini)
        algorithms = [
            ("RGA-Enhanced", enhanced_result.metrics['gini'], enhanced_result.metrics['social_welfare']),
            ("RGA", original_result.metrics['gini'], original_result.metrics['social_welfare']),
            ("RGA++", rga_plus_result.metrics['gini'], rga_plus_result.metrics['social_welfare'])
        ]
        
        # Sort by Gini index (lower is better for fairness)
        algorithms.sort(key=lambda x: x[1])
        
        print(f"\n--- Fairness Comparison (Lower Gini = More Fair) ---")
        for i, (name, gini, sw) in enumerate(algorithms):
            print(f"{i+1}. {name}: Gini = {gini:.4f}, Social Welfare = {sw:.4f}")
            
        best_algorithm = algorithms[0]
        print(f"\nBest fairness performance: {best_algorithm[0]} with Gini index {best_algorithm[1]:.4f}")
        
    except Exception as e:
        print(f"Error running enhanced RGA algorithm: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_rga_enhanced()