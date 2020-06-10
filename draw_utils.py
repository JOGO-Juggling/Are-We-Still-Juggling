import cv2

def draw_frame(frame, ball, body, ball_dy):
    '''Get a frame with ball and body data as input, and display in ocv window'''
    color = (0, 0, 255)

    # Add ball if information is given
    if ball != {}:
        x, y = ball['x'], ball['y']
        w, h = ball['width'], ball['height']
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 1)

        # Set vector color
        v_color = color
        if ball_dy < 0:
            v_color = (0, 255, 0)
        
        # Draw vector
        ball_dy *= 5
        vec_x, vec_y = int(x + .5 * w), int(y + .5 * h)
        frame = cv2.arrowedLine(frame, (vec_x, vec_y), (vec_x, vec_y + ball_dy), v_color, 4)
    
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
