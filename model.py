import pickle as pkl
import tensorflow as tf

def predict(user_input):

    # Loading models
    nlp_model = tf.keras.models.load_model('./model/nlp_model')
    reg_model = pkl.load(open('./model/model.pkl', 'rb'))
    
    # Word preprocessing
    ohe_docs = [tf.keras.preprocessing.text.one_hot(user_input[0], 51029)]
    pad_docs = tf.keras.preprocessing.sequence.pad_sequences(ohe_docs, maxlen=255, padding='post')
    user_input[0] = nlp_model.predict(pad_docs)

    # Price prediction
    return reg_model.predict([user_input])[0]
