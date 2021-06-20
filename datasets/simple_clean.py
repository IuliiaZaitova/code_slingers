from better_profanity import profanity
import csv


def get_joke(jokes, start="why"):
    
    '''  
    Function to get all jokes that start in a specific way.
    
    Arguments:
    * jokes - list of all jokes
    * start - the start of the joke (default: "why" bc that's our primary type)
    
    Returns:
    * select_jokes - (list) subset of all jokes that start in a particular way
    
    '''
    
    select_jokes = []
    for joke in jokes:
        if joke.lower().startswith(start):
            select_jokes.append(joke)
    return select_jokes


def clean_offensive(why):
    
    
    '''
    
    Simple function that cleans a dataset of profound and offensive jokes.
    
    Arguments:
    * why - dataset (list of s)
    
    
    Returns:
    * None
    '''
    
    
    nonos = [' jew', 'gay', 'homosexual', 'africa', 'chinese', 'mexican', ' mexic', ' latino', ' hispanic', 'black man', 'black woman', 'asian', 'muslim']
#     nos = []
    for joke in why:
        if any(el in joke.lower() for el in nonos) or profanity.contains_profanity(joke):
#             nos.append(joke)
            why.remove(joke)
    
    
# rows = []
# with open('./shortjokes.csv', 'r') as csvfile:
#     csvreader = csv.reader(csvfile)
#     fields = next(csvreader)
#     for row in csvreader:
#         rows.append(row)
        
# #      Get all jokes:   
# jokes = [] # all jokes
# for el in rows:
#     jokes.append(el[1])

# print('here')
# #     Get why jokes and clean them
# why = get_joke(jokes,start="why")
# clean_offensive(why)