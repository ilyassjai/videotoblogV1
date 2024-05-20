FROM python:3.8

# Layer caching for faster builds
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Copy the core_app code
COPY . /core_app
WORKDIR /core_app

# # Set the entry point for the core_app, if applicable
# # For example, if you have a script that needs to be run, specify it here
# CMD ["python3", "src/main.py"]
