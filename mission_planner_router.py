from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import schema, math, geopandas as gpd
from shapely import Polygon, LineString
import utils


mission_planner_router = APIRouter()


@mission_planner_router.post("/mission")
async def get_waypoints_for_AOI(data: schema.MissionParameters, req: Request):

    fov = float(data.FOV) * (3.14 / 180)  # Convert to radians
    image_height = data.ImageHeight
    image_width = data.ImageWidth
    overlap = data.Overlap
    r = image_width / image_height
    drone_speed = data.Speed
    polygon_coords = data.AOI['coordinates']
    alt= data.Altitude

    D = (
        2 * int(alt) * math.tan((float(fov)) / 2)
    )  # Diagonal of the drone image
    D = round(D, 2)
    sideA = float(D) * r / (math.sqrt(1 + (r**2)))  # side A of the drone image
    sideA = round(sideA, 2)  # width
    sideB = float(sideA) / r  # side B of the drone image #height
    sideB = round(sideB, 2)
    area = round((sideA * sideB), 2)  # area of the drone image
    gsd = round(
        math.sqrt(area / (int(image_height) * int(image_width))), 4
    )  # ground sampling distance

    x = float(overlap) / 100

    new_image_dist = round(((1 - x) * int(image_height) * gsd), 3)
    time_interval = math.floor(new_image_dist / drone_speed)  # seconds

    dist = round(
        ((1 - x) * int(image_width) * gsd), 3
    )  # distance between gridlines to maintain overlap percentage
    offset_distance = dist * 0.00001  # Offset distance in meters
    print(
        f"gsd: {gsd},fov:{fov} sideA: {sideA}, sideB: {sideB}, area: {area}, new_image_dist: {new_image_dist}, time interval: {time_interval}"
    )
    print(
        f"dist: {dist}, offset distance: {offset_distance}, time interval: {time_interval}"
    )

    polygon = Polygon(polygon_coords)
    perimeter = polygon.length
    left_top = polygon_coords[0]
    greatest_vertex = utils.find_greatest_vertex(left_top[0], left_top[1], polygon_coords)
    print(f"greatest_vertex: {greatest_vertex}")
    outer_line_coords = [left_top, greatest_vertex]
    outer_line = LineString(outer_line_coords)
    count = int(perimeter / (offset_distance))

    offsets = []
    offsets.append(gpd.GeoDataFrame(geometry=[outer_line]))
    for i in range(1, count):
        offset_line = outer_line.offset_curve(-(i * offset_distance))
        offsets.append(gpd.GeoDataFrame(geometry=[offset_line]))
        offset_line = outer_line.offset_curve((i * offset_distance))
        offsets.append(gpd.GeoDataFrame(geometry=[offset_line]))
    clipped_offsets, waypoints = utils.clip_linestrings_with_polygon_bounds(
        polygon_geometry=polygon, linestrings_list=offsets
    )
    utils.write_waypoints_to_csv(filename='small.csv', waypoints=waypoints, altitude=alt, photo_time_interval=time_interval)
    utils.write_waypoints_to_kml("small.kml", waypoints=waypoints, altitude=alt)


    return JSONResponse(content=utils.waypoints_to_linestring(waypoints))
