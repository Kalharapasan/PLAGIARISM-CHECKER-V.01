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
        magnitude1 = math.sqrt(sum(v ** 2 for v in vec1))
        magnitude2 = math.sqrt(sum(v ** 2 for v in vec2))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return (dot_product / (magnitude1 * magnitude2)) * 100
    
    def find_common_sequences(self, text1: str, text2: str) -> List[Dict]:
        words1 = self.tokenize(text1)
        words2 = self.tokenize(text2)
        
        matcher = difflib.SequenceMatcher(None, words1, words2)
        matches = []
        
        for match in matcher.get_matching_blocks():
            if match.size >= self.min_match_length:
                matched_text = ' '.join(words1[match.a:match.a + match.size])
                start = max(0, match.a - 20)
                end = min(len(words1), match.a + match.size + 20)
                context = ' '.join(words1[start:end])
                
                matches.append({
                    'text': matched_text,
                    'context': context,
                    'length': match.size,
                    'position': match.a
                })
        
        return matches
    
    def check_against_database(self, text: str, database_texts: List[Dict]) -> Dict:
        results = {
            'overall_similarity': 0,
            'total_words': len(self.tokenize(text)),
            'matches': []
        }
        
        text_clean = self.preprocess_text(text)
        
        for doc in database_texts:
            doc_text = doc.get('text', '')
            doc_clean = self.preprocess_text(doc_text)
            jaccard = self.calculate_jaccard_similarity(text_clean, doc_clean)
            cosine = self.calculate_cosine_similarity(text_clean, doc_clean)
            similarity = (jaccard + cosine) / 2
            if similarity > 5: 
                common_sequences = self.find_common_sequences(text_clean, doc_clean)
                match_info = {
                    'source': doc.get('source', 'Unknown'),
                    'url': doc.get('url', ''),
                    'similarity': round(similarity, 2),
                    'matched_sequences': common_sequences[:5]  
                }
                results['matches'].append(match_info)
        if results['matches']:
            total_weight = sum(m['similarity'] for m in results['matches'])
            weighted_sum = sum(m['similarity'] ** 2 for m in results['matches'])
            results['overall_similarity'] = round(
                weighted_sum / total_weight if total_weight > 0 else 0, 2
            )
        results['matches'].sort(key=lambda x: x['similarity'], reverse=True)
        
        return results
    
    def generate_report(self, results: Dict, output_file: str = None) -> str:
        report = []
        report.append("=" * 70)
        report.append("PLAGIARISM DETECTION REPORT")
        report.append("=" * 70)
        report.append("")
        report.append("SUMMARY")
        report.append("-" * 70)
        report.append(f"Overall Similarity Score: {results['overall_similarity']}%")
        report.append(f"Total Words Analyzed: {results['total_words']}")
        report.append(f"Number of Sources Matched: {len(results['matches'])}")
        
        matched_words = sum(
            sum(seq['length'] for seq in match['matched_sequences'])
            for match in results['matches']
        )
        report.append(f"Total Matched Words: {matched_words}")
        unique_percent = max(0, 100 - results['overall_similarity'])
        report.append(f"Unique Content: {unique_percent:.2f}%")
        report.append("")
        report.append("INTERPRETATION")
        report.append("-" * 70)
        score = results['overall_similarity']
        if score < 15:
            report.append("✓ LOW SIMILARITY - Acceptable level for academic work")
            report.append("  The document shows minimal overlap with existing sources.")
            report.append("  This is generally acceptable for submission.")
        elif score < 30:
            report.append("⚠ MODERATE SIMILARITY - Review recommended")
            report.append("  The document shows moderate overlap with existing sources.")
            report.append("  Check matches to ensure proper citation and paraphrasing.")
        else:
            report.append("✗ HIGH SIMILARITY - Significant concern")
            report.append("  The document shows substantial overlap with existing sources.")
            report.append("  Significant revision may be needed for academic integrity.")
        report.append("")
        if results['matches']:
            report.append("DETAILED MATCH ANALYSIS")
            report.append("-" * 70)
            
            for idx, match in enumerate(results['matches'], 1):
                report.append(f"\nMatch #{idx}")
                report.append(f"Source: {match['source']}")
                if match['url']:
                    report.append(f"URL: {match['url']}")
                report.append(f"Similarity: {match['similarity']}%")
                report.append(f"Number of matched sequences: {len(match['matched_sequences'])}")
                
                if match['matched_sequences']:
                    report.append("\nTop Matched Sequences:")
                    for seq_idx, seq in enumerate(match['matched_sequences'][:3], 1):
                        truncated = seq['text'][:80] + '...' if len(seq['text']) > 80 else seq['text']
                        report.append(f"\n  Sequence {seq_idx} ({seq['length']} words):")
                        report.append(f"  \"{truncated}\"")
                
                report.append("\n" + "-" * 70)
        else:
            report.append("DETAILED MATCH ANALYSIS")
            report.append("-" * 70)
            report.append("\nNo significant matches found.")
            report.append("The document appears to be largely original content.")
        
        report.append("")
        report.append("RECOMMENDATIONS")
        report.append("-" * 70)
        if results['overall_similarity'] < 15:
            report.append("• Document is acceptable for submission")
            report.append("• Continue maintaining good citation practices")
        elif results['overall_similarity'] < 30:
            report.append("• Review highlighted matches for proper citation")
            report.append("• Consider paraphrasing matched sections")
            report.append("• Ensure all quotes are properly attributed")
        else:
            report.append("• Significant revision recommended before submission")
            report.append("• Review all matched sections carefully")
            report.append("• Ensure proper citation for all borrowed content")
            report.append("• Consider rewriting highly similar sections in your own words")
        
        report.append("")
        report.append("=" * 70)
        report.append("Note: This is an automated analysis. Human review is recommended.")
        report.append("Always verify results and maintain academic integrity standards.")
        report.append("=" * 70)
        
        report_text = '\n'.join(report)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report_text)
            print(f"\nReport saved to: {output_file}")
        
        return report_text
    

