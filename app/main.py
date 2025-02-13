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
    SELECT  'red' as color,
            'Business Term' as type, 
            businessterm AS term,
            null as de_description, 
            null as legal_cons, 
            null as datatype, 
            null as PII_status, 
            null as confidential_level, 
            null as associated_businessterm,
            description as term_description,
            abbreviation,
            link_asset
    FROM public.businessglossary WHERE 
        businessterm::text ILIKE %s OR
        description::text ILIKE %s OR
        abbreviation::text ILIKE %s OR
        link_asset::text ILIKE %s
    UNION all
    SELECT  'blue' as color, 
            'Data Element' as type, 
            dataelement AS term,
            description as de_description, 
            legal_cons, 
            datatype, 
            PII_status, 
            confidential_level, 
            associated_businessterm,
            null as term_description,
            null as abbreviation,
            null as link_asset
    FROM public.datadictionary WHERE 
        dataelement::text ILIKE %s OR
        description::text ILIKE %s OR
        legal_cons::text ILIKE %s OR
        datatype::text ILIKE %s OR
        PII_status::text ILIKE %s OR
        confidential_level::text ILIKE %s OR
        associated_businessterm::text ILIKE %s
    """
    
    cursor.execute(query, tuple(['%' + q + '%'] * 11))
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