from fastapi import FastAPI, UploadFile, File, HTTPException
import PyPDF2
from typing import List
from uuid import uuid4
import magic
# import mimetypes



app = FastAPI()



@app.post("/upload-file")
async def uploadFile(uploadedFiles: List[UploadFile] = File(...)):

    for file in uploadedFiles:
        fileInBuffer = await file.read()

        mimeType = magic.from_buffer(fileInBuffer)
        isPDF = mimeType.startswith("PDF document") # Use MIME type checks to ensure that the file uploaded is a PDF
        print(isPDF)

        if file.content_type != "application/pdf" or not isPDF: # Check for correct filetype uploaded from both the HTTP Header and the MIME Type 
            raise HTTPException(status_code=400, detail="File type incorrect - Not a PDF")
        
        else:
            filename = f"{str(uuid4())}-{file.filename}" # Create a unique filename to ensure no filename collisions exist
            
            with open(filename, "wb") as fd:
                fd.write(fileInBuffer)

    return {"file-recieved": True}
    

