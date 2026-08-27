from pydantic import BaseModel

class User_question(BaseModel):
    question:str
    
class AI_Response(BaseModel):
    response:str
        
