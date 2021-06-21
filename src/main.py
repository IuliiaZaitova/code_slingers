## code for main workflow where following steps with take place
## input path will be passed 
## calling image captioning module to generate caption
## passing image caption to a model to extract entities
## passing entities and getting question from rule based question generation module
## passing the question to the joke generation module and getting the joke, which will be returned
## This file will be calling all of our model one by one

from question_generation import *

def captioning_inference(image_path):
    pass



def main(image_path: str):
    """
    main pipeline
    params:
    image_path: path to the image uploaded by the user
    """
    
    image_caption = captioning_inference(image_path)


    # question template
    
    question_generator = QuestionGenerator(generate_objects=True)
    doc = question_generator.parser.nlp(image_caption)

    verbs, nps = question_generator.parse_caption(image_caption)

    if question_generator.gen_obj:
        # get subject np
        subj = question_generator.parser.get_subj_np(nps)

        # generate objects
        word_parser = Word_parser()
        obj = word_parser.get_objects(str(verbs[0]))

        if obj:
            nps = [subj]+obj

    # get template for question
    template, nps = question_generator.choose_template(verbs, nps)

    # fill template
    question = question_generator.fill_template(template, verbs, nps)

    # passing question to gpt-2 and getting answer
