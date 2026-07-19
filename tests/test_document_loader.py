import pytest
from src.document_loader import load_documents

def test_load_documents_reads_txt_file(tmp_path):
    sample_file = tmp_path / "sample.txt"
    sample_file.write_text("Hello world", encoding="utf-8")
    
    result = load_documents(tmp_path)
    
    
    assert len(result) == 1
    assert result[0]["text"] == "Hello world"
    assert result[0]["source"] == "sample.txt"  


def test_empty_folder_error(tmp_path):
    with pytest.raises(ValueError):
        load_documents(tmp_path)


def test_missing_folder_raises_error(tmp_path):
    missing_path = tmp_path / "missing"
    
    with pytest.raises(FileNotFoundError):
        load_documents(missing_path)


def test_ignores_empty_file(tmp_path):
    valid_file = tmp_path / "valid.txt"
    valid_file.write_text("Hello World",  encoding="utf-8")

    empty_file = tmp_path / "empty.txt"
    empty_file.write_text("   \n\n   ", encoding="utf-8")

    result = load_documents(tmp_path)

    expected = [
        {
            "text": "Hello World",
            "source": "valid.txt"
        }
    ]

    assert result == expected
    
    

def test_ignore_unsupprted_file(tmp_path):
    valid_file = tmp_path/"valid.txt"
    unsupported_file =  tmp_path /"image.pdf"
    
    valid_file.write_text("Hello World", encoding="utf-8")
    unsupported_file.write_text("Ignored content",encoding="utf-8")
    
    result = load_documents(tmp_path)
    
    expected = [
        {
            "text": "Hello World",
            "source": "valid.txt"
        }
    ]
    
    assert expected == result


