## code for main workflow where following steps with take place
## input path will be passed 
## calling image captioning module to generate caption
## passing image caption to a model to extract entities
## passing entities and getting question from rule based question generation module
## passing the question to the joke generation module and getting the joke, which will be returned
## This file will be calling all of our model one by one

from question_generation import *
import sys
sys.path.append("/home/sharmila/projects/code_slingers")
from imagecaptioning.tools import eval
from src import joke_generator as jg

def captioning_inference(image_path= "data/test_image/"):

    result = eval.evaluation(model='output/image-captioning/model_path/model-best.pth', image_folder=image_path, cnn_model='resnet101', infos_path='output/image-captioning/model_path/infos_fc_nsc-best.pkl', only_lang_eval=0, force=1,device="cpu")

    return result



def main(image_path="data/test_image/"):
    """
    main pipeline
    params:
    image_path: path to the image uploaded by the user
    """
    image_caption = captioning_inference(image_path)
    # question template

    questions = []
    for each in image_caption:
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
    df["questions"] = pd.Series(questions)

    jokes = []    
    # passing question to gpt-2 and getting answer
    for question in questions:
        jokes.append(jg.evaluation(question))

    df["jokes"] = pd.Series(jokes)

    if len(df) == 1:
        return df.to_dict()



    #df.to_csv("output/image-captioning/captions.csv")



