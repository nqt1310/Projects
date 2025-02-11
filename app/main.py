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

# Connect to your PostgreSQL databases
conn1 = psycopg2.connect(
    dbname="db1",
    user="user1",
    password="password1",
    host="db1",
    port="5432"
)

conn2 = psycopg2.connect(
    dbname="db2",
    user="user2",
    password="password2",
    host="db2",
    port="5433"
)

@app.get("/search", response_model=List[dict])
def search(q: str = Query(..., min_length=1)):
    cursor1 = conn1.cursor(cursor_factory=RealDictCursor)
    cursor2 = conn2.cursor(cursor_factory=RealDictCursor)
    
    cursor1.execute("SELECT * FROM public.businessglossary WHERE namedest LIKE %s", ('%' + q + '%',))
    results1 = cursor1.fetchall()
    
    cursor2.execute("SELECT * FROM public.datadictionary WHERE namedest LIKE %s", ('%' + q + '%',))
    results2 = cursor2.fetchall()
    
    cursor1.close()
    cursor2.close()
    
    results = results1 + results2
    
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