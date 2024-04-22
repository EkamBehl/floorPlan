from ultralytics import YOLO
import numpy as np

async def getBoundingBox(image: np.ndarray) -> list[dict]:
    model = YOLO('./last.pt')  # Ensure this points to your actual model
    device = "cpu"
    
    results = model.predict(image, conf=0.01, device=device)
    
    # Initialization
    structured_objects = []
    boxes = results[0].cpu().numpy().boxes
    names = results[0].cpu().numpy().names

    # Separating detected objects by their classes
    walls = []
    doors = []
    windows = []

    for i in range(len(boxes.cls)):
        detected_object = {
            'class': names[int(boxes.cls[i])],
            'confidence': float(boxes.conf[i]),
            'coords': boxes.xyxy[i].tolist()  # Convert ndarray to list
        }
        
        if detected_object['class'] == 'wall':
            walls.append(detected_object)
        elif detected_object['class'] == 'door':
            doors.append(detected_object)
        elif detected_object['class'] == 'window':
            windows.append(detected_object)

    # Associating doors and windows with the nearest wall
    for wall in walls:
        # Initialize nested structure for each wall
        wall['associated_doors'] = []
        wall['associated_windows'] = []
        
        for door in doors:
            # Assuming a function `is_near` to determine if a door is near the wall
            if is_near(door['coords'], wall['coords']):
                wall['associated_doors'].append(door)
        
        for window in windows:
            # Assuming the same for windows
            if is_near(window['coords'], wall['coords']):
                wall['associated_windows'].append(window)
        
        structured_objects.append(wall)

    print(structured_objects)
    
    return structured_objects

def is_near(obj_coords, wall_coords):
    """
    Basic function to determine if an object is near a wall.
    This example uses a simple proximity check.
    """
    # Example condition to check proximity (this is oversimplified and needs refinement)
    # Let's say if the center of an object is within a certain distance of the wall's center, they are considered 'near'.
    obj_center = ((obj_coords[0] + obj_coords[2]) / 2, (obj_coords[1] + obj_coords[3]) / 2)
    wall_center = ((wall_coords[0] + wall_coords[2]) / 2, (wall_coords[1] + wall_coords[3]) / 2)

    # Define a simple distance threshold (this is arbitrary and for illustration)
    distance_threshold = 50  # Adjust based on your scale

    distance = np.sqrt((obj_center[0] - wall_center[0]) ** 2 + (obj_center[1] - wall_center[1]) ** 2)
    return distance < distance_threshold

def box_to_dict(box):
    return {
        "x": box.x,
        "y": box.y,
        "width": box.w,
        "height": box.h,
        "confidence": box.confidence,
        "class": box.cls
    }


