# Foobar

Software Project by team CODE SLINGERS for Language Generation Task.

## Introduction
This project is an attempt to generate joke based on Image. Hence, it includes three task:

    1. Image captioning
    2. Getting relevant entities for joke generation
    3. Joke generation module


## Installation

In order to get the model to run, follow these installation instructions.


<!-- ### Requirements -->
Pre-reqisite:

    python <= 3.7.5

---
_Optional_: to install a specific version of Python:

#### Ubuntu:

    sudo apt-install python3.6


#### Mac:

    [instructions]


#### Windows:

    [instructions]
---
#### Clone the repository

    git clone [link]

_Optional_: use the package manager [pip](https://pip.pypa.io/en/stable/) to install vitual environment.

    bash
    pip install virtualenv
    
    
#### Navigate to the folder with the cloned git repository

#### Create Virtual Environment

    virtualenv <name of env> --python /usr/bin/python[version] or <path to your python if its not the mentioned one>

#### Activate Virtual Environment

    source name_of_env/bin/activate


#### Install Requirements

    pip install -r requirements.txt




---

_Optional_: If you're on Mac.  

***Note: if you are on mac, then first install wget and unzip package***  

    [instructions]

---

#### Initial Downloads

    brew install wget
    chmod +x initialization_script.sh
    ./initialization_script.sh


**_YEAH!!_** Installation is done! Now you can jump to the execution part and run the web app.


## Execution
To run the webapp, run the following code, being in the root directory.

    python3 src/views.py



---


## Datasets

- Image Captioning Dataset
[Link](https://paperswithcode.com/datasets)

### COCO DATASET
- Download

```
./src/coco-download.sh

```
- Paper about the dataset
[Link] (https://arxiv.org/abs/1405.0312)

- Evaluation of dataset
This section gets all the captions and extract the entity and action from the captions and create a simple analysis

- Joke Dataset

 [Link](https://www.kaggle.com/abhinavmoudgil95/short-jokes)


## Execution
To run the webapp, run the following code, being in the root directory.

```
python3 src/views.py

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
