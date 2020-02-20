from __future__ import absolute_import, division, print_function

import tensorflow as tf

tf.compat.v1.enable_eager_execution()

# print("Is there a GPU available: "),
# print(tf.test.is_gpu_available())

# x = tf.random_uniform([3, 3])
# print("Is the Tensor on GPU #0:  "),
# print(x.device.endswith('GPU:0'))
import time

def time_matmul(x):
  start = time.time()
  for loop in range(10):
    tf.matmul(x, x)

  result = time.time()-start

  print("10 loops: {:0.2f}ms".format(1000*result))


# Force execution on CPU
print("On CPU:")
with tf.device("CPU:0"):
  x = tf.random_uniform([1000, 1000])
  assert x.device.endswith("CPU:0")
  time_matmul(x)

# Force execution on GPU #0 if available
if tf.test.is_gpu_available():
  with tf.device("GPU:0"): # Or GPU:1 for the 2nd GPU, GPU:2 for the 3rd etc.
    x = tf.random_uniform([1000, 1000])
    assert x.device.endswith("GPU:0")
    time_matmul(x)