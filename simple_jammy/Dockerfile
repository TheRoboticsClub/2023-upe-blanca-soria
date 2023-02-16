FROM basic-jammy
# ------------ Funcionamiento de Unibotics
# custom-robots
RUN mkdir -p /opt/jderobot && cd /opt/jderobot && \
	git clone -b noetic-devel https://github.com/JdeRobot/CustomRobots.git

EXPOSE 6080
EXPOSE 1108
EXPOSE 2303
EXPOSE 1905

CMD ["bash"]