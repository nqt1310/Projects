Ensure Docker is running on your machine.

Navigate to your project directory:

cd /path/to/your_project
Build the Docker images:

docker-compose build
Start the Docker containers:

docker-compose up
Access the web app:

Open your web browser and go to http://localhost:8000. This will serve the index.html file from the static directory.
To access the API endpoint, go to http://localhost:8000/search?q=your_query.
