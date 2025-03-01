from fastapi import FastAPI
from pydantic import BaseModel
from huggingface import genearateOutfit
from fastapi.middleware.cors import CORSMiddleware
from database import supabase

app = FastAPI()

'''app.add_middleware(
    CORSMiddleware,
    allow_origin=['http://localhost:3000'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)'''

# Health check endpoint
@app.get("/")
def healthcheck():
    return {"message": "Health check check"}

# Define request model
class ChatRequest(BaseModel):
    user_message: str
    temp: str

# AI Chatbot endpoint
@app.post("/chat")
def chat(request: ChatRequest):
    response = genearateOutfit(request.user_message, request.temp)
    return {"response": response}

# Clothing item model
class ClothingItem(BaseModel):
    user_id: str
    item_type: str
    material: str
    color: str
    formality: str
    pattern: str
    fit: str
    suitable_for_weather: str
    suitable_for_occasion: str

# User preference model
class UserPreferencce(BaseModel):
    user_id: str
    preferred_fit: str
    preferred_colors: list
    preferred_formality: str
    preferred_patterns: list
    preferred_temperature: str

# Add clothing item
@app.post("/add_clothing_item/")
async def add_clothing_item(item: ClothingItem):
    data, error = supabase.table("clothing_items").insert(item.dict()).execute()
    if error:
        return {"error": str(error)}
    return{"message": "Clothing item added succesfully", "data": data}

# Get all clothing items
@app.get("/clothing_items/")
async def get_clothing_items():
    try:
        response = supabase.table("clothing_items").select("*").execute()
        if not response.data:
            return {"data": []}
        return {"data": response.data}
    except Exception as e:
        return {"error": f"Internal Server Error: {str(e)}"}


# Add user preference
@app.post("/add_user_preference/")
async def add_user_preference(pref: UserPreferencce):
    data, error = supabase.table("user_preferences").insert(pref.dict()).execute()
    if error:
        return {"error": error}
    return {"messaga": "User preference added", "data": data}