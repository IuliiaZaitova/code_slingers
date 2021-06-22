import gpt_2_simple as gpt2
import tensorflow as tf



Model_checkpoint = "output/joke_generation/"

def evaluation(test):
    
    tf.reset_default_graph()
    sess = gpt2.start_tf_sess()
    gpt2.load_gpt2(sess, run_name='run1')
    result = gpt2.generate(sess, run_name='run1', prefix='<soq>'+ test + '<eoq>', length=100, temperature=0.9, return_as_list=True)
    return result[0]


#print(evaluation("Why was a bunch of fruits and vegetables on a table watching"))



