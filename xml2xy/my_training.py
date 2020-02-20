# TensorFlow and tf.keras
import matplotlib.pyplot as plt
# Helper libraries
import numpy as np
import os
import pathlib
import tensorflow as tf
from tensorflow import keras
# Default Python Libraries
from time import sleep, time

print(tf.__version__)

# read cell data
true_sample, true_label  = np.load('true_sample_01.npy'), np.load('true_imlabel_01.npy')
false_sample, false_label = np.load('false_sample_01.npy'), np.load('false_imlabel_01.npy')
print(len(true_label),len(false_label))
# split true and false into train and test sets
true_index, false_index = np.array(range(len(true_label))), np.array(range(len(false_label)))

np.random.shuffle(true_index)
np.random.shuffle(false_index)
cutratio =0.8
truecut=int(cutratio*len(true_label))
falsecut=int(cutratio*len(false_label))
true_train_sample, true_test_sample = true_sample[true_index[:truecut]], true_sample[true_index[truecut:]]
true_train_label, true_test_label = true_label[true_index[:truecut]], true_label[true_index[truecut:]]
false_train_sample, false_test_sample = false_sample[false_index[:falsecut]], false_sample[false_index[falsecut:]]
false_train_label, false_test_label = false_label[false_index[:falsecut]], false_label[false_index[falsecut:]]

# merge true and false into train and test set
train_sample,train_label = np.concatenate((true_train_sample,false_train_sample)),np.concatenate((true_train_label,false_train_label))
test_sample, test_label = np.concatenate((true_test_sample,false_test_sample)), np.concatenate((true_test_label,false_test_label))

# shuffle train and test sets
train_index, test_index = np.array(range(len(train_label))), np.array(range(len(test_label)))
np.random.shuffle(train_index)
np.random.shuffle(test_index)
train_sample,test_sample = train_sample[train_index], test_sample[test_index]
train_label,test_label = train_label[train_index], test_label[test_index]
train_label[train_label=='cell']=0
train_label[train_label=='notcell']=1
test_label[test_label=='cell']=0
test_label[test_label=='notcell']=1
# name my label
cell_names = ['cell','notcell']

# my rgb2grey
train_sample = train_sample / 255.0
test_sample = test_sample / 255.0

# my layer
mymodel = keras.Sequential([
    keras.layers.Flatten(input_shape=(31, 31)),
    keras.layers.Dense(512, activation=tf.nn.relu),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(512, activation=tf.nn.relu),
    keras.layers.Dense(2, activation=tf.nn.softmax)
])

# build mymodel
mymodel.compile(optimizer=tf.train.AdamOptimizer(), 
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# define checkpoint path
checkpoint_path = "training_3/cp-{epoch:04d}.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)
# Create checkpoint callback # Save weights, every 5-epochs.
cp_callback = tf.keras.callbacks.ModelCheckpoint(
	checkpoint_path, save_weights_only=True, verbose=1, period=100)

## load weight
#Sort the checkpoints by modification time.
# checkpoints = pathlib.Path(checkpoint_dir).glob("*.index")
# checkpoints = sorted(checkpoints, key=lambda cp:cp.stat().st_mtime)
# checkpoints = [cp.with_suffix('') for cp in checkpoints]
# latest = str(checkpoints[-1])
# mymodel.load_weights(latest)
# loss, acc = mymodel.evaluate(test_sample, test_label)
# print("Restored model, accuracy: {:5.2f}%".format(100*acc))

# train my model uncomment here to train
mymodel.fit(train_sample, train_label, epochs= 10000, callbacks = [cp_callback])

# evaluate my accu
my_test_loss, my_test_acc = mymodel.evaluate(test_sample, test_label)
print('My test accuracy:', my_test_acc)

# my predict
my_predictions = mymodel.predict(test_sample)

# Plot the first 25 test images, their predicted label, and the true label
# Color correct predictions in green, incorrect predictions in red
plt.figure(figsize=(10,10))
for j in range(50):
    plt.subplot(5,10,j+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid('off')
    plt.imshow(test_sample[j], cmap=plt.cm.binary)
    my_predicted_label = np.argmax(my_predictions[j])
    my_correct_label = int(test_label[j])
    if my_predicted_label == my_correct_label:
      color = 'green'
    else:
      color = 'red'
    plt.xlabel("{} ({})".format(cell_names[my_predicted_label], 
                                  cell_names[my_correct_label]),
                                  color=color)

plt.show()
