## code for main workflow where following steps with take place
## input path will be passed 
## calling image captioning module to generate caption
## passing image caption to a model to extract entities
## passing entities and getting question from rule based question generation module
## passing the question to the joke generation module and getting the joke, which will be returned
## This file will be calling all of our model one by one



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


    # passing question to gpt-2 and getting answer


