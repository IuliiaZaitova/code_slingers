Software Project by team CODE SLINGERS for Language Generation Task.
Jump to the set up


# Introduction #

This project is an attempt to generate joke based on Image. Hence, it includes three task:

1. Image captioning
2. Getting relevant entities for joke generation
3. Joke generation module



# Set Up #

    python version used is 3.7.5

    ## Note: ## it is required for python to be less than equal to 3.7.2 as we are using tensorflow 1.14 and it is not supported with latest python.

    Go through this link if you have higher version of python and you want to set up pyenv to manage different version of python.



    - Install the virtual Environment

    ```
    pip install virtualenv

    ```

    - Create the virtual environment

    ```
    virtualenv <name of env> --python /usr/bin/python3 or <path to your python if its not the mentioned one>

    ```

    - run this script to set up the initial directory required, to download all the files and set up the git for image captioning.(Recommended)

    OR
    
     run following steps step by step


        - This file tells steps to set up the evaluation for image captioning.

          Here, the git [link](https://github.com/ruotianluo/ImageCaptioning.pytorch) is used for the image captioning.
          Follow the following steps for evaluation on raw image. 

        1. Add this git submodule in your repo.

       ```
       git submodule add https://github.com/ruotianluo/ImageCaptioning.pytorch
       ```
       Change the directory and go inside ImageCaptioning.pytorch

       2. There is another submodule inside the ImageCaptioning.pytorch i.e. [coco-caption](https://github.com/ruotianluo/coco-caption/tree/ea20010419a955fed9882f9dcc53f2dc1ac65092)
        - First clone the content using 

	```
	git clone https://github.com/ruotianluo/coco-caption/tree/ea20010419a955fed9882f9dcc53f2dc1ac65092
	```

	- Remember to follow initialization steps in coco-caption/README.md i.e.
        - Go inside coco-caption folder and you will first need to download the Stanford CoreNLP 3.6.0 code and models for use by SPICE. To do this, run: bash get_stanford_models.sh
        - Note: SPICE will try to create a cache of parsed sentences in ./pycocoevalcap/spice/cache/. This dramatically speeds up repeated evaluations. The cache directory can be moved by setting 'CACHE_DIR' in ./pycocoevalcap/spice. In the same file, caching can be turned off by removing the '-cache' argument to 'spice_cmd'.
        -You will also need to download the Google News negative 300 word2vec model for use by WMD. To do this, run: bash get_google_word2vec_model.sh


         3. Download the pretrained model from this [link](https://github.com/ruotianluo/ImageCaptioning.pytorch/blob/master/MODEL_ZOO.md). Download one of the model Trained with Resnet101 feature. Put the model into output/image-captioning/model_path/ in the root git project

         4. Download the resnet 101 pretrained model from [link](https://drive.google.com/drive/folders/0B7fNdx_jAqhtbVYzOURMdDNHSGM). Put it inside ImageCaptioning.pytorch/data/imagenet_weights

         5. run
         ```
         python -m pip install -e .
         ```
        - Its done now

    -Set up for joke generation

    Make sure the checkpoint folder is inside output directory




# Datasets #

- Image Captioning Dataset
[Link](https://paperswithcode.com/datasets)

## COCO DATASET ##
- Download

```
./src/coco-download.sh

```


- Paper about the dataset
[Link] (https://arxiv.org/abs/1405.0312)

- Evaluation of dataset
THis section gets all the captions and extract the entity and action from the captions and create a simple analysis

- Joke Dataset

 [Link](https://www.kaggle.com/abhinavmoudgil95/short-jokes)


# Execution #

- individual image captioning inference running

Note: first go through set up [here](https://github.com/IuliiaZaitova/code_slingers/blob/master/Eval_Image_Caption.md)

```

python3 src/image_captioning_test.py

```
