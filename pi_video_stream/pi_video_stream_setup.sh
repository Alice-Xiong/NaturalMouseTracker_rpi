#$ sudo chmod 765 pi_video_stream_setup.sh
#$ sudo ./pi_video_stream_setup.sh

    echo "Installing python packages"
    pip python3 install numpy
    pip python3 install picamera
    pip python3 install datetime
    pip python3 install tables
    pip python3 install csv
    pip python3 install configparser

    exit