import os

os.environ["OPENAI_API_KEY"] = "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"

# Set the PYTHONPATH environment variable
current_directory = os.getcwd()  # equivalent to $(pwd)
src_directory = os.path.join(current_directory, "src")
os.environ["PYTHONPATH"] = f"{src_directory}:{os.environ.get('PYTHONPATH', '')}"

# os.environ["GOOGLE_API_KEY"] = 
