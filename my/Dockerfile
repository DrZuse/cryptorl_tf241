#docker build -t cryptorl:tf241 --rm .

FROM tensorflow/tensorflow:2.4.1
RUN apt-get update -y
RUN apt-get upgrade -y
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata mc
RUN apt-get install mongodb -y

RUN pip install --upgrade pip
RUN pip install wheel

RUN pip install cbpro
RUN pip install numpy
RUN pip install arctic
RUN pip install gym
RUN pip install h5py
RUN pip install Keras
RUN pip install Keras-Applications
RUN pip install Keras-Preprocessing
RUN pip install keras-rl2
RUN pip install more-itertools
RUN pip install pytest
RUN pip install python-dateutil
RUN pip install pytz
RUN pip install requests
RUN pip install scipy
RUN pip install sortedcontainers
RUN pip install tensorboard
RUN pip install tensorflow-estimator
RUN pip install tzlocal
RUN pip install urllib3
RUN pip install websockets
RUN pip install Cython
RUN pip install matplotlib
RUN pip install scikit-learn
#RUN pip install "dask[complete]"
RUN pip install pymongo
