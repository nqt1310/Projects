from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

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
DATABASE_URL = os.getenv("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

@app.get("/search", response_model=List[dict])
def search(q: str = Query(..., min_length=1)):
    cursor = conn.cursor()
    
    query = """
    SELECT 'red' as color,term as type, businessterm AS term FROM public.businessglossary WHERE id||businessterm||description||abbreviation||link_asset LIKE %s
    UNION
    SELECT 'blue' as color, DE as type, dataelement AS term FROM public.datadictionary WHERE id||dataelement||description||legal_cons||"datatype"||pii_status||confidential_level||associated_businessterm LIKE %s
    """
    
    cursor.execute(query, ('%' + q + '%', '%' + q + '%'))
    results = cursor.fetchall()
    
    cursor.close()
    
    if not results:
        raise HTTPException(status_code=404, detail="No results found")
    
    return results

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Serve the HTML file
@app.get("/")
def read_root():
    return FileResponse('app/static/index.html')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)