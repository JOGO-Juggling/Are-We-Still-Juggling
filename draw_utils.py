import cv2

def draw_frame(frame, ball, body):
    '''Get a frame with ball and body data as input, and display in ocv window'''
    color = (0, 0, 255)

    # Add ball if information is given
    if ball != {}:
        x, y = ball['x'], ball['y']
        w, h = ball['width'], ball['height']
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
    
    # Add body if information is given
    if body != {}:
        right_foot, left_foot = body['RAnkle'], body['LAnkle']
        if right_foot != {}:
            x, y = int(right_foot['x']), int(right_foot['y'])
            frame = cv2.circle(frame, (x, y), 5, color, 2)
        
        if left_foot != {}:
            x, y = int(left_foot['x']), int(left_foot['y'])
            frame = cv2.circle(frame, (x, y), 5, color, 2)
    
    # Draw and return frame
    cv2.imshow('Are We Still Juggling?', frame)
    return frame
