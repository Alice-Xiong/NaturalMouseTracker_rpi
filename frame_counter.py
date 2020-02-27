import cv2 


def get_video_frame_count(folder): 
# Get count from video
    count=0
    cap=cv2.VideoCapture(str(folder) + '/raw.avi')
    while (cap.isOpened()):
        ret,img=cap.read()
        if ret ==True:
            count+=1
        else:
            break
    print('[INFO] video frame count: ' + str(count))


def get_txt_frame_count(folder): 
    # Get frame count from txt
    count = 0
    with open(str(folder) + '/RFID_data_all.txt', 'r') as f:
        for line in f:
            count+=1
    print('[INFO] logfile frame count: ' + str(count-1))



'''
Testing code
'''
if __name__ == '__main__':
    folder = input('What is the folder name? ')
    get_video_frame_count(folder)
    get_txt_frame_count(folder)
