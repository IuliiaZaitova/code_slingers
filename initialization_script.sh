#!/bin/bash  
git submodule add https://github.com/sarmilaupadhyaya/ImageCaptioning.pytorch.git
cd ImageCaptioning
mkdir data/imagenet_weights
#wget https://drive.google.com/file/d/0B7fNdx_jAqhtSmdCNDVOVVdINWs/view?usp=sharing&resourcekey=0-yY3hyjUhP3WTTj4n6s95zg -O imagecaptioning/data/imagenet_weights/resnet101.pth
git clone https://github.com/ruotianluo/coco-caption.git

cd coco-caption
chmod +x get_stanford_models.sh
chmod +x get_google_word2vec_model.sh
./get_stanford_models.sh
./get_google_word2vec_model.sh
cd ..
python -m pip install -e .


