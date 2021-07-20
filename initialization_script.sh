#!/bin/bash  
rm -r imagecaptioning
git submodule add https://github.com/sarmilaupadhyaya/ImageCaptioning.pytorch.git
mv ImageCaptioning.pytorch imagecaptioning
cd imagecaptioning
mkdir data/imagenet_weights

wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=0B7fNdx_jAqhtSmdCNDVOVVdINWs' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=0B7fNdx_jAqhtSmdCNDVOVVdINWs" -O data/imagenet_weights/resnet101.pth && rm -rf /tmp/cookies.txt


git clone https://github.com/sarmilaupadhyaya/coco-caption.git

cd coco-caption
chmod +x get_stanford_models.sh
chmod +x get_google_word2vec_model.sh
./get_stanford_models.sh
./get_google_word2vec_model.sh
cd ..
python -m pip install -e .
cd ..

wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1-bnWPP6-c42wVQMztHpcVquUGd1XGc-z' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1-bnWPP6-c42wVQMztHpcVquUGd1XGc-z" && -O models.zip rm -rf /tmp/cookies.txt

unzip models.zip


