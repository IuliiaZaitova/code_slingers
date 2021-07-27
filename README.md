# Foobar

Software Project by team CODE SLINGERS for the Language Generation Task course at Saarland University.

## Introduction

This project is an attempt to generate WHY-jokes following the formula ```Why did X Y? -Z!"``` (e.g. _Why did the chicken cross the road? To get to the other side!_) based on an image. Hence, it encompasses three main tasks:

    1. Image captioning module
    2. Getting relevant entities for joke generation / Question generation module
    3. Joke generation module


## Installation

Note: Since, the project has three models as the pipeline running serially, it requires some memory space and RAM. Make sure you have around 3 GB physical disk space, 4 GB RAM and enough space to install the requirements. 

In order to get the model to run, follow these installation instructions.


<!-- ### Requirements -->
Pre-requisite:

    python==3.7.5

---
_Optional_: to install a specific version of Python:

#### Ubuntu:

    sudo apt-install python3.7


#### Mac:

    brew install python@3.7


#### Windows:
Download [32-bit version](https://www.python.org/ftp/python/3.7.5/python-3.7.5.exe) or [64-bit version](https://www.python.org/ftp/python/3.7.5/python-3.7.5-amd64.exe) and follow the instructions.


---
#### Clone the repository

    git clone [link]

_Optional_: use the package manager [pip](https://pip.pypa.io/en/stable/) to install vitual environment.

    bash
    pip install virtualenv
    
    
    
#### Navigate to the folder with the cloned git repository

#### Create Virtual Environment

    virtualenv <name of env> --python /usr/bin/python[version] or <path to your python if its not the mentioned one>
    
    Conda:
    conda create --name <name of your env> python=3.7

#### Activate Virtual Environment

    source name_of_env/bin/activate
    On Windows: name_of_env\Scripts\activate
    Conda:
    conda activate <name of your env>

(To leave the virtual environment, simply run: deactivate)

#### Install Requirements

    pip install -r requirements.txt
        
    Conda:
    have to first run:
    conda install pip



---

_Optional_: If you're on Mac.  

***Note: if you are on mac, then first install wget using brew***  

    [instructions]
    brew install wget

---

#### Initial Downloads
    This is the step that clones the submodules required for captioning, download pretrained models and set them up.
    
    ```
    chmod +x initialization_script.sh
    ./initialization_script.sh
    
    ```


**_YEAH!!_** Installation is done! Now you can jump to the execution part and run the web app.


## Execution
Before running the application, make sure to change the ROOT_PATH variable in the .env file to the path of your project.

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
