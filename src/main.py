## code for main workflow where following steps with take place
## input path will be passed 
## calling image captioning module to generate caption
## passing image caption to a model to extract entities
## passing entities and getting question from rule based question generation module
## passing the question to the joke generation module and getting the joke, which will be returned
## This file will be calling all of our model one by one
import os
from question_generation import *
import sys
from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.getenv("ROOT_PATH"))
from imagecaptioning.tools import eval
from src import joke_generator as jg
from bs4 import BeautifulSoup

model_path = os.getenv("MODEL_PATH")
info_path = os.getenv("INFO_PATH")
def captioning_inference(image_path= "data/test_image/"):

    result = eval.evaluation(model=model_path, image_folder=image_path, cnn_model='resnet101', infos_path=info_path, only_lang_eval=0, force=1,device="cpu")

    return result


def cleanMe(html):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    return [s for s in soup.strings if s not in ['','\n']]



def main(image_path="data/test_image/"):
    """
    main pipeline
    params:
    image_path: path to the image uploaded by the user
    """

    all_files = []
    import os
    for file in os.listdir(image_path):
        if file.endswith(".jpg"):
            all_files.append(file)

    image_caption = captioning_inference(image_path)
    # question template

    questions = []
    for each,filename in zip(image_caption, all_files):
        question_generator = QuestionGenerator(generate_objects=True)
        doc = question_generator.parser.nlp(each["caption"])
        verbs, nps = question_generator.parse_caption(each["caption"])
        if question_generator.gen_obj:
            # get subject np
            subj = question_generator.parser.get_subj_np(nps)
            # generate objects
            word_parser = Word_parser(question_generator.parser.nlp)
            obj = word_parser.get_objects(str(verbs[0]))

            if obj:
                nps = [subj]+obj
        # get template for question
        template, nps = question_generator.choose_template(verbs, nps)
        # fill template
        question = question_generator.fill_template(template, verbs, nps)
        questions.append(question)
        

    df = pd.DataFrame(image_caption)
    df["filename"] = pd.Series(all_files)
    df["questions"] = pd.Series(questions)

    jokes = []    
    # passing question to gpt-2 and getting answer

    for question in questions:
        jokes.append(jg.evaluation(question))

    df["jokes"] = pd.Series(jokes)
    df["jokes"] =  df.jokes.apply(lambda x: cleanMe(x))
    if len(df) == 1:
        return df.to_dict()



    #df.to_csv("output/image-captioning/captions_new.csv")


#main("/home/sharmila/projects/code_slingers/coco/data/images/test2017")
