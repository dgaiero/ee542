#!/bin/bash

# From: https://github.com/mohaseeb/raspberrypi3-opencv-docker/blob/master/opencv_3/3.4.2/download_build_install_opencv.sh

OPENCV_VERSION=3.4.2

WS_DIR=`pwd`
mkdir opencv
cd opencv

# download OpenCV and opencv_contrib
wget -O opencv.zip https://github.com/opencv/opencv/archive/$OPENCV_VERSION.zip
unzip opencv.zip
rm -rf opencv.zip

wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/$OPENCV_VERSION.zip
unzip opencv_contrib.zip
rm -rf opencv_contrib.zip

OPENCV_SRC_DIR=`pwd`/opencv-$OPENCV_VERSION
OPENCV_CONTRIB_MODULES_SRC_DIR=`pwd`/opencv_contrib-$OPENCV_VERSION/modules

# build and install
cd $OPENCV_SRC_DIR
mkdir build && cd build
cmake -D BUILD_opencv_java=OFF \
  -D WITH_CUDA=OFF \
  -D WITH_OPENGL=ON \
  -D WITH_OPENCL=ON \
  -D WITH_IPP=ON \
  -D WITH_TBB=ON \
  -D WITH_EIGEN=ON \
  -D WITH_V4L=ON \
  -D BUILD_TESTS=OFF \
  -D BUILD_PERF_TESTS=OFF \
  -D CMAKE_BUILD_TYPE=RELEASE \
  -D CMAKE_INSTALL_PREFIX=$(python3.9 -c "import sys; print(sys.prefix)") \
  -D PYTHON_EXECUTABLE=$(which python3.9) \
  -D PYTHON_INCLUDE_DIR=$(python3.9 -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") \
  -D PYTHON_PACKAGES_PATH=$(python3.9 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") \
  -D OPENCV_EXTRA_MODULES_PATH=$OPENCV_CONTRIB_MODULES_SRC_DIR \
  ..

make -j4			

make install
ldconfig

# verify the installation is successful
python -c "import cv2; print('Installed OpenCV version is: {} :)'.format(cv2.__version__))"
if [ $? -eq 0 ]; then
    echo "OpenCV installed successfully! ........................."
else
    echo "OpenCV installation failed :( ........................."
    SITE_PACKAGES_DIR=/usr/local/lib/python2.7/site-packages
    echo "$SITE_PACKAGES_DIR contents: "
    echo `ls -ltrh $SITE_PACKAGES_DIR`
    echo "Note: temporary installation dir $WS_DIR/opencv is not removed!"
    exit 1
fi

# cleanup
cd $WS_DIR
rm -rf opencv