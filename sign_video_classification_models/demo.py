"""
Given a video path and a saved model (checkpoint), produce classification
predictions.

Note that if using a model that requires features to be extracted, those
features must be extracted first.

Note also that this is a rushed demo script to help a few people who have
requested it and so is quite "rough". :)
"""
from keras.models import load_model
from data2 import DataSet
import numpy as np

def predict(data_type, seq_length, saved_model, image_shape, video_name, class_limit):
    model = load_model(saved_model)

    for i_video in video_name:
        # print('Ground Truth:', i_video)
        # Get the data and process it.
        if image_shape is None:
            data = DataSet(seq_length=seq_length, class_limit=class_limit)
        else:
            data = DataSet(seq_length=seq_length, image_shape=image_shape,
                class_limit=class_limit)

        # Extract the sample from the data.
        sample = data.get_frames_by_filename(i_video, data_type)

        # Predict!
        prediction = model.predict(np.expand_dims(sample, axis=0))
        # print(prediction)
        data.print_class_from_prediction(np.squeeze(prediction, axis=0))

        print('-------------------------')

def main():
    # model can be one of lstm, lrcn, mlp, conv_3d, c3d.
    model = 'lrcn'
    saved_model = 'data/checkpoints/lrcn-images.059-0.479.hdf5'

    #model = 'lstm'
    #saved_model = 'data/checkpoints/lstm-features.041-0.567.hdf5'
    # Sequence length must match the lengh used during training.
    seq_length = 80
    # Limit must match that used during training.
    class_limit = None

    # Demo file. Must already be extracted & features generated (if model requires)
    # Do not include the extension.
    # Assumes it's in data/[train|test]/
    # It also must be part of the train/test data.
    # TODO Make this way more useful. It should take in the path to
    # an actual video file, extract frames, generate sequences, etc.
    # video_name = 'v_Archery_g04_c02'

    video_name = ['CUTE_1','CUTE_2', 'DRESS-CLOTHES_3', 'EAT_1', 'EXCUSE_3', 'FIFTH_3', 'ART-DESIGN_3', 'SAME_1']


    # Chose images or features and image shape based on network.
    if model in ['conv_3d', 'c3d', 'lrcn']:
        data_type = 'images'
        image_shape = (200, 200, 3)
    elif model in ['lstm', 'mlp']:
        data_type = 'features'
        image_shape = None
    else:
        raise ValueError("Invalid model. See train.py for options.")

    predict(data_type, seq_length, saved_model, image_shape, video_name, class_limit)

if __name__ == '__main__':
    main()
