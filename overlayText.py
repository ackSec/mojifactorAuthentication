import cv2
import numpy as np
import time

def overlay_text(image, text, org, font_scale, color, thickness):
    # Convert the image to RGB format and get the image dimensions
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    h, w = image.shape[:2]

    # Define the text position and font
    (text_width, text_height), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
    x = int((w - text_width) / 2)
    y = int((h + text_height) / 2)
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Draw the text on the image
    cv2.putText(image, text, (x, y), font, font_scale, color, thickness)

    # Convert the image back to BGR format and return it
    return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

def countdown_timer(image, detected_emoji):
    # Define the countdown timer text positions and font
    font_scale = 20
    color = (255, 0, 0)
    thickness = 30

    # Start the countdown timer
    for i in range(5, 0, -1):
        # Update the countdown timer text
        text = str(i)
        image = overlay_text(image, text, (0, 200), font_scale, color, thickness)

        # Show the image with the updated text
        cv2.imshow("Video Stream", image)
        cv2.waitKey(1000)

    # Overlay the detected emoji on the image
    image = overlay_text(image, detected_emoji, (0, 200), font_scale, color, thickness)

    # Return the image after the countdown timer finishes
    return image
