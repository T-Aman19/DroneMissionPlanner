import csv
from typing import List
from shapely import Polygon, Point, LineString
import geopandas as gpd
def find_greatest_vertex(lat, lon, polygon_coords):
    # Create a Polygon from the provided coordinates
    polygon = Polygon(polygon_coords)

    # Create a Point from the given lat lon
    given_point = Point(lon, lat)

    # Calculate distances between given point and each vertex of the polygon
    distances = [
        given_point.distance(Point(coord)) for coord in polygon.exterior.coords[:-1]
    ]

    # Find the vertex with maximum distance
    max_distance_index = distances.index(max(distances))
    max_distance_vertex = polygon.exterior.coords[max_distance_index]

    # Find indices of adjacent vertices
    previous_index = (
        max_distance_index - 1
        if max_distance_index > 0
        else len(polygon.exterior.coords) - 1
    )
    next_index = (max_distance_index + 1) % len(polygon.exterior.coords)

    # Calculate distances between given point and adjacent vertices
    previous_distance = given_point.distance(
        Point(polygon.exterior.coords[previous_index])
    )
    next_distance = given_point.distance(Point(polygon.exterior.coords[next_index]))

    # Determine the vertex with the greater distance among adjacent vertices
    if previous_distance > next_distance:
        max_adjacent_vertex = polygon.exterior.coords[previous_index]
    else:
        max_adjacent_vertex = polygon.exterior.coords[next_index]

    return max_adjacent_vertex



def clip_linestrings_with_polygon_bounds(polygon_geometry, linestrings_list):
    polygon_gdf = gpd.GeoDataFrame(geometry=[polygon_geometry])

    clipped_linestrings = []
    intersecting_points = []
    for linestrings_df in linestrings_list:
        # Iterate over each linestring in the GeoDataFrame
        clipped = gpd.clip(linestrings_df, polygon_gdf)

        # Iterate over each geometry in the clipped GeoDataFrame
        for geom in clipped.geometry:
            if geom.geom_type == "MultiLineString":
                for line in geom.geoms:
                    coords = list(line.coords)
                    if len(intersecting_points) == 0:
                        intersecting_points.extend(map(Point, coords))
                    else:
                        # Check the direction of the line
                        first_coord = line.coords[0]
                        last_coord = line.coords[-1]
                        if Point(first_coord).distance(
                            Point(intersecting_points[-1].coords)
                        ) < Point(last_coord).distance(
                            Point(intersecting_points[-1].coords)
                        ):
                            intersecting_points.extend(map(Point, coords))
                        else:
                            intersecting_points.extend(map(Point, reversed(coords)))
            elif geom.geom_type == "LineString":
                coords = list(geom.coords)
                if len(intersecting_points) == 0:
                    intersecting_points.extend(map(Point, coords))
                else:
                    # Check the direction of the line
                    first_coord = geom.coords[0]
                    last_coord = geom.coords[-1]
                    # print(
                    #     f"first_coord:{first_coord} last_coord:{last_coord}, last insertecting points: {intersecting_points[-1]}"
                    # )
                    # print(
                    #     f"distance from first_coord:{Point(first_coord).distance(Point(intersecting_points[-1].coords))}, second_coord: {Point(last_coord).distance(Point(intersecting_points[-1].coords))}"
                    # )
                    if Point(first_coord).distance(
                        Point(intersecting_points[-1].coords)
                    ) < Point(last_coord).distance(
                        Point(intersecting_points[-1].coords)
                    ):
                        intersecting_points.extend(map(Point, coords))
                    else:
                        intersecting_points.extend(map(Point, reversed(coords)))
        # for idx, row in clipped.iterrows():
        #     points = list(row.geometry.coords)
        #     first_coord = points[0]
        #     last_coord = points[-1]
        #     print(f'first_coord:{first_coord} last_coord:{last_coord}, last insertecting points: {intersecting_points[-1]}')
        #     print(f'distance from first_coord:{Point(first_coord).distance(Point(intersecting_points[-1].coords))}, second_coord: {Point(last_coord).distance(Point(intersecting_points[-1].coords))}')
        #     if Point(first_coord).distance(
        #         Point(intersecting_points[-1].coords)
        #     ) > Point(last_coord).distance(
        #         Point(intersecting_points[-1].coords)
        #     ):
        #         intersecting_points.extend(map(Point, points))
        #     else:
        #         intersecting_points.extend(map(Point, reversed(points)))

    return clipped_linestrings, intersecting_points


def write_waypoints_to_csv(filename, waypoints, altitude, photo_time_interval):
    """
    Write waypoints to a CSV file.

    :param waypoints: List of (latitude, longitude) tuples representing the waypoints.
    :param altitude: Altitude for each waypoint.
    :param filename: Name of the CSV file to write.
    """
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(
            [
                "latitude",
                "longitude",
                "altitude(m)",
                "heading(deg)",
                "curvesize(m)",
                "rotationdir",
                "gimbalmode",
                "gimbalpitchangle",
                "actiontype1",
                "actionparam1",
                "actiontype2",
                "actionparam2",
                "altitudemode",
                "speed(m/s)",
                "poi_latitude",
                "poi_longitude",
                "poi_altitude(m)",
                "poi_altitudemode",
                "photo_timeinterval",
                "photo_distinterval",
            ]
        )
        # Write each waypoint
        for waypoint in waypoints:
            # print(type(waypoint))
            # print(waypoint.xy)
            writer.writerow(
                [
                    list(waypoint.xy[1])[0],
                    list(waypoint.xy[0])[0],
                    altitude,
                    0.00,
                    0.20,
                    0.00,
                    2.00,
                    -90.00,
                    -1.00,
                    0.00,
                    -1.00,
                    0.00,
                    0.00,
                    12.00,
                    0.00,
                    0.00,
                    0.00,
                    0.00,
                    -1.00,
                    -1.00,
                ]
            )
    print("csv generated successfully")


def waypoints_to_json(waypoints: List[Point], filename):
    import json

    json_data = []
    for point in waypoints:
        json_data.append({"lat": point.x, "lng": point.y})
    with open(filename, "w") as file:
        file.write(json.dumps(json_data))


def write_waypoints_to_kml(filename, waypoints, altitude):
    print(f"len(waypoints): {len(waypoints)}")
    with open(filename, "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
        f.write("<Document>\n")
        f.write("<name>Flight Mission</name>\n")

        # Add LineString for flight path
        f.write("<Placemark>\n")
        f.write("<name>Flight Path</name>\n")
        f.write("<LineString>\n")
        f.write("<coordinates>\n")
        f.write(
            " ".join(
                [f"{waypoint.x},{waypoint.y},{altitude}" for waypoint in waypoints]
            )
        )  # Exclude the first waypoint
        f.write("\n</coordinates>\n")
        f.write("</LineString>\n")
        f.write("</Placemark>\n")

        # Add Placemarks for waypoints, excluding the first one
        # for i, waypoint in enumerate(waypoints):
        #     f.write(f'<Placemark>\n<name>Waypoint {i}</name>\n')
        #     f.write('<Point>\n<coordinates>\n')
        #     f.write(f'{waypoint.x},{waypoint.y},0\n')
        #     f.write('</coordinates>\n</Point>\n</Placemark>\n')

        f.write("</Document>\n")
        f.write("</kml>\n")


def waypoints_to_linestring(waypoints):
    linestring = LineString(waypoints)
    return {
        "type": "Feature",
        "properties": {},
        "geometry": {
            "type": "LineString",
            "coordinates": list(linestring.coords)
        }
    }

