from pathlib import Path
    
def load_documents(folder_path:Path)->list[dict]:
         documents = []
         
         
         if not folder_path.exists():
             raise FileNotFoundError(f" This path{folder_path} is not found!")
       
        
         for file in folder_path.glob("*.txt"):
            text = file.read_text(encoding = "utf-8")
            
            if not text.strip():
                continue
            
            documents.append({
                "text":text,
                "source":file.name
            })
         if not documents:
             raise ValueError("there is no any file here! ):")
         
        
         return documents
        
