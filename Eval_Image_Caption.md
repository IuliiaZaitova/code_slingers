# This file tells steps to set up the evaluation for image captioning.
Here, the git [link](https://github.com/ruotianluo/ImageCaptioning.pytorch) is used for the image captioning.
FOllow the following steps for evaluation on raw image.

1. Add this git submodule in your repo.

```
git submodule add https://github.com/ruotianluo/ImageCaptioning.pytorch
```

2. There is another submodule inside the ImageCaptioning.pytorch i.e. [coco-caption](https://github.com/ruotianluo/coco-caption/tree/ea20010419a955fed9882f9dcc53f2dc1ac65092)
        - First clone the content using 

	```
	git clone https://github.com/ruotianluo/coco-caption/tree/ea20010419a955fed9882f9dcc53f2dc1ac65092
	```

	- Remember to follow initialization steps in coco-caption/README.md i.e.
        - Go inside coco-caption folder and you will first need to download the Stanford CoreNLP 3.6.0 code and models for use by SPICE. To do this, run: bash get_stanford_models.sh
        - Note: SPICE will try to create a cache of parsed sentences in ./pycocoevalcap/spice/cache/. This dramatically speeds up repeated evaluations. The cache directory can be moved by setting 'CACHE_DIR' in ./pycocoevalcap/spice. In the same file, caching can be turned off by removing the '-cache' argument to 'spice_cmd'.
        -You will also need to download the Google News negative 300 word2vec model for use by WMD. To do this, run: bash get_google_word2vec_model.sh


3. Download the pretrained model from this [link](https://github.com/ruotianluo/ImageCaptioning.pytorch/blob/master/MODEL_ZOO.md). Download one of the model Trained with Resnet101 feature. Put the model into output/image-captioning/model_path/

4. Download the resnet 101 pretrained model from [link](https://drive.google.com/drive/folders/0B7fNdx_jAqhtbVYzOURMdDNHSGM). Put it inside ImageCaptioning.pytorch/data/imagenet_weights

5. run
```
python -m pip install -e .
```
6. If you running without gpu, run the file image_captioning_test.py with path to the test image. This file is in the src folder which is in the root directory




