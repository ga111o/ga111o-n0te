import os
from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv
from fastapi.responses import RedirectResponse

load_dotenv()

app = FastAPI()

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
BUCKET_NAME = os.getenv('BUCKET_NAME')

s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name='us-east-2'
)


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        s3.upload_fileobj(file.file, BUCKET_NAME, file.filename)
        return {"filename": file.filename}
    except NoCredentialsError:
        return {"error": "Credentials not available"}
    except Exception as e:
        return {"error": str(e)}


@app.get("/")
async def read_root():
    return RedirectResponse(url="/static/index.html")
