import cv2
import numpy as np
import os


def human_count():

    # Paths to the YOLO files
    yolo_weights = "yolov3.weights"
    yolo_config = "yolov3.cfg"
    yolo_names = "coco.names"

    # Check if files exist
    if not os.path.exists(yolo_weights):
        raise FileNotFoundError(f"YOLO weights file not found: {yolo_weights}")
    if not os.path.exists(yolo_config):
        raise FileNotFoundError(f"YOLO config file not found: {yolo_config}")
    if not os.path.exists(yolo_names):
        raise FileNotFoundError(f"COCO names file not found: {yolo_names}")

    # Load YOLO
    net = cv2.dnn.readNet(yolo_weights, yolo_config)
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    classes = []
    with open(yolo_names, "r") as f:
        classes = [line.strip() for line in f.readlines()]

    # Initialize video capture
    # cap = cv2.VideoCapture("human_count.mp4")
    # if not cap.isOpened():
    #     raise IOError("Cannot open video file")


    # Initialize video capture for webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    output_dir = "output_frames"
    os.makedirs(output_dir, exist_ok=True)
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("No more frames or error in reading frame")
            break

        height, width, channels = frame.shape

        # Detecting objects
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5 and classes[class_id] == "person":
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        human_count = 0
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                confidence = confidences[i]
                if label == "person":
                    human_count += 1
                    color = (0, 255, 0)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


        break
        # print(f"Human in the room: {human_count}")
        # cv2.putText(frame, f"Human Count: {human_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        # output_frame_path = os.path.join(output_dir, f"frame_{frame_count:04d}.jpg")
        # success = cv2.imwrite(output_frame_path, frame)
        # if success:
        #     print(f"Frame {frame_count} written to {output_frame_path}")
        # else:
        #     print(f"Failed to write frame {frame_count}")

        frame_count += 1

    cap.release()
    return human_count

human_count()