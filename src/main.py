from utils import *
from whisper import *
from llm import *
from youtubeAPI import *
from langchain_openai import ChatOpenAI
import os
import glob
from dotenv import load_dotenv




if __name__ == "__main__":
    load_dotenv()

    url = 'https://www.youtube.com/watch?v=Fk1gXKbcMo0'
    os.environ['OPENAI_API_KEY'] = 'sk-proj-UDfHlTwwCvVi9IbX0laOT3BlbkFJUDCLXgNqtUgJQkPp7ypb'
    openai_api_key = os.getenv('OPENAI_KEY')

    image_paths = [file for file in glob.glob(os.path.join('./slidemse', '*.png'))]    
    md_paths = [f"output{i}.md" for i in range(len(image_paths))]

    #start
    llm = ChatOpenAI(openai_api_key=openai_api_key,model="gpt-3.5-turbo",temperature=0.5)
    df_slides=videotodataframe(url)
    chat(llm,df_slides)
    merged_md = merge_markdown_with_images(md_paths, image_paths)

    with open("merged_output.md", "w") as f:
        f.write(merged_md)
