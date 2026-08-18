

def chunk_documents(documents:list[dict], max_words: int = 200, overlap_words: int = 30, min_words : int = 40)-> list[dict]:
    chunks = []
        
    if max_words <= 0 :
        raise ValueError("max_words must be greater than  zero ):")
    
    if overlap_words < 0 or overlap_words >= max_words:
        raise ValueError("overlab_worda must be beetween 0 and max_words")
    
    if min_words <= 0  or min_words > max_words:
        raise ValueError("min_words must be between one and max_words")
    
        
    for document in documents:
        text = document["text"]
        source = document["source"]
        domain = document.get("domain")
        file_type = document.get("file_type")
        paragraphs = text.split("\n\n")
        
        paragraph_groups = []
        buffer_words = []
        buffer_start_id = None
        buffer_end_id = None
            
        for paragraph_id, paragraph in enumerate(paragraphs):
                 
            paragraph_text = paragraph.strip()
                
            if not  paragraph_text:
                continue
                
            words = paragraph_text.split()
                
            if buffer_start_id is None:
                buffer_start_id = paragraph_id  
                              
            buffer_end_id = paragraph_id
            buffer_words.extend(words)
            
            if len(buffer_words) >= min_words :
                paragraph_groups.append({
                    "words":buffer_words,
                    "start_id": buffer_start_id,
                    "end_id": buffer_end_id
                })
                
                buffer_words = []
                buffer_start_id = None
                buffer_end_id = None
                     
           
        if buffer_words:
            if paragraph_groups:
                previous_group = paragraph_groups[-1] 
                previous_group["words"].extend(buffer_words)
                previous_group["end_id"] = buffer_end_id
                
            else:
                paragraph_groups.append({
                    "words": buffer_words,
                    "start_id": buffer_start_id,
                    "end_id": buffer_end_id
                    })
        
        
        for group in paragraph_groups:
            
           group_words = group["words"]
           start_id = group["start_id"]
           end_id = group["end_id"]

           if start_id == end_id:
            group_id = str(start_id)
            
           else:
             group_id = f"{start_id}_{end_id}"

           if len(group_words) <= max_words:
             chunks.append({
               "text": " ".join(group_words),
               "source": source,
               "chunk_id": group_id,
               "domain": domain,
               "file_type": file_type
        })
             continue

           start = 0
           sub_chunk_id = 0

           while start < len(group_words):
            end = min(start + max_words, len(group_words))
            sub_words = group_words[start:end]

            chunks.append({
            "text": " ".join(sub_words),
            "source": source,
            "chunk_id": f"{group_id}_sub_{sub_chunk_id}",
            "domain": domain,
            "file_type": file_type
        })

            if end == len(group_words):
              break

            start = end - overlap_words
            sub_chunk_id += 1
       
    return chunks
                
                
                

        
        
    
