FROM nvidia/opengl:1.2-glvnd-runtime-ubuntu20.04

ARG VIRTUALGL_VERSION=3.0
ARG TURBOVNC_VERSION=3.0

# Setup NON INTERACTIVE ENVIRONMENT
ARG DEBIAN_FRONTEND=noninteractive

# Install locales to prevent errors
RUN apt-get clean && \
    apt-get update && \
    apt-get install --no-install-recommends -y locales && \
    rm -rf /var/lib/apt/lists/* && \
    locale-gen en_US en_US.UTF-8
ENV LANG en_US.UTF-8 
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Install desktop and common tools
RUN apt-get update && apt-get install -y \
        software-properties-common \
        apt-utils \
        build-essential make gcc git \
        ca-certificates \
        curl wget \
        gzip zip unzip \
        libc6-dev libglu1 libglu1:i386 libegl1-mesa libegl1-mesa:i386 \
        libsm6 libxv1 libxv1:i386 libpci3 \
        python3 python3-numpy libpython3-dev \
        python \
        x11-xkb-utils xauth xfonts-base xkb-data \
        libxtst6 libxtst6:i386 \
        mlocate \
        nano vim \
        htop net-tools \
        xterm rsync \
        lxde-core \
        tasksel && \
    rm -rf /var/lib/apt/lists/*
RUN tasksel install lubuntu-core lubuntu-desktop

# Install VirtualGL and TurboVNC
RUN wget --no-check-certificate https://deac-fra.dl.sourceforge.net/project/virtualgl/${VIRTUALGL_VERSION}/virtualgl_${VIRTUALGL_VERSION}_amd64.deb && \
    wget --no-check-certificate https://kumisystems.dl.sourceforge.net/project/virtualgl/${VIRTUALGL_VERSION}/virtualgl32_${VIRTUALGL_VERSION}_amd64.deb && \
    apt-get update && dpkg -i ./virtualgl_${VIRTUALGL_VERSION}_amd64.deb ./virtualgl32_${VIRTUALGL_VERSION}_amd64.deb && \
    rm virtualgl_${VIRTUALGL_VERSION}_amd64.deb virtualgl32_${VIRTUALGL_VERSION}_amd64.deb && \
    chmod u+s /usr/lib/libvglfaker.so && \
    chmod u+s /usr/lib/libdlfaker.so && \
    chmod u+s /usr/lib32/libvglfaker.so && \
    chmod u+s /usr/lib32/libdlfaker.so && \
    chmod u+s /usr/lib/i386-linux-gnu/libvglfaker.so && \
    chmod u+s /usr/lib/i386-linux-gnu/libdlfaker.so && \
    wget --no-check-certificate https://sourceforge.net/projects/turbovnc/files/${TURBOVNC_VERSION}/turbovnc_${TURBOVNC_VERSION}_amd64.deb && \
    apt-get update && apt-get install -y --no-install-recommends ./turbovnc_${TURBOVNC_VERSION}_amd64.deb && \
    rm turbovnc_${TURBOVNC_VERSION}_amd64.deb && \
    rm -rf /var/lib/apt/lists/* && \
    echo -e "no-remote-connections\n\
no-httpd\n\
no-x11-tcp-connections\n\
no-pam-sessions\n\
permitted-security-types = None, VNC, otp\
" > /etc/turbovncserver-security.conf
# Set paths for VirtualGL and turboVNC
ENV PATH "$PATH:/opt/VirtualGL/bin:/opt/TurboVNC/bin"

# Install noVNC and Websockify
RUN git clone https://github.com/novnc/noVNC.git -b v1.2.0 && \
	cd noVNC/utils && \
	git clone https://github.com/novnc/websockify websockify -b v0.9.0

# Xorg segfault error mitigation
RUN apt-get update && apt-get install -y --no-install-recommends \
        dbus-x11 \
        libdbus-c++-1-0v5 && \
    rm -rf /var/lib/apt/lists/*

# Gazebo11
RUN wget --quiet http://packages.osrfoundation.org/gazebo.key -O - | apt-key add - \
	&& sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -sc` main" > /etc/apt/sources.list.d/gazebo-stable.list' \
	&& apt-get update \
	&& DEBIAN_FRONTEND=noninteractive apt-get -y --quiet --no-install-recommends install \
        ant \
        binutils \
        bc \
        dirmngr \
        gazebo11 \
        gstreamer1.0-plugins-bad \
        gstreamer1.0-plugins-base \
        gstreamer1.0-plugins-good \
        gstreamer1.0-plugins-ugly \
        libeigen3-dev \
        libgazebo11-dev \
        libgstreamer-plugins-base1.0-dev \
        libimage-exiftool-perl \
        libopencv-dev \
        libxml2-utils \
        mesa-utils \
        protobuf-compiler \
        x-window-system \
	&& apt-get -y autoremove \
	&& apt-get clean autoclean \
	&& rm -rf /var/lib/apt/lists/{apt,dpkg,cache,log} /tmp/* /var/tmp/*

# apt-get install dependencies
# Nodejs, x11vnc, xterm, xdummy
RUN apt-get update && apt-get --no-install-recommends install -y \
		x11vnc \
		xterm \
		xserver-xorg-video-dummy \
		x11-apps \
	&& apt-get -y autoremove \
	&& apt-get clean autoclean \
	&& rm -rf /var/lib/apt/lists/{apt,dpkg,cache,log} /tmp/* /var/tmp/*

RUN wget https://xpra.org/xorg.conf \
    && rm -rf /tmp/*
# Install ROS and ROS packages
ENV ROS_DISTRO noetic
RUN apt-get update && apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654 \
	&& sh -c 'echo "deb http://packages.ros.org/ros/ubuntu `lsb_release -sc` main" > /etc/apt/sources.list.d/ros-latest.list' \
	&& sh -c 'echo "deb http://packages.ros.org/ros-shadow-fixed/ubuntu `lsb_release -sc` main" > /etc/apt/sources.list.d/ros-shadow.list' \
	&& apt-get update \
	&& apt-get -y --quiet --no-install-recommends install \
    ros-$ROS_DISTRO-desktop-full \
    geographiclib-tools \
    libeigen3-dev \
    libgeographic-dev \
    libopencv-dev \
    libyaml-cpp-dev \
    python3-rosdep \
    python3-catkin-tools \
    python3-catkin-lint \
    python3-rosinstall-generator \
    python3-osrf-pycommon \
    python3-vcstool \
    ros-$ROS_DISTRO-gazebo-ros-pkgs \
    ros-$ROS_DISTRO-octomap \
    ros-$ROS_DISTRO-octomap-msgs \
    ros-$ROS_DISTRO-pcl-conversions \
    ros-$ROS_DISTRO-pcl-msgs \
    ros-$ROS_DISTRO-pcl-ros \
    ros-$ROS_DISTRO-ros-base \
    ros-$ROS_DISTRO-rostest \
    ros-$ROS_DISTRO-rosunit \
    ros-$ROS_DISTRO-xacro \
	&& geographiclib-get-geoids egm96-5 \
	&& apt-get -y autoremove \
	&& apt-get clean autoclean \
	&& rm -rf /var/lib/apt/lists/{apt,dpkg,cache,log} /tmp/* /var/tmp/*
    
#vainas de jderobots
RUN mkdir -p /opt/jderobot && cd /opt/jderobot && \
	git clone -b $ROS_DISTRO-devel https://github.com/JdeRobot/CustomRobots.git

# instalar rviz
RUN apt-get update && apt-get --no-install-recommends install -y \
    rviz \
    && apt-get -y autoremove \
	&& apt-get clean autoclean \
	&& rm -rf /var/lib/apt/lists/{apt,dpkg,cache,log} /tmp/* /var/tmp/*

# comanditos para dejar todo preparau par ejecutar ros
RUN sudo apt-get update && rosdep init && rosdep update

# expose port
EXPOSE 6080
EXPOSE 1108
EXPOSE 2303
EXPOSE 1905

COPY . /home


CMD ["bash"]
