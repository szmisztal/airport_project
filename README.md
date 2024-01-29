# Airport Project

## Project Description
Project based on the Server-Client architecture, working with sockets, where the server represents an airport and each connecting client represents an airplane. The application operates automatically, simulating airport operations. The server sends commands to clients based on their position and distance, directing them towards safe landing. Each connection, collision between airplanes, and successful landing are recorded in a database. Visualization of airport traffic is achieved using the matplotlib library.

## Technologies Used
- **Python 3**: The primary programming language used for implementing the project.
- **Threading**: Utilized for handling multiple tasks concurrently, including monitoring aircraft traffic and managing them.
- **Matplotlib**: A Python library used for creating plots, utilized for visualizing aircraft positions at the airport.

## System Requirements
- Python 3.x
- Libraries: Matplotlib, NumPy

## Running the Project
1. Clone the repository to your local machine: `git clone https://github.com/your-repository.git`
2. Navigate to the project directory: `cd AirportManagementSystem`
3. Start the server: `python server.py`
4. Launch the client (aircraft): `python client.py`
