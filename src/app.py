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
from datetime import timedelta
import pytz


app = Flask(__name__)
CORS(app)

ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi'}



# Function to get the title from merged_output.md
def get_title_from_md_file(md_file_path):
    if not os.path.isfile(md_file_path):
        print(f"File does not exist: {md_file_path}")
        return None
    
    with open(md_file_path, 'r') as f:
        lines = f.readlines()

    if lines:  # Check if lines is not empty
        title = lines[0].replace('#', '').strip()
    else:
        title = "No title found"

    return title
    

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
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/sbcodes/Downloads/v2bdb-423513-c5346e202132.json'
    openai_api_key = os.getenv('OPENAI_KEY')

    image_paths = [file for file in glob.glob(os.path.join('./slidemse', '*.png'))]    
    md_paths = [f"./outputs/output{i}.md" for i in range(len(image_paths))]

    #start
    llm = ChatOpenAI(openai_api_key=openai_api_key,model="gpt-3.5-turbo",temperature=0.5)
    df_slides=videotodataframe(youtube_link)
    chat(llm,df_slides)


    image_paths = [file for file in glob.glob(os.path.join('./slidemse', '*.png'))]    
    md_paths = [f"./outputs/output{i}.md" for i in range(len(image_paths))]


    merged_md = merge_markdown_with_images(md_paths, image_paths)

    
    # Connect to Firestore
    db = firestore.Client()

    # Generate a unique ID for the article
    article_id = db.collection('articles').document().id

    # Upload the images to Google Cloud Storage
    bucket_name = 'images_for_articles'
    merged_md = merge_markdown_with_images(md_paths, image_paths)
    print(f"Uploading {len(image_paths)} slides: {image_paths}")
    for i, image_path in enumerate(image_paths):
        # Create a directory named after the article ID
        directory_name = f"{article_id}"
        destination_blob_name = f"{directory_name}/{os.path.basename(image_path)}"
        # Name the image using the article ID and the original file name
        destination_blob_name = f"{directory_name}/slide_{i}.png"
        upload_blob(bucket_name, image_path, destination_blob_name)
        # Get the URL of the image
        image_url = get_image_url(bucket_name, destination_blob_name)
        # Replace the local image path with the URL in the markdown
        merged_md = merged_md.replace(image_path, image_url)

    if destination_blob_name is not None:
        thumbnail_url = get_image_url(bucket_name, destination_blob_name)
    else:
        print("destination_blob_name is None")
        thumbnail_url = None
    # Write the merged markdown to a file
    
    with open("merged_output.md", "w") as f:
        f.write(merged_md)
    title = get_title_from_md_file("merged_output.md")    

    # Store the results of the API call in Firestore
    doc_ref = db.collection('articles').document(article_id)
    doc_ref.set({
        'id': article_id,
        'title': title,  # Replace with your actual title
        'content': merged_md,  # Replace with your actual content
        'date_created': firestore.SERVER_TIMESTAMP,
        'thumbnail_url': thumbnail_url,
    })

    # Delete the temporary files
    for file in md_paths:
        os.remove(file)

    for file in image_paths:
        os.remove(file)

    # Delete the merged markdown file
    os.remove("merged_output.md")
    return jsonify({'message': 'Processing completed!', 'article_id': article_id})  

if __name__ == '__main__':
    app.run(debug=True)