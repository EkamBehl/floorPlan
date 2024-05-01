
from ultralytics import YOLO

import numpy as np

from scipy.signal import savgol_filter
from sklearn.linear_model import RANSACRegressor

def negate_y_axis(coords):
    # coords is a list of [x, y] coordinates
    negated_coords = [[x, -y] for [x, y] in coords]
    return negated_coords


def find_most_isolated_corner_and_opposite(bbox, mask_coords):
    [x1, y1, x2, y2] = bbox
    bbox_corners = np.array([
        [x1, y1],  # top-left
        [x2, y1],  # top-right
        [x2, y2],  # bottom-right
        [x1, y2]   # bottom-left
    ])

    # Track the maximum of minimum distances
    max_min_distance = 0
    most_isolated_corner_index = -1

    # Iterate through each corner to find the minimum distance to the mask points
    for i, corner in enumerate(bbox_corners):
        min_distance = np.min(np.sqrt((mask_coords[:, 0] - corner[0]) ** 2 + (mask_coords[:, 1] - corner[1]) ** 2))
        # Check if this minimum distance is the greatest found so far
        if min_distance > max_min_distance:
            max_min_distance = min_distance
            most_isolated_corner_index = i

    if most_isolated_corner_index == -1:
        return None, None  # In case no corner is sufficiently isolated

    # Calculate the index for the next corner clockwise
    next_corner_index = (most_isolated_corner_index) % 4
    # Calculate the index for the opposite corner to the next corner
    opposite_of_next_index = (next_corner_index + 2) % 4

    # Return the next corner and the opposite corner to the next corner
    return [bbox_corners[next_corner_index], bbox_corners[opposite_of_next_index]]

def find_closest_wall_coord(corner, wall_coords):
    if not wall_coords:
        return None

    min_distance = np.inf
    closest_point = None

    corner = np.array(corner)  # Ensure corner is a NumPy array for vector operations

    # Iterate through each wall's segments
    for wall in wall_coords:
        for segment in wall:
            p1, p2 = map(np.array, segment)  # Convert segment points to NumPy arrays

            # Vector from p1 to p2 and from p1 to corner
            p2_p1 = p2 - p1
            p0_p1 = corner - p1

            # Project point onto the line segment
            t = np.dot(p0_p1, p2_p1) / np.dot(p2_p1, p2_p1)
            t = np.clip(t, 0, 1)  # Ensure t is within the valid range of the segment

            # Calculate the closest point on the segment
            closest = p1 + t * p2_p1
            distance = np.linalg.norm(closest - corner)

            if distance < min_distance:
                min_distance = distance
                closest_point = closest
    print("closest point: ",closest_point)
    return closest_point.tolist() if closest_point is not None else None


def ChangeName(name):
    if(name=='wwaall'):
        name='wall'
    elif(name=='door'):
        name='door'
    else:
        name='wall'
    return name
async def getBoundingBox(image: np.ndarray) -> list[dict]:
    # Load a pretrained YOLOv8 model
    model = YOLO('./best2.pt')
    device = "cpu"
    
    # Run inference on the image
    results = model.predict(image, conf=0.1, device=device)
    
    wall_objects = []
    wall_coords=[]
    boxes = results[0].cpu().numpy().boxes
    names = results[0].cpu().numpy().names
    masks = results[0].masks

    for i in range(len(boxes.cls)):
        class_name = ChangeName(names[int(boxes.cls[i])])
        coords = masks[i].xy[0]
        if(class_name=="wall"):
             if isinstance(coords, np.ndarray):
                coords = coords.tolist()
       
                wall_coords.append(coords)
                wall_objects.append({
                    'class': class_name,
                    'coords': coords
                })
    for i in range(len(boxes.cls)):
        class_name = ChangeName(names[int(boxes.cls[i])])
        coords = masks[i].xy[0]
        if(class_name=="door"):
        # Ensure door coordinates are processed by getDoorPts and converted to list format
            bboxcorners=boxes.xyxy[i].tolist()

            door_coords = find_most_isolated_corner_and_opposite(bboxcorners,coords)
            door_coords = [coord.tolist() if isinstance(coord, np.ndarray) else coord for coord in door_coords]
            print("wall coordinates length",len(wall_coords))
        
           
            wall_coordinate=find_closest_wall_coord(door_coords[1],wall_coords)
            print("wall coordinate",wall_coordinate)
            doorCoords=[door_coords[0],wall_coordinate]
            wall_objects.append({
                'class': class_name,
                'coords': doorCoords
            })
    
           

    return wall_objects


# # Loop through each result
#     for result in results:
#         for mask in result.masks:
#             wall_objects.append({
#                 'class':'wall',
#                 'coords':mask.xy[0]
#             })
#     print("--------------------------------------")
#     print(wall_objects)
#     print("----------------------------------")
#     return wall_objects