from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
app = FastAPI()
# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="thangcoi123",
    host="localhost",
    port="5432"
)

@app.get("/search", response_model=List[dict])
def search(q: str = Query(..., min_length=1)):
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM public.newtable WHERE namedest LIKE %s", ('%' + q + '%',))
    results = cursor.fetchall()
    cursor.close()
    if not results:
        raise HTTPException(status_code=404, detail="No results found")
    return results
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the HTML file
@app.get("/")
def read_root():
    return FileResponse('static/index.html')
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)