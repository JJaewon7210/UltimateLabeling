import cv2
import os

VIDEO_PATH  = 'D:/Construction_Video/Data/video/'
OUTPUT_PATH = 'D:/Construction_Video/Data/rgb-images/'

def video_to_frames(input_file: str, output_dir):
    """Function to extract frames from input video file
    and save them as separate frames in an output directory.
    Args:
        input_file: Input video file. (end with ".mp4")
        output_dir: Output directory to save the frames.
    Returns:
        None
    Example:
        input_file = 'D:/Construction_Video/Data/video/-ngh7-0TYmE_000013.mp4'
        output_dir = 'D:/Construction_Video/Data/rgb-images/-ngh7-0TYmE_000013/'
    """
    try:
        os.mkdir(output_dir)
    except OSError:
        pass
    # name of video
    video_name = input_file.replace('.mp4','').split('/')[-1]
    # Start capturing the feed
    cap = cv2.VideoCapture(input_file)
    # Find the number of frames
    video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    count = 0
    print ("Name of video: ", video_name)
    print ("Number of frames: ", video_length)
    # Start converting the video
    while cap.isOpened():
        # Extract the frame
        ret, frame = cap.read()
        if not ret:
            continue
        # Write the results back to output location.
        output_file = '{}/{:05d}.jpg'.format(output_dir,count)
        # output_dir + +"/" + video_name + "_%#05d.jpg" % (count+1)
        cv2.imwrite(output_file, frame)
        count = count + 1
        # If there are no more frames left
        if (count > (video_length-1)):
            # Release the feed
            cap.release()
            # Print stats
            print ("Done extracting frames.\n%d frames extracted" % count)
            print("--"*20)
            break

if __name__=="__main__":
    for video_file in os.listdir(VIDEO_PATH):
        if '.mp4' in video_file:
            video_name = video_file.replace('.mp4','').split('/')[-1]
            output_dir = '{}/{}/'.format(OUTPUT_PATH,video_name)
            input_file = VIDEO_PATH + video_file
            video_to_frames(input_file, output_dir)