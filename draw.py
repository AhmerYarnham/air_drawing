import cv2
from ahmercv import HandTracker

# Setup
cap = cv2.VideoCapture(0)
tracker = HandTracker(max_hands=1, detection_confidence=0.8)

canvas = None
prev_x, prev_y = 0, 0
drawing = False

while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)

    if canvas is None:
        canvas = frame.copy() * 0

    # Detect hands using ahmercv
    hands, frame = tracker.find_hands(frame)

    if hands and drawing:
        x, y = tracker.get_finger_position(hands, finger=8)

        if prev_x == 0 and prev_y == 0:
            prev_x, prev_y = x, y

        cv2.line(canvas, (prev_x, prev_y), (x, y), (0, 255, 0), 5)
        prev_x, prev_y = x, y
    else:
        prev_x, prev_y = 0, 0

    combined = cv2.addWeighted(frame, 0.7, canvas, 0.3, 0)

    status = "DRAWING" if drawing else "NOT DRAWING"
    cv2.putText(combined, f"SPACE=draw toggle | C=clear Q=quit | {status}",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow("Air Drawing", combined)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    if key == ord('c'):
        canvas = frame.copy() * 0
    if key == ord(' '):
        drawing = not drawing

cap.release()
cv2.destroyAllWindows()