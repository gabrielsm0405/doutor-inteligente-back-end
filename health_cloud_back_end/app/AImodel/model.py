import numpy as np
import cv2
from ...settings import BASE_DIR, API_URL
from django.utils.crypto import get_random_string

from tensorflow.keras.applications.densenet import DenseNet121
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing import image
from tensorflow.keras import backend as K
from tensorflow.keras import models
from tensorflow import keras
import tensorflow as tf
from tensorflow.python.framework.ops import disable_eager_execution, enable_eager_execution

labels = [
    'Cardiomegaly', 
    'Emphysema', 
    'Effusion', 
    'Hernia', 
    'Infiltration', 
    'Mass', 
    'Nodule', 
    'Atelectasis',
    'Pneumothorax',
    'Pleural_Thickening', 
    'Pneumonia', 
    'Fibrosis', 
    'Edema', 
    'Consolidation'
]

def get_mean_std_per_batch(image_path, H=320, W=320):
    sample_data = []
    for idx in range(0, 100):
        # path = image_dir + img
        sample_data.append(np.array(image.load_img(image_path, target_size=(H, W))))

    mean = np.mean(sample_data[0])
    std = np.std(sample_data[0])
    return mean, std

def load_image(img_path, preprocess=True, H=320, W=320):
    """Load and preprocess image."""    
    mean, std = get_mean_std_per_batch(img_path, H=H, W=W)

    x = image.load_img(img_path, target_size=(H, W))
    if preprocess:
        x -= mean
        x /= std
        x = np.expand_dims(x, axis=0)
    return x

def generate_grad_cam(image_path, input_model, image, cls, layer_name, H=320, W=320):
    """GradCAM method for visualizing input saliency."""
    with tf.GradientTape() as gtape:
        conv_layer = input_model.get_layer(layer_name)
        heatmap_model = models.Model([input_model.inputs], [conv_layer.output, input_model.output])
        conv_output, predictions = heatmap_model(image)
        loss = predictions[0, cls]
        grads = gtape.gradient(loss, conv_output)[0, :, :, :]
        pooled_grads = np.mean(grads, axis=(0, 1))

    cam = np.dot(conv_output[0, :], pooled_grads)

    originalImage = cv2.imread(image_path)

    cam = cv2.resize(cam, (originalImage.shape[1], originalImage.shape[0]), cv2.INTER_LINEAR)
    cam = np.maximum(cam, 0)
    cam = cam / cam.max()
    
    resultImageName = "heatmap"+str(cls)+get_random_string(length=20, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVXWXYZ0123456789')+".png"

    cv2.imwrite('./images/'+resultImageName, 255*cam)
    heatmapImage = cv2.imread('./images/'+resultImageName)
    heatmapImage = cv2.applyColorMap(heatmapImage, cv2.COLORMAP_JET)
    result = cv2.addWeighted(heatmapImage, 0.7, originalImage, 0.3, 0)
    cv2.imwrite('./images/'+resultImageName, result)

    result_link = API_URL+"images/"+resultImageName

    return result_link

def get_results(image_path):
    base_model = DenseNet121(weights='imagenet', include_top=False)
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    predictions = Dense(len(labels), activation="sigmoid")(x)
    model = Model(inputs=base_model.input, outputs=predictions)
    model.load_weights(BASE_DIR+"/health_cloud_back_end/app/AImodel/pretrained_model.h5")

    preprocessed_input = load_image(image_path)
    predictions = model.predict(preprocessed_input)[0]

    results = []
    for label in labels:
        cam = generate_grad_cam(image_path, model, preprocessed_input, labels.index(label), 'bn')
        results.append(
            {"heatmap_link": cam, "prediction": str(predictions[labels.index(label)]), "pathology": label}
        )
        
    return results