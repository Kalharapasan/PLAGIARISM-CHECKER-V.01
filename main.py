#!/usr/bin/env python3
import os
import sys
import re
from pathlib import Path
from typing import List, Dict, Set
from collections import Counter
import difflib
import math

class SimplePlagiarismChecker:
    def __init__(self):
        self.min_match_length = 5  
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what',
            'which', 'who', 'when', 'where', 'why', 'how', 'all', 'each', 'every',
            'some', 'any', 'no', 'not', 'only', 'own', 'same', 'so', 'than', 'too',
            'very', 's', 't', 'just', 'now'
        }
    
    def extract_text_from_txt(self, filepath: str) -> str:
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            raise Exception(f"Error reading TXT file: {e}")
    
    def tokenize(self, text: str) -> List[str]:
        words = re.findall(r'\b[a-z0-9]+\b', text.lower())
        return words
    
    def preprocess_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def get_sentences(self, text: str) -> List[str]:
        sentences = re.split(r'[.!?]+\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def get_ngrams(self, words: List[str], n: int = 3) -> List[str]:
        filtered_words = [w for w in words if w not in self.stop_words]
        ngrams = []
        for i in range(len(filtered_words) - n + 1):
            ngrams.append(' '.join(filtered_words[i:i+n]))
        return ngrams
    
    def calculate_jaccard_similarity(self, text1: str, text2: str) -> float:
        words1 = set(self.tokenize(text1))
        words2 = set(self.tokenize(text2))
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return (intersection / union) * 100 if union > 0 else 0.0
    
    def calculate_cosine_similarity(self, text1: str, text2: str) -> float:
        words1 = self.tokenize(text1)
        words2 = self.tokenize(text2)
        freq1 = Counter(words1)
        freq2 = Counter(words2)
        all_words = set(freq1.keys()).union(set(freq2.keys()))
        vec1 = [freq1.get(word, 0) for word in all_words]
        vec2 = [freq2.get(word, 0) for word in all_words]
        dot_product = sum(v1 * v2 for v1, v2 in zip(vec1, vec2))



if __name__ == "__main__":
    main()
    