def create_sample_database() -> List[Dict]:
    return [
        {
            'source': 'Wikipedia - Academic Integrity',
            'url': 'https://en.wikipedia.org/wiki/Academic_integrity',
            'text': '''Academic integrity is the moral code or ethical policy of academia. 
            It includes values such as avoidance of cheating or plagiarism, maintenance of 
            academic standards, and honesty and rigor in research and academic publishing. 
            Academic integrity is important because it ensures that students and researchers 
            are held to high ethical standards and that their work is trustworthy and credible.
            In educational contexts, there are differing definitions of plagiarism depending 
            on the institution. However, the core principle remains the same: giving proper 
            credit to original sources.'''
        },
        {
            'source': 'Educational Research Journal',
            'url': 'https://example.com/research/plagiarism',
            'text': '''Plagiarism is the representation of another author's language, thoughts, 
            ideas, or expressions as one's own original work. In educational contexts, there are 
            differing definitions of plagiarism depending on the institution. Plagiarism is 
            considered a violation of academic integrity and can have significant consequences.
            Students must understand that proper attribution is essential. When you use someone 
            else's ideas or words, you must give credit to the original source.'''
        },
        {
            'source': 'University Writing Guide',
            'url': 'https://example.com/writing-guide',
            'text': '''Proper citation is essential in academic writing. When students use someone 
            else's ideas or words, they must give credit to the original source. This includes 
            direct quotes, paraphrased material, and even ideas that influenced their thinking. 
            Failure to cite sources properly is considered plagiarism and violates academic 
            integrity policies at most institutions. Teachers and professors take this seriously.'''
        },
        {
            'source': 'Research Ethics Handbook',
            'url': 'https://example.com/ethics',
            'text': '''Original research demonstrates critical thinking and deep understanding 
            of the subject matter. Students should strive to develop their own ideas and 
            arguments, supported by proper research and citation. The ability to synthesize 
            information from multiple sources and create something new is a key skill in 
            higher education. This separates excellent students from average ones. Academic 
            excellence requires both knowledge and integrity.'''
        },
        {
            'source': 'Academic Standards Guide',
            'url': 'https://example.com/standards',
            'text': '''Teachers and professors take academic integrity seriously because it 
            ensures that students and researchers are held to high ethical standards and that 
            their work is trustworthy and credible. When students maintain academic integrity, 
            they develop skills that will serve them throughout their professional careers. 
            These skills include critical thinking, research competency, and ethical decision-making.
            Understanding and following academic integrity principles is crucial for success.'''
        }
    ]
    
def main():
    print("=" * 70)
    print("PLAGIARISM CHECKER - Standalone Version")
    print("Advanced Document Analysis (No External Dependencies)")
    print("=" * 70)
    print()
    if len(sys.argv) < 2:
        print("Usage: python main.py <file_path>")
        print("\nSupported format: .txt")
        print("\nExample:")
        print("  python main.py document.txt")
        print("\nNote: For DOCX and PDF support, use the full version with dependencies.")
        return
    
    filepath = sys.argv[1]
    
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        return
    
    if not filepath.lower().endswith('.txt'):
        print("Error: Only .txt files are supported in standalone version.")
        print("For DOCX and PDF support, use the full version with dependencies.")
        return
    checker = SimplePlagiarismChecker()
    print(f"Processing: {filepath}")
    print("Extracting text...")
    
    try:
        text = checker.extract_text_from_txt(filepath)
        print(f"✓ Text extracted successfully ({len(text)} characters)")
        print(f"✓ Word count: {len(checker.tokenize(text))} words")
    except Exception as e:
        print(f"✗ Error: {e}")
        return
    print("\nLoading reference database...")
    database = create_sample_database()
    print(f"✓ {len(database)} reference documents loaded")



if __name__ == "__main__":
    main()
    