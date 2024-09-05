import cv2
import os

def images_to_video(image_folder='./tmp', output_video_path='video/enc_video.avi', fps=30):
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    images.sort(key=lambda x: int(x.split('.')[0]))
    # print(images)

    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc('F','F','V','1'), fps, (width, height), isColor=True)

    for image in images:
        img_path = os.path.join(image_folder, image)
        img = cv2.imread(img_path)
        video.write(img)

    cv2.destroyAllWindows()
    video.release()
