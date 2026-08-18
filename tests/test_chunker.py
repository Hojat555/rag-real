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
    
    result = chunk_documents(documents, max_words=20, min_words=1, overlap_words=0)
    
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
    
    
    result = chunk_documents(documents, max_words = 2, overlap_words=0, min_words=1)
    
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

def test_large_paragraph_has_overlap():
    documents = [{
        "text": "one two three four five six seven eight",
        "source": "sample.txt",
        "domain": "test",
        "file_type": ".txt"
    }]

    chunks = chunk_documents(
        documents,
        max_words=5,
        overlap_words=2,
        min_words=1
    )

    assert chunks[0]["text"] == "one two three four five"
    assert chunks[1]["text"] == "four five six seven eight"
    
def test_chunker_merges_small_paragraphs():
    documents = [
        {
            "text": "one two\n\nthree four\n\nfive six seven",
            "source": "test.txt"
        }
    ]
    
    chunks = chunk_documents(
        documents,
        max_words=20,
        min_words=5,
        overlap_words=0
    )
    
    assert len(chunks) == 1
    assert chunks[0]["text"] == "one two three four five six seven"
    


    
    

