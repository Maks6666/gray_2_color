# Photo/Video colorizer with autoencoder neural network.


<div style="display: flex; justify-content: space-between;">

<img src="c_ex.jpg" alt="Фото 1" style="width: 49%;" />
<img src="ex.jpg" alt="Фото 2" style="width: 49%;" />


    

    
</div>

#
Model of autoencoder Neural Network, which can colorize images and videoframes. It is custom autoencoder model designed and built by myselt using Tensorflow functional API. Model contains more than 21 millions of parameters and weighs 81 MB. Model was trained with this [dataset](/kaggle/input/landscape-image-colorization) in Kaggle notebook with GPU P100. You may check all parameters in "autoencoder_structure.ipynb" file. 



<div style="display: flex; justify-content: space-between;">
    <img src="params.jpg" alt="Фото 1" style="width: 100%" />
</div>

#
Here is also a program, which allows users to handle any image by model using just interface elements of console apps without code using. Running "main.py" in a folder with NN model weights, (which you may recieve, running "autoencoder_structure.ipynb" file on any data) and photo to preprocess, program will allow you to chose some photos from working folder and then, they will be automatically proprocessed by NN model and returned in the same folder.

<div style="display: flex; justify-content: space-between;">
    <img src="curses.jpg" alt="Фото 1" style="width: 100%" />
</div>

#
Program uses "Curses" module as main graphical interface element. 


## Model
File with model - autoencoder.structure.ipynb" containes two different colorizer autoencoder models - for 320x320 and for 240x240 images. Depending on user task, it is possible to use them all, fitting data there. 

## Model structure 

Autoencoder as a main program engine in both variations is written with Tensorflow functional API and each of them uses Conv2D as main convolutional layers. Also MaxPooling2D and UpSampling2D layers are used as up- and down samplers of images sizes. As a main activation function, autoencoders use LeakyRelu. 



## Video colorization
Program is also able to colorize videos. Being just a bunch of images (frames), each video could be divided into frame^ which will be put into array form and could be also fitted for model. It will preprocess it and return colorized one as "colorized_test_video_mp4". 

## Authors:
- Kucher Maks (maxim.kucher2005@gmail.com)
