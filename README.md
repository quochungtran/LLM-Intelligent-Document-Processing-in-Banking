Intelligence 

# Create python virtual enviroment

python -m venv .venv

source .venv/bin/activate

deactivate

# Install dependencies

pip install -r backend/requirements.txt
pip install -r backend/requirements_vector_db.txt

# Set up chatbot project
docker network create internal-network

