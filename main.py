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
    



if __name__ == "__main__":
    main()
    