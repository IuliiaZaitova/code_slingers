# Foobar

Software Project by team CODE SLINGERS for Language Generation Task.

## Introduction
This project is an attempt to generate joke based on Image. Hence, it includes three task:

    1. Image captioning
    2. Getting relevant entities for joke generation
    3. Joke generation module


## Installation
### Requirements
    python <= 3.7.5

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install vitual environment.

```bash
pip install virtualenv
```

### Create Virtual Environment

```
virtualenv <name of env> --python /usr/bin/python3 or <path to your python if its not the mentioned one>

```

### install requirements

```
pip install -r requirements.txt

```

### Initial Downloads
***Note: if you are on mac, then first install wget:***
***Also, install unzip package***

```
brew install wget

```


```
chmod +x initialization_script.sh
./initialization_script.sh

```

YEAH!! installation is done. Now you can jump to the execution part and run the web app.


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
