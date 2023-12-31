from tensorflow.keras.layers import Conv2D, Activation, UpSampling2D, Dense
from tensorflow.keras.layers import Input, Flatten, Reshape
from tensorflow.keras.models import Model
import numpy as np


def CNN_AUTOENCODER(input_shape, latent_dimension=128, mode='full'):
    """Auto-encoder model for latent-pose reconstruction.
    # Arguments
        input_shape: List of integers, indicating the initial tensor shape.
        latent_dimension: Integer, value of the latent vector dimension.
        mode: String {`full`, `encoder`, `decoder`}.
            If `full` both encoder-decoder parts are returned as a single model
            If `encoder` only the encoder part is returned as a single model
            If `decoder` only the decoder part is returned as a single model
    """

    if mode not in ['full', 'encoder', 'decoder']:
        raise ValueError('Invalid mode.')

    i = Input(input_shape, name='image')
    x = Conv2D(32, (3, 3), strides=(2, 2), padding='same', name='conv2D_1')(i)
    x = Activation('relu', name='relu_1')(x)
    x = Conv2D(64, (3, 3), strides=(2, 2), padding='same', name='conv2D_2')(x)
    x = Activation('relu', name='relu_2')(x)
    x = Conv2D(128, (3, 3), strides=(2, 2), padding='same', name='conv2D_3')(x)
    x = Activation('relu', name='relu_3')(x)
    x = Conv2D(256, (3, 3), strides=(2, 2), padding='same', name='conv2D_4')(x)
    convolution_shape = np.array(x.shape[1:])
    x = Activation('relu', name='relu_4')(x)
    x = Flatten(name='flatten_1')(x)

    z = Dense(latent_dimension, name='latent_vector')(x)

    if mode == 'decoder':
        z = Input(shape=(latent_dimension, ), name='input')
    x = Dense(np.prod(convolution_shape), name='dense_1')(z)
    x = Reshape(convolution_shape, name='reshape_1')(x)
    x = UpSampling2D((2, 2), name='upsample_1')(x)
    x = Conv2D(128, (3, 3), padding='same', name='conv2D_5')(x)
    x = Activation('relu', name='relu_5')(x)
    x = UpSampling2D((2, 2), name='upsample_2',)(x)
    x = Conv2D(64, (3, 3), padding='same', name='conv2D_6')(x)
    x = Activation('relu', name='relu_6')(x)
    x = UpSampling2D((2, 2), name='upsample_3')(x)
    x = Conv2D(32, (3, 3), padding='same', name='conv2D_7')(x)
    x = Activation('relu', name='relu_7')(x)
    x = UpSampling2D((2, 2), name='upsample_4')(x)
    x = Conv2D(input_shape[-1], (3, 3), padding='same', name='conv2D_8')(x)
    output_tensor = Activation('sigmoid', name='label')(x)
    base_name = 'CNN-AUTOENCODER-' + str(latent_dimension)
    if mode == 'encoder':
        name = base_name + '-encoder'
        model = Model(i, z, name=name)

    elif mode == 'decoder':
        name = base_name + '-decoder'
        model = Model(z, output_tensor, name=name)

    elif mode == 'full':
        model = Model(i, output_tensor, name=base_name)

    return model


if __name__ == "__main__":
    model = CNN_AUTOENCODER((32, 32, 3))
    model.summary()
