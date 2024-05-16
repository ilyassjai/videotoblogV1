from werkzeug.utils import secure_filename  # type: ignore
from flask import Flask, request, jsonify  # type: ignore
from flask_cors import CORS # type: ignore
from utils import *
from whisper import *
from llm import *
from youtubeAPI import *
from langchain_openai import ChatOpenAI
from google.cloud import firestore, storage
from datetime import datetime
import os
import glob
from dotenv import load_dotenv
import subprocess

app = Flask(__name__)
CORS(app)

ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

@app.route('/')
def index():
    return jsonify({'status': 'server is live'})

@app.route('/process-youtube-link', methods=['POST'])
def process_youtube_link():
    data = request.get_json()
    youtube_link = data.get('youtubeLink')

    load_dotenv()
    os.environ['OPENAI_API_KEY'] = 'sk-proj-UDfHlTwwCvVi9IbX0laOT3BlbkFJUDCLXgNqtUgJQkPp7ypb'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/sbcodes/Downloads/v2bdb-423513-c5346e202132.json'
    openai_api_key = os.getenv('OPENAI_KEY')

    image_paths = [file for file in glob.glob(os.path.join('./slidemse', '*.png'))]    
    md_paths = [f"output{i}.md" for i in range(len(image_paths))]

    #start
    llm = ChatOpenAI(openai_api_key=openai_api_key,model="gpt-3.5-turbo",temperature=0.5)
    df_slides=videotodataframe(youtube_link)
    chat(llm,df_slides)
    merged_md = merge_markdown_with_images(md_paths, image_paths)

    with open("merged_output.md", "w") as f:
        f.write(merged_md)

    # Connect to Firestore
    db = firestore.Client()

    # Generate a unique ID for the article
    article_id = db.collection('articles').document().id

    # Store the results of the API call in Firestore
    doc_ref = db.collection('articles').document(article_id)
    doc_ref.set({
        'id': article_id,
        'title': 'your_title',  # Replace with your actual title
        'content': merged_md,  # Replace with your actual content
        'date_created': datetime.now(),
    })

    # Upload the images to Google Cloud Storage
    bucket_name = 'images-for-articles'
    for image_path in image_paths:
        # Name the image using the article ID
        destination_blob_name = f"{article_id}_{os.path.basename(image_path)}"
        upload_blob(bucket_name, image_path, destination_blob_name)

    return jsonify({'message': 'Processing completed!'})

if __name__ == '__main__':
    app.run(debug=True)