import cv2
import numpy as np
#modify and download the cfg,weight,names file before running the file
def real_time_object_detection():
    config_file = r"\yolo_files\yolov4.cfg"
    weights_file = r"\yolo_files\yolov4.weights"
    classes_file = r"\yolo_files\custom_classes.names"  # Custom classes

    # Load the YOLO model
    net = cv2.dnn.readNet(weights_file, config_file)

    # Load class labels
    with open(classes_file, 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    # Start video capture (0 for the default camera)
    video = cv2.VideoCapture(0)

    if not video.isOpened():
        print("Error: Could not open video.")
        return

    while True:
        ret, frame = video.read()
        if not ret:
            print("Error: Failed to capture video frame.")
            break

        # Prepare the frame for detection
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)

        layer_names = net.getLayerNames()
        unconnected_out_layers = net.getUnconnectedOutLayers()
        output_layers = [layer_names[i - 1] for i in unconnected_out_layers]

        outs = net.forward(output_layers)

        # Process the outputs and draw bounding boxes
        class_ids, confidences, boxes = [], [], []
        height, width, _ = frame.shape

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.25:
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
        mobile_detected = False  # Flag to track mobile detection
        detected_model = None  # To store detected mobile model

        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = classes[class_ids[i]]  # Use custom class label
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, label, (x, y + 30), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

                # Check if the detected object is a mobile device
                if label == "cell phone":  # Assuming 'cell phone' is one of your custom classes
                    detected_model = label  # Store detected model name
                    mobile_detected = True  # Set flag if mobile device is detected

        cv2.imshow("Real-Time Object Detection", frame)

        if mobile_detected:
            print(f"{detected_model} detected")  # Output message to terminal
            break  # Exit the loop

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    real_time_object_detection()
