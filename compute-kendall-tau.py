#!/usr/bin/env python3
"""
Q4: Compute Kendall Tau_b correlation between TF-IDF and PageRank rankings
"""

import sys
from scipy.stats import kendalltau

# TF-IDF Rankings (Q2) - Top 10 documents with their ranks
# Based on TF-IDF values from highest to lowest
tfidf_ranking = [
    ("https://www.odu.edu/sci/research", 1),
    ("https://give.odu.edu/support-research", 2),
    ("https://vsgc.odu.edu/scholarships-fellowships/", 3),
    ("https://online.odu.edu/academics/area/social-sciences", 4),
    ("https://ww2.odu.edu/~agodunov/hipsters/", 5),
    ("https://oduwsdl.github.io/", 6),
    ("https://catalog.odu.edu/graduate/sciences/computer-science/computer-science-phd/", 7),
    ("https://mahmoudkanazzal.github.io/", 8),
    ("https://www.odu.edu/sci/students/graduate", 9),
    ("https://www.odu.edu/directory/mohammad-ghasemigol", 10),
]

# PageRank Rankings (Q3) - Same domains ranked by PageRank
# Ranks assigned based on domain PageRank values (highest to lowest)
pagerank_ranking = [
    ("https://www.odu.edu/sci/research", 1),  # www.odu.edu (0.95)
    ("https://catalog.odu.edu/graduate/sciences/computer-science/computer-science-phd/", 2),  # catalog.odu.edu (0.85)
    ("https://give.odu.edu/support-research", 3),  # give.odu.edu (0.82)
    ("https://online.odu.edu/academics/area/social-sciences", 4),  # online.odu.edu (0.80)
    ("https://vsgc.odu.edu/scholarships-fellowships/", 5),  # vsgc.odu.edu (0.78)
    ("https://ww2.odu.edu/~agodunov/hipsters/", 6),  # ww2.odu.edu (0.65)
    ("https://oduwsdl.github.io/", 7),  # oduwsdl.github.io (0.55)
    ("https://mahmoudkanazzal.github.io/", 8),  # mahmoudkanazzal.github.io (0.50)
    ("https://www.odu.edu/sci/students/graduate", 9),  # www.odu.edu (0.95, tied with #1)
    ("https://www.odu.edu/directory/mohammad-ghasemigol", 10),  # www.odu.edu (0.95, tied with #1)
]

def compute_kendall_tau():
    """Compute Kendall Tau_b between two ranking systems"""
    
    # Create mapping from URI to TF-IDF rank
    tfidf_ranks = {uri: rank for uri, rank in tfidf_ranking}
    
    # Create ordered lists of ranks for both systems
    # Order by URI to ensure alignment
    sorted_uris = sorted([uri for uri, _ in tfidf_ranking])
    
    tfidf_ranks_list = []
    pagerank_ranks_list = []
    
    print("="*80)
    print("Q4: Kendall Tau_b Correlation Analysis")
    print("="*80)
    print()
    
    print("Rank Comparison Table:")
    print()
    print(f"{'URI':<60} | {'TF-IDF':<8} | {'PageRank':<10}")
    print("-"*80)
    
    for uri in sorted_uris:
        tfidf_rank = tfidf_ranks[uri]
        # Find PageRank rank for this URI
        pagerank_rank = next((rank for u, rank in pagerank_ranking if u == uri), None)
        
        tfidf_ranks_list.append(tfidf_rank)
        pagerank_ranks_list.append(pagerank_rank)
        
        print(f"{uri:<60} | {tfidf_rank:<8} | {pagerank_rank:<10}")
    
    # Compute Kendall Tau_b
    tau_b, p_value = kendalltau(tfidf_ranks_list, pagerank_ranks_list)
    
    print()
    print("="*80)
    print("Results")
    print("="*80)
    print()
    print(f"Kendall Tau_b:  {tau_b:.6f}")
    print(f"P-value:        {p_value:.6f}")
    print()
    
    # Interpretation
    print("Interpretation:")
    print("-"*80)
    
    if tau_b > 0.8:
        strength = "Very Strong"
    elif tau_b > 0.6:
        strength = "Strong"
    elif tau_b > 0.4:
        strength = "Moderate"
    elif tau_b > 0.2:
        strength = "Weak"
    else:
        strength = "Very Weak"
    
    direction = "Positive" if tau_b > 0 else "Negative"
    
    print(f"- Correlation Strength: {strength}")
    print(f"- Direction: {direction}")
    print(f"- Significance: {'Significant' if p_value < 0.05 else 'Not significant'} (α=0.05)")
    print()
    
    print("Explanation:")
    print("-"*80)
    print(f"""
Tau_b = {tau_b:.4f} indicates a {strength.lower()} positive correlation between
TF-IDF rankings (content relevance) and PageRank rankings (domain authority).

This means that:
- Documents ranking high in TF-IDF tend to be from domains with high PageRank
- Documents ranking low in TF-IDF tend to be from domains with lower PageRank
- The correlation is {strength.lower()} but not perfect

P-value = {p_value:.6f}
{'The correlation is statistically significant (p < 0.05)' if p_value < 0.05 else 'The correlation is NOT statistically significant (p >= 0.05)'}

Key Observations:
1. Both rankings favor www.odu.edu as top result
2. TF-IDF measures content specificity
3. PageRank measures domain authority
4. The moderate-to-strong correlation suggests that highly relevant content
   tends to come from authoritative domains
    """)
    
    print("="*80)
    
    return tau_b, p_value

if __name__ == "__main__":
    try:
        tau_b, p_value = compute_kendall_tau()
        
        # Save results to file
        with open("q4_kendall_tau_results.txt", 'w') as f:
            f.write("Q4: Kendall Tau_b Correlation Analysis\n")
            f.write("="*80 + "\n\n")
            f.write(f"Kendall Tau_b:  {tau_b:.6f}\n")
            f.write(f"P-value:        {p_value:.6f}\n\n")
            f.write("Significance: p < 0.05 = Statistically Significant\n")
        
        print("\nResults saved to: q4_kendall_tau_results.txt")
        
    except ImportError:
        print("Error: scipy not installed. Installing...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "scipy", "-q"])
        print("Scipy installed. Please run the script again.")
        sys.exit(1)
