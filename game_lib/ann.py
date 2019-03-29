import os
os.environ['TF_CPP_MIN_VLOG_LEVEL'] = '3'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tensorflow import logging
logging.set_verbosity(logging.INFO)

import numpy as np
from keras.models import Sequential
from keras.layers import Dense

# # # Generate dummy data
# x_train = np.random.random((1000, 12))
# y_data = np.random.randint(3, size=1000)
# y_train = keras.utils.to_categorical(np.random.randint(3, size=1000), num_classes=3)
# # x_test = np.random.random((100, 12))
# # y_test = keras.utils.to_categorical(np.random.randint(3, size=(100, 1)), num_classes=3)


def init_ann(weights):
    w1 = np.reshape(weights[:168], (12,14))
    w2 = np.reshape(weights[168:], (14,3))
    
    model = Sequential()
    layer1 = Dense(14, activation='relu', weights=[w1,w1[0]], input_dim=12)
    model.add(layer1)
    output_layer = Dense(3, activation='softmax', weights=[w2,w2[0]])
    model.add(output_layer)
    
    #sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy',
              #optimizer=sgd,
              optimizer='rmsprop',
              metrics=['accuracy'])

    model.summary()
    return model, layer1, output_layer

# Inputs should be given here.
def train(model, x_train, y_train):
    model.fit(x_train, y_train, epochs=20, batch_size=64, verbose=0)
    return model

# def model_test():
#     score = model.evaluate(x_test, y_test, batch_size=128)

# def get_weights(model):
#     model.

def predict(model, x):
    return model.predict(np.reshape(x, (1,12)))

def save_model(model):
    with open('winner.json', 'w') as fd:
        fd.write(model.to_json())

# sample_population = []
# sample_fitness = np.random.uniform(low=0.2, high=1.0, size=(10,))

# for i in range(0, 10):
#     sampl = np.random.uniform(low=0.2, high=1.0, size=(210,))
#     sample_population.append(sampl)

# weights = ga.createNewPopulation(sample_population, sample_fitness)
# # print(weights[0][:168])
# # weightz = np.reshape(weights[0][:168], (12,14))
# # print(np.shape(weightz))
# # print(np.shape(weightz[0]))

# model, layer1, output_layer = init_ann(weights[0])
# model = train(model, x_train, y_train)
# x = np.reshape(x_train[5], (1,12))
# y = predict(model, x)
# print(y)


