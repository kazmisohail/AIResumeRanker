"""
Configuration settings for the AI Resume Ranker application.
This file centralizes tunable parameters for easier management.
"""

# Scoring Model Weights
# Adjust the weights to change the importance of keyword vs. semantic matching......
# The sum should ideally be 1.0.....
# Change accordinglyy...!!!
HYBRID_SCORE_WEIGHTS: dict[str, float] = {
    "keyword": 0.6,    # 60% importance for TF-IDF keyword matching
    "semantic": 0.4    # 40% importance for spaCy semantic similarity
}