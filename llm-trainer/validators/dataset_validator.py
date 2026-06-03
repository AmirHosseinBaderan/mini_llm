class DatasetValidator:
    
    def validate_document(self,doc):
        if not doc["text"]:
            return False
        
        if len(doc["text"]) < 20:
            return False
        
        return True