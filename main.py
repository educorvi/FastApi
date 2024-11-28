import json
import base64
from typing import Union
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional
from ner import analyze_text

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/api/v1/CaseImport")
async def post_item(request:Request):
    try:
        raw = await request.json()  # Parse JSON body
        data = json.loads(raw)
        complete = open("/Users/larswalther/HiDrive/public/Kundenfreigaben/ShowCase/CaseFile.json", "wb")
        complete.write(raw.encode('utf-8'))
        complete.close()
        filetickets = data['fs_dateiupload']
        for ticket in filetickets:
            filename = f"New_{ticket['metadata']['filename']}"
            base64_string = ticket['base64_filedata']
            binary_data = base64.b64decode(base64_string)
            output_file_path = f"/Users/larswalther/HiDrive/public/Kundenfreigaben/ShowCase/{filename}"
            with open(output_file_path, "wb") as file:
                file.write(binary_data)
                file.close()
        return {"status": "success"}  # Return the parsed JSON for demonstration
    except Exception as e:
        return {"error": "Invalid JSON", "details": str(e)}

@app.post("/api/v1/NerCheck")
async def post_sentence(request:Request):
    data = await request.json()
    ret = analyze_text(data)
    return ret
