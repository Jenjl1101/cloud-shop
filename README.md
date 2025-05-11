# CloudShop CLI Application

A command-line marketplace application that allows users to buy and sell items.

## Requirements

- Python 3.6 or higher

## Building

Run the build script to set up the environment:
```sh
./build.sh
```
The script will:
- Check for Python 3.6 or higher
- Create a virtual environment (`venv/`) if it does not exist
- Install required dependencies from `requirements.txt`
- Remove the existing `cloudshop.db` database file (if present)
- Ensure `cloudshop.py` and `run.sh` are executable

## Running

Before running, ensure the virtual environment has been set up by executing `build.sh`. Then, start the application using:
```sh
./run.sh
```
This will:
- Verify that the virtual environment (`venv/`) exists
- Activate the virtual environment
- Run `cloudshop.py`
- Deactivate the virtual environment upon exit

You can also process commands from a file:
```sh
cat commands.txt | ./run.sh
```
or use:
```sh
./run.sh < commands.txt | tee output.log
```
to write the STDIN to a file.

## 🐳 Build and Run with Docker

You can also use Docker to build and run this project, without manually running `build.sh`.

**Build the image:**
```sh
docker build -t cloudshop .
```

**Run the container:**
```sh
docker run -it cloudshop
```

**Run commands from a file:**
```sh
docker run -i cloudshop < commands.txt
```

**Mount a host folder to the container (e.g., to persist the database):**
```sh
docker run -it -v $(pwd):/app cloudshop
```

### Docker Image Tagging Logic

The Docker images for this project are tagged using the following logic:

- `latest`: This tag is used for the most recent successful build from the `main` branch. It represents the latest stable version of the application.
- `<commit-sha>`: Each build is also tagged with the first seven characters of the commit SHA. This allows you to reference a specific version of the application based on the exact state of the code at the time of the build.

These tags are automatically applied during the GitHub Actions workflow, which tests, builds, and pushes the Docker image to DockerHub. You can find the images on DockerHub under the repository `${{ secrets.DOCKERHUB_USERNAME }}/2025cloud`.

## Commands

The application supports the following commands:

| Command | Description | Usage |
|---------|-------------|-------|
| `REGISTER` | Create a new user account | `REGISTER <username>` |
| `CREATE_LISTING` | Create a new item listing | `CREATE_LISTING <username> <title> <description> <price> <category>` |
| `DELETE_LISTING` | Remove an existing listing | `DELETE_LISTING <username> <listing_id>` |
| `GET_LISTING` | View details of a specific listing. Username is taken just for authentication. | `GET_LISTING <username> <listing_id>` |
| `GET_CATEGORY` | View all listings in a category. Username is taken just for authentication. | `GET_CATEGORY <username> <category>` |
| `GET_TOP_CATEGORY` | Show the category with most listings. Username is taken just for authentication. | `GET_TOP_CATEGORY <username>` |

## Database

The application uses SQLite for data storage. The database file is created in the current directory as `cloudshop.db` and is reset each time `build.sh` is run.

## Notes


