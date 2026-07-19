

def chunk_documents(documents:list[dict], max_words: int = 200)-> list[dict]:
    chunks = []
        
    if max_words < 0 :
        raise ValueError("max_words must be greater than  zero ):")
        
    for document in documents:
        text = document["text"]
        source = document["source"]
        paragraphs = text.split("\n\n")
            
        for chunk_id, paragraph in enumerate(paragraphs):
                 
            paragraph_text = paragraph.strip()
                
            if not  paragraph_text:
                continue
                
            words = paragraph_text.split()
                
            if len(words) > max_words:
                for i in range(0, len(words), max_words):
                    sub_words =  words[i : i+max_words]
                    sub_text = " ".join(sub_words)
                        
                    chunks.append({
                        "text":sub_text,
                        "source": source,
                        "chunk_id": f"{chunk_id}_sub_{i //max_words}"
                        })
                        
            else : 
                chunks.append({
                "text": paragraph_text,
                "source": source,
                "chunk_id": str(chunk_id)
                   }) 
                            
    return chunks
                
                
                

        
        
    
