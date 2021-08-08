# Software Project by team CODE SLINGERS for the Language Generation Task course at Saarland University.

![architecture](https://github.com/IuliiaZaitova/code_slingers/blob/master/images/example-2.png?raw=true)

While there is already some Humor Generation work out there using given word context, in this project we explore Humor Generation given images. A joint pipeline of image captioning, question generation from the caption and finally a joke in the form of answer to the question is the brief architecture. We were able to implement it successfully and get comparative result to the works done before.

# Outline

1. Directory Structure
2. Introduction
3. Installation
4. Dataset
5. Contributing
6. License


## Directory structure

    .
    ├── data     #pickle files for templates and object generations
    │   ├── aux_verbs.pkl
    │   ├── dobj_dict_classes.p
    │   ├── one_slot.pkl
    │   ├── pobj_dict_classes.p
    │   ├── three_slots.pkl
    │   ├── two_slots.pkl
    │   ├── verb_transitivity.tsv
    │   └── verb_trans.p
    ├── documents    #general documents
    │   └── code_slingers_presentation.pdf
    ├── images      #images
    │   └── architecture.png
    ├── initialization_script.sh    #for initialization
    ├── initialization_script_windows.sh
    ├── README.md
    ├── requirements.txt
    └── src     #main python files
        ├── grammar_parsing.py
        ├── joke_generator.py
        ├── main.py
        ├── parsing.py
        ├── question_generation.py
        ├── static  #static file for the app
        │   ├── css
        │   │   └── main.css
        │   └── img
        │       └── saarland.png
        ├── templates    # html 
        │   └── upload_image.html
        └── views.py    #main flask app file


## Introduction

This project is an attempt to generate WHY-jokes following the formula ```Why did X Y? -Z!"``` (e.g. _Why did the chicken cross the road? To get to the other side!_) based on an image. Hence, it encompasses three main tasks:

    1. Image captioning
    2. Question generation / Getting relevant entities for joke generation
    3. Joke generation

The short architecture of our project:
    
![architecture](https://github.com/IuliiaZaitova/code_slingers/blob/master/images/New_Architecture_updated.png?raw=true)


## Installation

Note: Since, the project has three models as the pipeline running serially, it requires some memory space and RAM. Make sure you have around 3 GB physical disk space, 4 GB RAM and enough space to install the requirements. 

In order to get the model to run, follow these installation instructions.


<!-- ### Requirements -->
Pre-requisites:

    python==3.7.5

On Windows you will also need [Git for Windows](https://gitforwindows.org/).

---
_Optional_: to install a specific version of Python:

#### Ubuntu:

    pyenv install 3.7.5

(To install ```pyenv```, follow [this tutorial](https://github.com/pyenv/pyenv-installer#installation--update--uninstallation), and then [this one](https://www.laac.dev/blog/setting-up-modern-python-development-environment-ubuntu-20/))
<!--     sudo apt-install python3.7 -->


#### Mac:

    brew install python@3.7


#### Windows:
Download Python 3.7.5 for Windows [here](https://www.python.org/ftp/python/3.7.5/python-3.7.5-amd64.exe), run it and follow the instructions.
    
---
#### Clone the repository

    git clone [link]

_Optional_: use the package manager [pip](https://pip.pypa.io/en/stable/) to install a vitual environment.

    bash
    pip install virtualenv
    
    
    
#### Navigate to the folder with the cloned git repository

#### Create Virtual Environment

    virtualenv <name of env> --python /usr/bin/python[version] or <path to your python if its not the mentioned one>
    
Conda:

    conda create --name <name of your env> python=3.7

#### Activate Virtual Environment

    source name_of_env/bin/activate
On Windows:

    name_of_env\Scripts\activate
Conda:

    conda activate <name of your env>

(To leave the virtual environment, simply run: ```deactivate``` (with virtualenv) or ```conda deactivate``` (with Conda))

---

### Install Requirements

    pip install -r requirements.txt
        
Conda:

    conda install pip
    pip install -r requirements.txt


---

_Optional_: If you're on Mac.  

***Note: if you are on mac, then first install wget using brew***  

    brew install wget

---

---
You also need to download the spacy model:

    python -m spacy download en_core_web_lg

---

#### Initial Downloads

This is the step that clones the submodules required for captioning, download pretrained models and set them up. This might take a while depending on your internet speed. :)
    
    chmod +x initialization_script.sh
    ./initialization_script.sh
    
 On Windows:
 
 If you did not choose to import Linux tools when installing Git for Windows, you have to use the Git Bash to run the initialization script. Either way, both Git Bash and Windows Command Prompt should be run as administrator.

    chmod +x initialization_script.sh
    sh initialization_script_windows.sh

---

************************************************************************************************************************************
**NOTE**: If you encounter the following error (mostly due to internet issue models are not downloaded properly and you can't unzip.

```
Archive:  models.zip
  End-of-central-directory signature not found.  Either this file is not
  a zipfile, or it constitutes one disk of a multi-part archive.  In the
  latter case the central directory and zipfile comment will be found on
  the last disk(s) of this archive.
unzip:  cannot find zipfile directory in one of models.zip or
        models.zip.zip, and cannot find models.zip.ZIP, period.

```
Then Kindly rerun the following code

```

wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1-bnWPP6-c42wVQMztHpcVquUGd1XGc-z' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1-bnWPP6-c42wVQMztHpcVquUGd1XGc-z"  -O models.zip && rm -rf /tmp/cookies.txt
unzip models.zip


```

If not then skip this section
************************************************************************************************************************************
**_YAY!!_** Installation is done! Now you can jump to the execution part and run the web app.


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


./src/coco-download.sh

sh src/coco-download.sh


- Paper about the dataset
[Link] (https://arxiv.org/abs/1405.0312)

- Evaluation of dataset
This section gets all the captions and extract the entity and action from the captions and create a simple analysis

- Joke Dataset

 [Link](https://www.kaggle.com/abhinavmoudgil95/short-jokes)


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
