# ------------------- Import
import cv2
import time

# ------------------- Create the CSRT tracker
def create_tracker():
    if hasattr(cv2, "TrackerCSRT_create"):
        return cv2.TrackerCSRT_create()
    elif hasattr(cv2, "legacy") and hasattr(cv2.legacy, "TrackerCSRT_create"):
        return cv2.legacy.TrackerCSRT_create()
    else:
        raise AttributeError("CSRT not found. Install opencv-contrib-python.")

# ------------------- Cam setup
def open_camera():
    cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION) # AVFoundation is the native backend for camera access

    if not cap.isOpened():
        cap = cv2.VideoCapture(0) # Fallback in case AVFoundation doesn't work

    return cap

# ------------------- Start of the Main function
def main():
    cap = open_camera()

    if not cap.isOpened():
        print("error: Could not open the webcam.")
        return

    time.sleep(2) # Giving the camera a second to warm up as it was displayig a black frame

# ------------------- Frame warm up
    frame = None
    for _ in range(20):
        ok, frame = cap.read()
        if ok and frame is not None and frame.size > 0:
            if frame.mean() > 5: # Ignore
                break
        time.sleep(0.05)

    if frame is None or frame.size == 0:
        print("error: Could not get a frame from the webcam.")
        cap.release()
        return

# ------------------- Preview 
    print(">>> Live preview started <<<")
    print("Press 's' to select an object.")
    print("Press 'q' to quit.")

    selected_frame = None

    # Live preview first
    while True:
        ok, frame = cap.read()
        if not ok or frame is None or frame.size == 0:
            print("error: Failed to read the frame.")
            break

        cv2.putText(
            frame,
            "Press 's' to select object | Press 'q' to quit",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2,
        )

        cv2.imshow("Live Preview", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("s"): # selecting 's' freezes the current frame so the user can select the ROI
            selected_frame = frame.copy()
            break
        elif key == ord("q"): # selecting 'q' quits
            cap.release()
            cv2.destroyAllWindows()
            return

    if selected_frame is None: # if null then distroy
        print("No frame selected.")
        cap.release()
        cv2.destroyAllWindows()
        return

# ------------------- ROI selection aka drawing a bounding box
    bbox = cv2.selectROI("Select Object", selected_frame, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow("Select Object")
    cv2.destroyWindow("Live Preview")

    if bbox == (0, 0, 0, 0):
        print("No bounding box selected")
        cap.release()
        cv2.destroyAllWindows()
        return

# ------------------- Initializing the tracker
    tracker = create_tracker()
    tracker.init(selected_frame, bbox) # this is where the tracker learns what to follow

    prev_time = time.time()

# ------------------- Tracker while loop
    while True:
        ok, frame = cap.read()
        if not ok or frame is None or frame.size == 0:
            print("error: Failed to read the frame.")
            break

        success, bbox = tracker.update(frame) # update the tracker with the new frame so it returns the new position of the object

# ------------------- Frames Per Second calculation
        current_time = time.time()
        fps = 1 / (current_time - prev_time) if current_time != prev_time else 0
        prev_time = current_time

# ------------------- Drawing results
        if success:
            x, y, w, h = [int(v) for v in bbox]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) # BRG, thickness
            cv2.putText(
                frame,
                "Tracking", # text
                (x, y - 10), # position of text
                cv2.FONT_HERSHEY_SIMPLEX, # font
                0.7, # scale
                (0, 255, 0), # green
                2, # thickness
            )
        else:
            cv2.putText(
                frame,
                "Tracking Failed", # text
                (20, 60), # position of text
                cv2.FONT_HERSHEY_SIMPLEX, # font
                0.9, # scale
                (0, 0, 255), # red
                2, # thickness
            )

        cv2.putText(
            frame,
            f"FPS: {fps:.2f}", # text
            (20, 95), # position of text
            cv2.FONT_HERSHEY_SIMPLEX, # font
            0.8, # scale
            (255, 0, 0), # blue
            2, # thickness
        )
        cv2.putText(
            frame,
            "Press 'q' to quit", # text
            (20, 130), # position of text
            cv2.FONT_HERSHEY_SIMPLEX, # font
            0.8, # scale
            (255, 255, 255), # black
            2, # thickness
        )
# ------------------- Ending it all
        cv2.imshow("Real-Time Object Tracker", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"): # exit when user presses 'q'
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()