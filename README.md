# 🔍 Plagiarism Checker - Academic Integrity Tool

A standalone plagiarism detection system that analyzes text documents for similarity against a reference database. Currently supports TXT files with plans for expanded format support.

## ✨ Features

- **Text File Support**: TXT file analysis
- **Advanced Detection Algorithms**:
  - Jaccard similarity coefficient
  - Cosine similarity with word frequency analysis
  - N-gram matching with stop word filtering
  - Sequence matching using difflib
  - Common phrase detection
- **Comprehensive Reports**: Detailed plagiarism reports with match analysis
- **Similarity Scoring**: Color-coded results (Green/Yellow/Red)
- **Source Attribution**: Identifies specific sources and matching sequences
- **No External Dependencies**: Standalone version using only Python standard library

## 📋 Requirements

### Standalone Version
- Python 3.8+
- No external dependencies required
- Built using Python standard library only

### Future Enhancements (Planned)
- python-docx (for DOCX support)
- pypdf (for PDF support)
- pdfplumber (for advanced PDF parsing)
- nltk (for enhanced text processing)
- scikit-learn (for advanced similarity algorithms)

## 🚀 Quick Start

1. **Navigate to the project directory**:
   ```bash
   cd "Python Project/PLAGIARISM CHECKER V.01/Project"
   ```

2. **Run the plagiarism checker**:
   ```bash
   python main.py document.txt
   ```
   
   **Currently supported**: TXT files only
   
   **Example with the included sample**:
   ```bash
   python main.py plagiarism_report_sample_document.txt
   ```

3. **View results**:
   - Results are displayed in the terminal
   - A detailed report is saved as `plagiarism_report_[filename].txt`
   - Similarity score with color-coded status

**Note**: For DOCX and PDF support, use the full version with dependencies (planned enhancement).

## 📖 Usage Examples

### Example 1: Check the Sample Document
```bash
python main.py plagiarism_report_sample_document.txt
```

**Output**:
```
======================================================================
PLAGIARISM CHECKER - Standalone Version
Advanced Document Analysis (No External Dependencies)
======================================================================

Processing: plagiarism_report_sample_document.txt
Extracting text...
✓ Text extracted successfully (3334 characters)
✓ Word count: 333 words

Loading reference database...
✓ 5 reference documents loaded

Analyzing document for similarity...
✓ Analysis complete!

OVERALL SIMILARITY: 26.56%
[█████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]
Status: 🟡 YELLOW - REVIEW NEEDED
======================================================================
```

### Example 2: Check Your Own Text File
```bash
python main.py your_document.txt
```

### Color-Coded Results:
- **🟢 Green** (0-15%): Low similarity - Acceptable ✓
- **🟡 Yellow** (15-30%): Moderate similarity - Review needed ⚠
- **🔴 Red** (30%+): High similarity - Significant concern ✗

## 🎯 Understanding Results

### Similarity Scores

| Score Range | Interpretation | Action Required |
|-------------|---------------|-----------------|
| 0-15% | **Low Similarity** - Acceptable | ✓ Generally acceptable for submission |
| 15-30% | **Moderate Similarity** - Review | ⚠ Review matches, ensure proper citation |
| 30%+ | **High Similarity** - Concern | ✗ Significant revision needed |

### Report Components

1. **Overall Similarity Score**: Percentage of content matching existing sources
2. **Total Words**: Number of words analyzed
3. **Matched Words**: Number of words found in sources
4. **Sources Found**: Number of matching sources detected
5. **Unique Content**: Percentage of original content
6. **Detailed Matches**: Specific sources and matching sequences

## 🔧 Advanced Features

### Custom Database

To check against your own database of documents, modify the `create_sample_database()` function in `main.py`:

```python
def create_sample_database() -> List[Dict]:
    return [
        {
            'source': 'Your Document Title',
            'url': 'https://your-url.com',
            'text': 'Your document text here...'
        },
        # Add more documents...
    ]
```

### Adjusting Sensitivity

Modify these parameters in the `SimplePlagiarismChecker` class:

```python
self.min_match_length = 5  # Minimum words for a match (default: 5)
```

