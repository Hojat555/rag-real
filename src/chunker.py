

def chunk_documents(documents:list[dict], max_words: int = 200, overlap_words: int = 30)-> list[dict]:
    chunks = []
        
    if max_words <= 0 :
        raise ValueError("max_words must be greater than  zero ):")
    
    if overlap_words < 0 or overlap_words >= max_words:
        raise ValueError("overlab_worda must be beetween 0 and max_words")
    
        
    for document in documents:
        text = document["text"]
        source = document["source"]
        domain = document.get("domain")
        file_type = document.get("file_type")
        paragraphs = text.split("\n\n")
            
        for chunk_id, paragraph in enumerate(paragraphs):
                 
            paragraph_text = paragraph.strip()
                
            if not  paragraph_text:
                continue
                
            words = paragraph_text.split()
                
            if len(words) > max_words:
                start = 0
                sub_chunk_id = 0
                
                while start < len(words):
                    end = min(start + max_words, len(words))
                    sub_words = words[start:end]
        
                    chunks.append({
                        "text":" ".join(sub_words),
                        "source": source,
                        "chunk_id": f"{chunk_id}_sub_{sub_chunk_id}",
                        "domain": domain,
                        "file_type": file_type,
                        })  
                    if end == len(words):
                        break
                    start = end - overlap_words
                    sub_chunk_id += 1 
                     
            else : 
                chunks.append({
                "text": paragraph_text,
                "source": source,
                "chunk_id": str(chunk_id),
                "domain": domain,
                "file_type": file_type,
                   }) 
                            
    return chunks
                
                
                

        
        
    
