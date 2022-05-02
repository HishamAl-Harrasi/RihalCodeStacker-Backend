from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from uuid import uuid4
from dotenv import load_dotenv
from pdfParse import parseResume
import os
import magic
import helperFunctions  # This is my helper function library

# This is the main backend API file - it contains one endpoint (/upload-files),
# which the front end accesses to upload the resume files and keywords
# being searched for


load_dotenv()
FILE_SAVE_DIRECTORY = helperFunctions._getResumeStorageDirectory()

# This allows the server admin to set whether they want the uploaded resumes to
# be saved or discarded after their analysis - Note that these files will be
# saved into the resumeFiles directory, although this file save directory can be changed
# in the .env file. This functionality can be toggled on or off from the .env file as well
RESUME_SAVE_MODE = os.getenv("RESUME_SAVE_MODE")


app = FastAPI()  # Initialize the FastAPI instance


origins = ["*"]  # Options to allow for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload-files")
async def uploadFile(files: List[UploadFile] = File(...), keywords: List[str] = None):
    # Initial input validation and checking - This is handled on the front end but is here for enforcement of the rule

    if (len(files) < 1) or (len(keywords) < 1):
        HTTPException(
            status_code=422, detail="No files or keywords were provided in the request")

    acceptedFiles = []      # Array containing the files for which keywords were found
    unacceptedFiles = []    # Array containing the files for which no keywords were found

    saveMode = True if RESUME_SAVE_MODE == "True" else False

    for file in files:
        fileInBuffer = await file.read()

        # The following runs some security checks to ensure that the submitted
        # file is a PDF - If the file type is not a PDF, the file gets rejected

        # Use MIME type checks to ensure that the file uploaded is a PDF
        mimeType = magic.from_buffer(fileInBuffer)
        isPDF = mimeType.startswith("PDF document")

        # Check for correct filetype uploaded from both the HTTP Header and the MIME Type
        if file.content_type != "application/pdf" or not isPDF:
            raise HTTPException(
                status_code=400, detail="File type incorrect - Not a PDF")

        else:
            try:

                # Create a unique filename to ensure no filename collisions exist - This is used for storing the file locally
                filename = f"{str(uuid4())}-{file.filename}"
                fullPath = os.path.join(FILE_SAVE_DIRECTORY, filename)
                with open(fullPath, "wb") as fd:
                    fd.write(fileInBuffer)

                # Run the PDF parse and keyword search
                keywordsFound = parseResume(fullPath, keywords)

                if len(keywordsFound) > 0:
                    acceptedFiles.append(
                        {"filename": file.filename, "keywordsFound": keywordsFound})
                else:
                    unacceptedFiles.append({"filename": file.filename})

                if (not saveMode):  # Delete file after analysis if save mode is turned off
                    os.remove(fullPath)

            except:
                raise HTTPException(
                    status_code=422, detail="An error has occurred proccessing the uploaded documents")

    # Create the response object
    httpResponse = {}
    httpResponse["acceptedFiles"] = acceptedFiles
    httpResponse["unacceptedFiles"] = unacceptedFiles

    return httpResponse
