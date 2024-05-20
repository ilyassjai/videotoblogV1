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
import json

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



if __name__ == "__main__":
    load_dotenv()
    if len(sys.argv) < 2:
        print("Please provide a YouTube link as a command-line argument.")
        sys.exit(1)

    url = sys.argv[1]

    print(f"Current working directory: {os.getcwd()}")

    # Use absolute path for the credentials file
    credentials_path = os.path.abspath('/Users/asilbekmuminov/code/TER/videotoblogV1/core_app/src/v2bdb-423513-c5346e202132.json')
    print(f"Using credentials file at: {credentials_path}")


    # url = 'https://www.youtube.com/watch?v=Fk1gXKbcMo0'
    openai_api_key = os.getenv('OPENAI_KEY')
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'v2bdb-423513-c5346e202132.json' 

    image_paths = [file for file in glob.glob(os.path.join('./slidemse', '*.png'))]    
    md_paths = [f"output{i}.md" for i in range(len(image_paths))]

    #start
    llm = ChatOpenAI(openai_api_key=openai_api_key,model="gpt-3.5-turbo",temperature=0.5)
    df_slides=videotodataframe(url)
    chat(llm,df_slides)
    merged_md = merge_markdown_with_images(md_paths, image_paths)

    with open("merged_output.md", "w") as f:
        f.write(merged_md)

    # Connect to Firestore
    db = firestore.Client()

    # Generate a unique ID for the article
    article_id = db.collection('articles').document().id

    # Upload the images to Google Cloud Storage
    bucket_name = 'images_for_articles'
    for image_path in image_paths:
        # Create a directory named after the article ID
        directory_name = f"{article_id}"
        # Name the image using the article ID and the original file name
        destination_blob_name = f"{directory_name}/{os.path.basename(image_path)}"
        upload_blob(bucket_name, image_path, destination_blob_name)

    destination_blob_name = None

    for i, image_path in enumerate(image_paths):
        # Create a directory named after the article ID
        directory_name = f"{article_id}"
        # Name the image using the article ID and the original file name
        destination_blob_name = f"{directory_name}/slide_{i}.png"
        upload_blob(bucket_name, image_path, destination_blob_name)
        # Get the URL of the image
        image_url = get_image_url(bucket_name, destination_blob_name)
        # Replace the local image path with the URL in the markdown
        merged_md = merged_md.replace(image_path, image_url)

    thumbnail_url = get_image_url(bucket_name, destination_blob_name)  # Use your existing function

    # Write the merged markdown to a file
    
    with open("merged_output.md", "w") as f:
        f.write(merged_md)
    title = get_title_from_md_file("merged_output.md")    

    timestamp = datetime.now() + timedelta(hours=5.5)

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
    result = {'message': 'Processing completed!', 'article_id': article_id}
    print(json.dumps(result))