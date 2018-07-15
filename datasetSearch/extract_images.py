import cv2

from glob import glob


def frame_capture(vid_file):
    cap = cv2.VideoCapture(vid_file)
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_count = 0
    print("getting {} images".format(num_frames))
    try:
        while True:
            ret, frame = cap.read()
            cv2.imshow("frame1", frame)
            cv2.imwrite("../images/{}_{}.jpg".format(vid_file, frame_count), frame)
            frame_count += 1
            if ret == False:
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                break
    except:
        print("got {} images out of {}".format(frame_count, num_frames))

video_files = glob("../videos/*.MOV")
print(video_files)

for i in range(len(video_files)):
    print("processing video:{}".format(video_files[i]))
    try:
        frame_capture(video_files[i])
    except:
        break
cv2.destroyAllWindows()
