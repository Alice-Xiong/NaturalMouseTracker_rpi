#$ sudo chmod 765 pi_video_stream_setup.sh
#$ sudo ./pi_video_stream_setup.sh

    echo "Installing python packages"
    pip3 install numpy
    pip3 install imutils
    apt install libatlas3-base libsz2 libharfbuzz0b libtiff5 libjasper1 libilmbase12 libopenexr22 libilmbase12 libgstreamer1.0-0 libavcodec57 libavformat57 libavutil55 libswscale4 libqtgui4 libqt4-test libqtcore4
    pip3 install opencv-contrib-python libwebp6
    pip3 install wiringpi
    pip3 install tables

    echo "Install complete\n Make sure you manually ENABLE CAMERA PORT."
    exit
