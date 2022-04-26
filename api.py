from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List
from uuid import uuid4
from dotenv import load_dotenv
from pdfParse import parseResume
import os
import magic
import helperFunctions  # This is my helper functions directory

load_dotenv()
FILE_SAVE_DIRECTORY = helperFunctions._getResumeStorageDirectory()
RESUME_SAVE_MODE = os.getenv("RESUME_SAVE_MODE")

app = FastAPI()  # Initialize the FastAPI instance


@app.post("/upload-files")
async def uploadFile(uploadedFiles: List[UploadFile] = File(...)):
    resumeParseAnalysis = []

    for file in uploadedFiles:
        fileInBuffer = await file.read()

        # Use MIME type checks to ensure that the file uploaded is a PDF
        mimeType = magic.from_buffer(fileInBuffer)
        isPDF = mimeType.startswith("PDF document")
        print(isPDF)

        # Check for correct filetype uploaded from both the HTTP Header and the MIME Type
        if file.content_type != "application/pdf" or not isPDF:
            raise HTTPException(
                status_code=400, detail="File type incorrect - Not a PDF")

        else:
            try:

                # Create a unique filename to ensure no filename collisions exist
                filename = f"{str(uuid4())}-{file.filename}"
                fullPath = os.path.join(FILE_SAVE_DIRECTORY, filename)
                with open(fullPath, "wb") as fd:
                    fd.write(fileInBuffer)

                resumeParseAnalysis.append(parseResume(
                    fullPath, ["Cyber", "authentication", "React", "SQL", "Docker"]))

                if not RESUME_SAVE_MODE:
                    os.remove(fullPath)  # Delete file after analysis

            except:
                raise HTTPException(
                    status_code=422, detail="An error has occurred proccessing the uploaded documents")

    return resumeParseAnalysis
    # return {"file-recieved": True}
