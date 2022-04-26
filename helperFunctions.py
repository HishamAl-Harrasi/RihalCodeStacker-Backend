import pathlib
import os
from dotenv import load_dotenv


# Functions in this file are helper functions which
# are used for organising and simplifying the code


def _getResumeStorageDirectory():
    load_dotenv()

    currentDirectory = pathlib.Path(__file__).parent.resolve()
    RESUME_DIRECTORY = os.getenv("RESUME_DIRECTORY")

    return os.path.join(currentDirectory, RESUME_DIRECTORY)
