"""
Building a Brain - Fashion MNIST (Pure NumPy + Standard Library ONLY)
Perfect beginner ML project for minipythonprojects repo!

Showcases: urllib download, gzip parsing, NumPy math from scratch,
gradient descent, matplotlib, interactive input.

"""

import numpy as np
import matplotlib.pyplot as plt
import urllib.request
import gzip
import os

# ====================== DOWNLOAD & LOAD DATA ======================
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']


def download_file(url, filename):
    if not os.path.exists(filename):
        print(f"Downloading {filename} (~25 MB)...")
        urllib.request.urlretrieve(url, filename)


base_url = "http://fashion-mnist.s3-website.eu-central-1.amazonaws.com/"
files = {
    "train_images": "train-images-idx3-ubyte.gz",
    "train_labels": "train-labels-idx1-ubyte.gz",
    "valid_images": "t10k-images-idx3-ubyte.gz",
    "valid_labels": "t10k-labels-idx1-ubyte.gz"
}

for name, fname in files.items():
    download_file(base_url + fname, fname)


def load_images(filename):
    with gzip.open(filename, 'rb') as f:
        data = np.frombuffer(f.read(), dtype=np.uint8, offset=16)
    return data.reshape(-1, 28, 28).astype('float32') / 255.0


def load_labels(filename):
    with gzip.open(filename, 'rb') as f:
        data = np.frombuffer(f.read(), dtype=np.uint8, offset=8)
    return data


print("Loading Fashion MNIST dataset...")
train_images = load_images("train-images-idx3-ubyte.gz")
train_labels = load_labels("train-labels-idx1-ubyte.gz")
valid_images = load_images("t10k-images-idx3-ubyte.gz")  # ← fixed
valid_labels = load_labels("t10k-labels-idx1-ubyte.gz")  # ← fixed

X_train = train_images.reshape(-1, 784)
X_valid = valid_images.reshape(-1, 784)

# Show example
plt.figure(figsize=(5, 5))
plt.imshow(train_images[42], cmap='gray')
plt.title(f"Example: {class_names[train_labels[42]]}")
plt.show()

print(f"Training images: {len(train_images)} | Validation: {len(valid_images)}")


# ====================== THE BRAIN (from scratch) ======================
class Brain:
    def __init__(self):
        self.W = np.random.randn(784, 10) * 0.01
        self.b = np.zeros(10)

    def softmax(self, z):
        exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))
        return exp_z / np.sum(exp_z, axis=1, keepdims=True)

    def forward(self, X):
        return X @ self.W + self.b

    def predict(self, X):
        return np.argmax(self.forward(X), axis=1)

    def train(self, X, y, epochs=5, lr=0.1):
        y_onehot = np.eye(10)[y]
        losses = []

        for epoch in range(epochs):
            logits = self.forward(X)
            probs = self.softmax(logits)
            loss = -np.mean(np.sum(y_onehot * np.log(probs + 1e-10), axis=1))
            losses.append(loss)

            grad = probs - y_onehot
            self.W -= lr * (X.T @ grad) / len(X)
            self.b -= lr * np.mean(grad, axis=0)

            print(f"Epoch {epoch + 1}/{epochs} - Loss: {loss:.4f}")

        return losses


print("\nTraining the brain (5 epochs)...")
brain = Brain()
losses = brain.train(X_train, train_labels, epochs=5, lr=0.1)

pred_valid = brain.predict(X_valid)
accuracy = np.mean(pred_valid == valid_labels)
print(f"\n✅ Brain trained! Validation accuracy: {accuracy:.1%}")

plt.figure(figsize=(6, 4))
plt.plot(losses, marker='o')
plt.title('Training Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.show()


# ====================== INTERACTIVE QUIZ ======================
def test_brain(idx):
    if idx < 0 or idx >= len(train_images):
        print("Index must be 0-59999!")
        return

    img = train_images[idx]
    plt.figure(figsize=(8, 4))
    plt.subplot(1, 2, 1)
    plt.imshow(img, cmap='gray')
    plt.title(f"Image #{idx}\nCorrect: {class_names[train_labels[idx]]}")

    logits = brain.forward(X_train[idx:idx + 1])
    probs = brain.softmax(logits)[0]
    predicted = np.argmax(probs)

    plt.subplot(1, 2, 2)
    plt.bar(range(10), probs)
    plt.xticks(range(10), class_names, rotation=45, ha='right')
    plt.title("Brain's Confidence")
    plt.tight_layout()
    plt.show()

    print(f"Correct  : {class_names[train_labels[idx]]}")
    print(f"Brain says: {class_names[predicted]} ({probs[predicted]:.1%})")
    print("-" * 50)


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🧠 BRAIN READY! Enter image index (0-59999)")
    print("Type -1 to quit")
    print("=" * 60)

    while True:
        try:
            inp = input("\nImage index: ").strip()
            if inp == "-1":
                print("Awesome! Add this to minipythonprojects 🎉")
                break
            test_brain(int(inp))
        except:
            print("Please enter a number or -1")