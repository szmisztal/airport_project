# Airport Project

## Project Description
The project is based on a client-server architecture, operating on sockets, where the server represents an airport, and each connecting client represents an airplane. The application operates automatically, simulating the operation of an airport. The server sends commands to clients based on their position and distance, directing them towards a safe landing. Every connection, collision between airplanes, and successful landing is recorded in a database. Visualization of airport traffic is implemented using the matplotlib library. Additionally, to facilitate interaction with the system and expand its functionality, an API using the Flask framework was implemented. This API allows for remote management of the server and monitoring of the airport's status, opening up new possibilities for further development and integration of the project.

## Features
- **Real-time Simulation:** Experience the dynamic operation of an airport with live updates and interactions between the server (airport) and clients (airplanes).
- **Command Dispatch:** The server intelligently issues commands to airplanes, ensuring their safe routing and landing based on their real-time positions and trajectories.
- **Comprehensive Logging:** Every significant event within the simulation, from aircraft movements to landings, is captured and stored for analysis and review.
- **Visual Insights:** Utilize matplotlib to gain a visual understanding of the airport's traffic, offering an intuitive representation of the simulation's complexity.
- **API Integration:** The Flask API introduces a new layer of interaction, allowing remote server management and real-time monitoring of the airport's operational status.

## Technologies Used
- **Python 3**: The backbone of the project, used for all primary development efforts.
- **Flask**: Empowers the API, facilitating seamless interaction and control over the simulation.
- **Threading**: Enables the system to handle multiple operations simultaneously, essential for real-time simulation and monitoring.
- **Matplotlib**: Provides the graphical capabilities to visualize the simulation, enhancing understanding and engagement.
- **NumPy**: Used for efficient numerical computations, particularly in processing and analyzing simulation data.

## System Requirements
- Python 3.x installed on your machine.
- Flask, for setting up the API.
- Matplotlib and NumPy, for data visualization and numerical operations.


## API Endpoints
Below is a list of available endpoints in the airport simulation system API:

### Start the Airport Server

- **Endpoint:** `/start`
- **Method:** GET
- **Description:** Starts the airport server process.
- **Response:** JSON response indicating that the server has started and its PID.

### Close the Airport Server

- **Endpoint:** `/close`
- **Method:** GET
- **Description:** Closes the airport server process.
- **Response:** JSON response indicating that the server has stopped.

### Pause the Airport Server Operations

- **Endpoint:** `/pause`
- **Method:** GET
- **Description:** Pauses the airport server operations.
- **Response:** JSON response indicating that the server is paused.

### Restore the Airport Server Operations

- **Endpoint:** `/restore`
- **Method:** GET
- **Description:** Resumes the airport server operations.
- **Response:** JSON response indicating that the server operations have been resumed.

### Get Server Uptime

- **Endpoint:** `/uptime`
- **Method:** GET
- **Description:** Provides the uptime of the airport server.
- **Response:** JSON response with the server uptime duration.

### Get All Airplanes

- **Endpoint:** `/airplanes`
- **Method:** GET
- **Description:** Retrieves the total number of airplanes.
- **Response:** JSON response with the total number of airplanes.

### Get Airplanes Collision Information

- **Endpoint:** `/collisions`
- **Method:** GET
- **Description:** Retrieves the list of airplanes that crashed due to running out of fuel and due to collision.
- **Response:** JSON response with the list of airplanes crashed by running out of fuel and by collision.

### Get Successfully Landed Airplanes

- **Endpoint:** `/landings`
- **Method:** GET
- **Description:** Retrieves the list of airplanes that landed successfully.
- **Response:** JSON response with the list of airplanes that had a successful landing.

### Get Airplanes Currently in the Air

- **Endpoint:** `/airplanes_in_the_air`
- **Method:** GET
- **Description:** Retrieves the list of airplanes that are currently in the air.
- **Response:** JSON response with the list of airplanes that are in the air.

### Get Specific Airplane Details

- **Endpoint:** `/airplanes/<int:airplane_id>`
- **Method:** GET
- **Description:** Retrieves details of a specific airplane by its ID.
- **Response:** JSON response with the details of the specified airplane or an error message if the airplane ID does not exist.