# Create 'internal-network' if it does not exist
echo "==== CREATING DOCKER NETWORK 'internal-network' ===="
if ! docker network ls | grep -q "internal-network"; then
    docker network create internal-network
    echo "Network 'internal-network' created successfully."
else
    echo "Network 'internal-network' already exists."
fi

# Run Docker Compose to start the containers
echo "==== STARTING DOCKER CONTAINERS ===="
docker compose up -d

echo "==== DOCKER SETUP COMPLETE ===="
docker ps  # Show running containers