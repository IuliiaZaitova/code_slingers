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

    ```
    chmod +x initialization_script.sh
    ./initialization_script.sh

    ```



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
