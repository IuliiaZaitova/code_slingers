import pandas as pd
import sys

sys.path.append("/home/sharmila/projects/code_slingers")
from imagecaptioning.tools import eval

result = eval.evaluation(model='output/image-captioning/model_path/model-best.pth', image_folder="data/test_image/", cnn_model='resnet101', infos_path='output/image-captioning/model_path/infos_fc_nsc-best.pkl', only_lang_eval=0, force=1,device="cpu")

df = pd.DataFrame(result)

df.to_csv("output/image-captioning/captions.csv")
