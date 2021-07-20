#!/bin/bash  


git submodule add https://github.com/sarmilaupadhyaya/ImageCaptioning.pytorch.git

cd ImageCaptioning

git clone https://github.com/ruotianluo/coco-caption.git

cd coco-caption
chmod +x get_stanford_models.sh
chmod +x get_google_word2vec_model.sh
./get_stanford_models.sh
./get_google_word2vec_model.sh
cd ..
python -m pip install -e .


