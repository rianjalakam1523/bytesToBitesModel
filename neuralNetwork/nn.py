import tensorflow as tf
from tensorflow.keras import Sequential, Input
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, ReLU, Softmax

# AUTHOR: RIAN JALAKAM, FALL 2026

"""
This will remain at least mostly untouched until we have collected our training data. 
Our team will be taking pictures of the inventory within food banks and gradually organizing these images and labeling them before the training phase starts, to which the model will be run through ONNX.
The goal is to utilize TensorRT that comes with the NVIDIA Jetson Orin Nano.
Any updates will be testing theories.
"""

class EdgeCNN(tf.keras.Model):
    def __init__(self, num_classes: int = 3):
        super(EdgeCNN, self).__init__()
        
        # Feature extraction layers using explicit Input layer
        self.conv1 = Sequential([
            Input(shape=(64, 64, 3)),
            Conv2D(32, kernel_size=(3, 3), padding='same'),
            ReLU(),
            MaxPooling2D(pool_size=(2, 2))
        ])
        
        self.conv2 = Sequential([
            Conv2D(64, kernel_size=(3, 3), padding='same'),
            ReLU(),
            MaxPooling2D(pool_size=(2, 2))
        ])
        
        # Classification head
        self.flatten = Flatten()
        self.fc1 = Dense(128)
        self.relu3 = ReLU()
        self.classifier = Dense(num_classes)
        self.softmax = Softmax()

    def call(self, inputs):
        x = self.conv1(inputs)
        x = self.conv2(x)
        x = self.flatten(x)
        x = self.fc1(x)
        x = self.relu3(x)
        x = self.classifier(x)
        return self.softmax(x)

if __name__ == "__main__":
    print("--- 1. Loading Dataset ---")
    batch_size = 32
    img_height = 64
    img_width = 64
    
    train_ds = tf.keras.utils.image_dataset_from_directory(
        "dataset/train",
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size
    )
    
    val_ds = tf.keras.utils.image_dataset_from_directory(
        "dataset/train",
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size
    )
    
    class_names = train_ds.class_names
    num_classes = len(class_names)
    print(f"Found classes: {class_names} (Total: {num_classes})")

    # Normalize pixel values from [0, 255] down to [0.0, 1.0] for stable training
    normalization_layer = tf.keras.layers.Rescaling(1./255)
    train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
    val_ds = val_ds.map(lambda x, y: (normalization_layer(x), y))

    # Optimize dataset performance with prefetching
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    print("--- 2. Initializing and Compiling Model ---")
    model = EdgeCNN(num_classes=num_classes)
    
    model.compile(
        optimizer='adam', # Utilize an Adaptive Moment Estimation optimizer to adjust learning rates dynamically
        loss='sparse_categorical_crossentropy',  # Use sparse since labels come as integers from directory loader
        metrics=['accuracy']
    )

    print("--- 3. Training Model ---")
    epochs = 10
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs
    )

    print("--- 4. Saving Model for TensorRT Export ---")
    export_path = "saved_edge_cnn_model.keras"
    model.save(export_path)
    print(f"Model successfully trained and saved to '{export_path}'!")
