import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from ollama import chat
from ollama import ChatResponse

_model = None 
def load_model_lazy():
    global _model
    if _model is None:
        try:
            _model = load_model('dermdude.keras')
            print("Model loaded successfully")  # Debugging
        except Exception as e:
            print(f"Error loading model: {e}")
            raise  # Re-raise the exception
    return _model

def predict_image(img_path,description):
    print(img_path)
    print(description)
    img = image.load_img(img_path, target_size=(300, 300))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.  # Normalize
    
    model = load_model_lazy()

    prediction = model.predict(img_array)
    
    class_index = np.argmax(prediction[0])
    
    class_names = [
    'Acne and Rosacea Photos',
 'Actinic Keratosis Basal Cell Carcinoma and other Malignant Lesions',
 'Atopic Dermatitis Photos',
 'Bullous Disease Photos',
 'Cellulitis Impetigo and other Bacterial Infections',
 'Eczema Photos',
 'Exanthems and Drug Eruptions',
 'Hair Loss Photos Alopecia and other Hair Diseases',
 'Herpes HPV and other STDs Photos',
 'Light Diseases and Disorders of Pigmentation',
 'Lupus and other Connective Tissue diseases',
 'Melanoma Skin Cancer Nevi and Moles',
 'Nail Fungus and other Nail Disease',
 'Poison Ivy Photos and other Contact Dermatitis',
 'Psoriasis pictures Lichen Planus and related diseases',
 'Scabies Lyme Disease and other Infestations and Bites',
 'Seborrheic Keratoses and other Benign Tumors',
 'Systemic Disease',
 'Tinea Ringworm Candidiasis and other Fungal Infections',
 'Urticaria Hives',
 'Vascular Tumors',
 'Vasculitis Photos',
 'Warts Molluscum and other Viral Infections']
    predicted_class = class_names[class_index]

    ollama_response = guided_response_ollama(description,predicted_class)
    return predicted_class, ollama_response

def guided_response_ollama(description,predicted_class):
    response: ChatResponse = chat(model='llama3:latest', messages=[
  {
    'role': 'user',
    'content': 'You are given a description of a skin condition. You are also given a likely condition,' + predicted_class +' that has been diagnosed using a machine learning model. You are to provide a response to the user based on a description of the likely condition. This likely condition is absolute and you are not to give another diagnosis and to abide by the other three parts of this answer according to the diagnosis, excluding the three alternate conditions. This response will be segregated in three parts: Description of condition, Treatment and prevention of condition, and finally when to see a doctor. Finally, you are to make three other possible skin condition to the user purely based on the description of the condition purely based on the description alone, that is not the likely condition that we provided to the user, which acts as alternate conditions that the user should be aware of. Label each part of your response accordingly. Use ** to bold text and \n to line break. This is the description from the user: ' + description + 'The likely condition is: '+predicted_class,
  },
  
])  
    bolded = 0
    output = response.message.content
    output = output.replace('\n', '<br />')
    while "**" in output:
        if bolded % 2 == 0:
            output = output.replace("**", "<b>", 1)
        elif bolded % 2 == 1:
            output = output.replace("**", "</b>", 1)
        bolded += 1
    print(output)
    
    return output