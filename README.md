# Polygrid Drone Flying Path Generator


This project provides an API endpoint for generating a polygonal grid drone flying path considering various camera specifications and flight parameters. The generated path consists of waypoints represented as a LineString geometry, along with the time interval between two consecutive photos based on the vertical overlap specified by the user. Additionally, the application saves the generated waypoints in KML, GeoJSON, and Litchi-compatible CSV files.

## Features
Generate drone flying path based on camera specifications and flight parameters.
Specify field of view (FOV),image width, and height.
Set altitude of flight and overlap percentage (horizontal and vertical).
Define area of interest (AOI) using GeoJSON polygon.
Returns waypoints represented as a LineString geometry with time interval between photos.
Save generated waypoints in KML, GeoJSON, and Litchi-compatible CSV files.
## Getting Started

### Prerequisites

- Python 3.10+
- FastAPI
- Pydantic
- Uvicorn
- GeoPandas
- Shapely

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/T-Aman19/DroneMissionPlanner.git
   ```

2. Navigate to the project directory:

   ```bash
   cd DroneMissionPlanner
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Usage

1. Start the FastAPI server:

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 7000
   ```

2. Open your browser and navigate to `http://localhost:7000/docs` to access the Swagger UI.
   
3. Use the provided endpoint `/mission` to generate drone flying path by providing the required parameters.

## API Endpoint

- Endpoint: `http://localhost:7000/mission`
- Method: POST
- Request Body:

  ```json
  {
    "FOV": 84,
    "AOI": {
      "type": "Polygon",
      "coordinates": [
        [
          [77.395034, 28.49966],
          [77.395077, 28.494889],
          [77.401257, 28.495247],
          [77.401085, 28.498302],
          [77.395034, 28.49966]
        ]
      ]
    },
    "ImageHeight": 6000,
    "ImageWidth": 8000,
    "Overlap": 80,
    "Altitude": 100,
    "Speed": 15
  }
  ```

- Response Body:

  ```json
  {
    "type": "Feature",
    "properties": {},
    "geometry": {
      "type": "LineString",
      "coordinates": [
        [77.395034, 28.49966],
        [77.401085, 28.498302],
        [77.40102193410102, 28.498020989871378],
        ...
      ]
    }
  }
  ```

## Contributors

- T-Aman19(https://github.com/T-Aman19)

## License

This project is licensed under the [MIT License](LICENSE).
