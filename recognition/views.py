import os
import cv2
import numpy as np
import tensorflow as tf
from moviepy.editor import VideoFileClip
from django.shortcuts import render
from django.http import JsonResponse
import uuid 
from datetime import datetime
from fitmind import settings

# Keypoint and edge definitions
KEYPOINT_DICT = {
    "nose": 0,
    "left_eye": 1,
    "right_eye": 2,
    "left_ear": 3,
    "right_ear": 4,
    "left_shoulder": 5,
    "right_shoulder": 6,
    "left_elbow": 7,
    "right_elbow": 8,
    "left_wrist": 9,
    "right_wrist": 10,
    "left_hip": 11,
    "right_hip": 12,
    "left_knee": 13,
    "right_knee": 14,
    "left_ankle": 15,
    "right_ankle": 16,
}

KEYPOINT_EDGE_INDS_TO_COLOR = {
    (0, 1): (255, 0, 255),
    (0, 2): (0, 255, 255),
    (1, 3): (255, 0, 255),
    (2, 4): (0, 255, 255),
    (0, 5): (255, 0, 255),
    (0, 6): (0, 255, 255),
    (5, 7): (255, 0, 255),
    (7, 9): (255, 0, 255),
    (6, 8): (0, 255, 255),
    (8, 10): (0, 255, 255),
    (5, 6): (255, 255, 0),
    (5, 11): (255, 0, 255),
    (6, 12): (0, 255, 255),
    (11, 12): (255, 255, 0),
    (11, 13): (255, 0, 255),
    (13, 15): (255, 0, 255),
    (12, 14): (0, 255, 255),
    (14, 16): (0, 255, 255),
}

def main(video_path):
    # Load model
    model = tf.lite.Interpreter(model_path="./models/movenet_singlepose_lightning.tflite")
    model.allocate_tensors()

    # Define path for output video file
    output_file_name = f"result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    output_file_path = os.path.join(settings.MEDIA_ROOT, "assets/output", output_file_name)

    # Load the video
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error opening video stream or file")
        return None

    # Get dimensions of frame
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    temp_output_path = os.path.join(settings.MEDIA_ROOT, "assets/output", f"temp_result_{uuid.uuid4()}.avi")
    out = cv2.VideoWriter(temp_output_path, fourcc, 20.0, (frame_width, frame_height))

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            img = frame.copy()
            img = tf.image.resize_with_pad(np.expand_dims(img, axis=0), target_height=192, target_width=192)
            img = tf.cast(img, dtype=tf.float32)

            input_details = model.get_input_details()
            output_details = model.get_output_details()

            model.set_tensor(input_details[0]["index"], np.array(img))
            model.invoke()
            keypoints_with_scores = model.get_tensor(output_details[0]["index"])

            draw_connections(frame, keypoints_with_scores, KEYPOINT_EDGE_INDS_TO_COLOR, 0.4)
            draw_keypoints(frame, keypoints_with_scores, confidence_threshold=0.4)

            out.write(frame)
        else:
            break

    cap.release()
    out.release()
    convert_to_mp4(temp_output_path, output_file_path)
    return output_file_name  # Return the output file name for URL construction

def draw_keypoints(frame, keypoints, confidence_threshold=0.5):
    y, x, _ = frame.shape
    new_keypoints = np.squeeze(np.multiply(keypoints, np.array([y, x, 1])))
    for keypoint in new_keypoints:
        ky, kx, kp_conf = keypoint
        if kp_conf > confidence_threshold:
            cv2.circle(frame, (int(kx), int(ky)), 3, (0, 255, 0), -1)

def draw_connections(frame, keypoints, edges, confidence_threshold=0.5):
    y, x, _ = frame.shape
    new_keypoints = np.squeeze(np.multiply(keypoints, np.array([y, x, 1])))

    for vertices, edge_color in edges.items():
        v1, v2 = vertices
        y1, x1, c1 = new_keypoints[v1]
        y2, x2, c2 = new_keypoints[v2]
        if (c1 > confidence_threshold) & (c2 > confidence_threshold):
            cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), edge_color, 2)

def convert_to_mp4(out_file_path: str, nw_out_file_path: str) -> None:
    clip = VideoFileClip(out_file_path)
    clip.write_videofile(nw_out_file_path)
    os.remove(out_file_path)

def upload_video(request):
    if request.method == 'POST':
        if 'video' in request.FILES:
            video = request.FILES['video']
            video_name = f"{uuid.uuid4()}_{video.name}"
            video_path = os.path.join(settings.MEDIA_ROOT, "assets/input/", video_name)
            os.makedirs(os.path.dirname(video_path), exist_ok=True)

            # Save the uploaded video to the input directory
            with open(video_path, 'wb+') as destination:
                for chunk in video.chunks():
                    destination.write(chunk)

            # Process the video and get the output video filename
            result_video_name = main(video_path)
            if result_video_name is None:
                return JsonResponse({'error': 'Error processing video.'}, status=500)

            # Construct the video URL based on MEDIA_URL and the output directory
            video_url = settings.MEDIA_URL + "assets/output/" + result_video_name

            feedback = "Pose correcte. Bravo!"  # Update this based on your evaluation logic
            return render(request, 'result.html', {'video_url': video_url, 'feedback': feedback})

        else:
            return JsonResponse({'error': 'No video provided.'}, status=400)

    return render(request, 'upload.html')
