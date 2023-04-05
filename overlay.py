import cv2

def overlay_text(frame, text, pos):
    """
    Overlay text onto a video frame at a specified position.
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    color = (255, 255, 255)
    thickness = 2
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    text_pos = (pos[0] - text_size[0] // 2, pos[1] + text_size[1] // 2)
    cv2.putText(frame, text, text_pos, font, font_scale, color, thickness, cv2.LINE_AA)
    
def overlay_countdown(frame, countdown, pos):
    """
    Overlay a countdown timer onto a video frame at a specified position.
    """
    text = str(countdown)
    overlay_text(frame, text, pos)
