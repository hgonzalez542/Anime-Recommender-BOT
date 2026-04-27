from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import random
import json
from datetime import datetime

# IMPORT YOUR RECOMMENDER
from .recommender import AnimeRecommender

app = FastAPI()
recommender = AnimeRecommender()

# CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# REQUEST MODEL 
class PromptRequest(BaseModel):
    prompt: str


# CHAT LOGGER 
class ChatLogger:

    def __init__(self, filename="chat_history.txt"):
        self.filename = filename

    def save_chat(self, prompt):
        with open(self.filename, "a") as f:  # FILE I/O
            timestamp = datetime.now()
            f.write(f"{timestamp} - {prompt}\n")

    def read_history(self):
        try:
            with open(self.filename, "r") as f:
                return f.readlines()
        except FileNotFoundError:
            return []


logger = ChatLogger()


# HELPER FUNCTION (DICTIONARY + LOOP)
def count_genres(anime_list):
    genre_count = {}  # dictionary

    for anime in anime_list:  # for loop
        for g in anime.get("genres", []):
            genre_count[g] = genre_count.get(g, 0) + 1

    return genre_count


# API ENDPOINT
@app.post("/chat")
def chat(req: PromptRequest):

    prompt = req.prompt  # variable

    print(f"User searched: {prompt}")  # formatted output

    # SAVE CHAT (FILE I/O)
    logger.save_chat(prompt)

    parsed, results = recommender.recommend(prompt)

    new_gen = results["new_gen"]
    old_gen = results["old_gen"]

    # MATH EXPRESSION + RANDOM
    for anime in new_gen:
        anime["score"] = anime.get("rating", 0) * 0.5 + random.uniform(0, 1)

    # WHILE LOOP
    i = 0
    while i < len(old_gen):
        old_gen[i]["score"] = old_gen[i].get("rating", 0) * 0.4 + random.uniform(0, 1)
        i += 1

    # DICTIONARY USAGE
    genre_summary = count_genres(new_gen + old_gen)

    # RESPONSE
    return {
        "assistant_message": f"I analyzed your request: '{prompt}' and found matching anime.",
        "new_gen": new_gen,
        "old_gen": old_gen,
        "genre_summary": genre_summary 
    }