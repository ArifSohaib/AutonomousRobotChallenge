import cv2

from glob import glob
import os

def frame_capture(vid_file, label):
    cap = cv2.VideoCapture(vid_file)
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    file_name_idx = vid_file.find(label)+1
    print("label:{}".format(label))
    print(file_name_idx)
    file_name = vid_file[file_name_idx+len(label):]
    file_name = file_name[:-4]
    print("file_name:{}".format(file_name))
    frame_count = 0
    print("getting {} images".format(num_frames))
    try:
        while True:
            ret, frame = cap.read()
            cv2.imshow("frame1", frame)
            cv2.imwrite("./images/{}/{}_{}.jpg".format(label,file_name, frame_count), frame)
            #uncomment for debugging
            # print(os.path.abspath("./images/{}/{}_{}.jpg".format(label,file_name, frame_count)))
            frame_count += 1
            if ret == False:
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                break
    except:
        print("got {} images out of {}".format(frame_count, num_frames))
video_labels = glob("./videos/*")

for lbl in video_labels:
    label = lbl[9:]
    print(label)
    video_files = glob("./videos/{}/*.MOV".format(label))
    print(video_files)
    print("extracting {}".format(label))
    print("abs path: {}".format(os.path.abspath(lbl)))
    if not os.path.exists("./images/{}".format(label)):
        os.mkdir("./images/{}".format(label))
    for i in range(len(video_files)):
        print("processing video:{}".format(video_files[i]))
        frame_capture(video_files[i], label)

cv2.destroyAllWindows()