In the `check_against_database` method:
```python
if similarity > 5:  # Minimum similarity to report (default: 5%)
```

### Integration with Web Services

To connect the web interface with real plagiarism detection APIs:

1. **Turnitin API** (commercial)
2. **Copyscape API** (commercial)
3. **Custom implementation** using the Python backend

Example integration in the HTML file:
```javascript
async function checkPlagiarism() {
    const formData = new FormData();
    formData.append('file', uploadedFile);
    
    const response = await fetch('/api/check-plagiarism', {
        method: 'POST',
        body: formData
    });
    
    const results = await response.json();
    displayResults(results);
}
```

## 📊 Technical Details

### Text Extraction

- **DOCX**: Uses `python-docx` to parse document structure
- **PDF**: Primary: `pdfplumber` (better for tables), Fallback: `pypdf`
- **TXT**: Direct UTF-8 text reading with error handling

### Similarity Detection Algorithms

1. **TF-IDF with Cosine Similarity**:
   - Converts text to numerical vectors
   - Measures angle between vectors
   - Effective for overall document similarity

2. **N-gram Matching**:
   - Identifies common phrase patterns
   - Detects paraphrased content
   - Configurable n-gram size

3. **Sequence Matching**:
   - Uses difflib for longest common subsequences
   - Finds exact and near-exact matches
   - Highlights specific plagiarized sections

### Performance Optimization

- Text preprocessing removes stop words
- Efficient vectorization with sklearn
- Batch processing for multiple documents
- Caching for repeated checks

## 🛠️ Troubleshooting

### Common Issues

**Issue**: "Module not found" error
```bash
# Solution: Install dependencies manually
pip install python-docx pypdf pdfplumber nltk scikit-learn --break-system-packages
```

**Issue**: PDF extraction returns empty text
```bash
# Solution: PDF might be scanned image. Use OCR:
pip install pytesseract pdf2image --break-system-packages
```

**Issue**: NLTK data not found
```python
# Solution: Download NLTK data manually
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

**Issue**: Web interface doesn't show file content
- **Solution**: The standalone HTML version uses simulated detection. For actual file processing, use the Python backend or integrate with an API.

## 📝 File Structure

```
Project/
├── main.py                               # Main plagiarism checker script
├── index.html                            # Web interface (placeholder)
├── plagiarism_report_sample_document.txt # Sample document for testing
├── README.md                             # This file
├── requirements.txt                      # Dependencies for future enhancements
└── .venv/                               # Virtual environment
```

## 🔒 Privacy & Ethics

- **Local Processing**: All text processing happens locally (Python version)
- **No Data Storage**: Files are not stored after analysis
- **Educational Purpose**: This tool is for educational integrity
- **Ethical Use**: Should be used to improve writing, not circumvent detection

## 🎓 Use Cases

1. **Students**: Check work before submission
2. **Educators**: Verify assignment originality
3. **Researchers**: Ensure proper citation
4. **Publishers**: Verify manuscript originality
5. **Content Creators**: Check for unintentional duplication

## 🚀 Future Enhancements

- [ ] Support for DOCX files (Word documents)
- [ ] Support for PDF files
- [ ] Web interface implementation
- [ ] Real-time web search integration
- [ ] Multi-language support
- [ ] Enhanced similarity algorithms (TF-IDF, sklearn integration)
- [ ] Paraphrase detection
- [ ] Citation analysis
- [ ] Batch processing
- [ ] Cloud API integration
- [ ] Machine learning improvements
- [ ] Similarity visualization
- [ ] Export to multiple formats (PDF, DOCX, HTML)

## 📄 [License](./LICENSE.md): Proprietary – Permission Required

This tool is for educational purposes. Ensure you have the right to analyze any documents you check.

## 🤝 Contributing

To enhance this tool:
1. Add support for more file formats
2. Implement additional similarity algorithms
3. Integrate with external APIs
4. Improve the UI/UX
5. Add multilingual support

## ⚠️ Disclaimer

This tool provides automated similarity detection but should not be the sole basis for academic integrity decisions. Human review and judgment are essential. Results should be interpreted in context with proper understanding of citation practices and academic standards.

---

**Made with ❤️ for academic integrity**
