from src.chunker import chunk_documents
import pytest


def test_splits_two_paragraphs_and_preserves_metadata():
    
    documents = [
        {
            "text":"First paragraph.\n\nSecond paragraph.",
            "source" :"document.txt",
            "domain": "artificial_intelligence",
            "file_type": ".txt",
        }
    ]
    
    result = chunk_documents(documents)
    
    expected = [
        {
            "text": "First paragraph.",
            "source": "document.txt",
            "chunk_id": "0",
            "domain": "artificial_intelligence",
            "file_type": ".txt",
        },
        {
            "text": "Second paragraph.",
            "source": "document.txt",
            "chunk_id": "1",
            "domain": "artificial_intelligence",
            "file_type": ".txt",
        }
    ]
    
    
    assert result == expected
    


def test_splits_large_paragraph_without_losing_words():
    
    documents = [
        {
            "text": "one two three four five",
            "source": "document.txt",
            "domain": "artificial_intelligence",
            "file_type": ".txt",
        }
    ]
    
    
    result = chunk_documents(documents, max_words = 2)
    
    expected = [
        {
            "text": "one two",
            "source": "document.txt",
            "chunk_id": "0_sub_0",
            "domain": "artificial_intelligence",
            "file_type": ".txt",
        },
        {
            "text": "three four",
            "source": "document.txt",
            "chunk_id": "0_sub_1",
            "domain": "artificial_intelligence",
             "file_type": ".txt",
        },
        {
            "text": "five",
            "source": "document.txt",
            "chunk_id": "0_sub_2",
            "domain": "artificial_intelligence",
            "file_type": ".txt",
        }
    ]
    
    assert expected == result

    
    

