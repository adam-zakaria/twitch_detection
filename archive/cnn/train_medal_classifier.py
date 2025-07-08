# train_medal_classifier.py

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
import os

# Directory structure:
# data/
#   train/
#     double_kill/   # positive examples
#     no_double_kill/      # negative examples
#   val/
#     double_kill/   # validation positives
#     no_double_kill/      # validation negatives
#   test/
#     double_kill/   # test positives
#     no_double_kill/      # test negatives

data_dir    = "/Users/azakaria/Code/twitch_detections/test/frames/data"
batch_size  = 32
#num_epochs  = 10
num_epochs  = 2
num_classes = 2
device      = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Checkpoint path
checkpoint_path = "medal_classifier.pth"

# Data transforms
train_transform = transforms.Compose([
    transforms.Resize((96, 96)),
    transforms.RandomHorizontalFlip(),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485,0.456,0.406],
                         std=[0.229,0.224,0.225])
])
val_transform = transforms.Compose([
    transforms.Resize((96, 96)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485,0.456,0.406],
                         std=[0.229,0.224,0.225])
])

# Datasets and loaders
train_dataset = datasets.ImageFolder(
    os.path.join(data_dir, "train"),
    transform=train_transform
)
val_dataset = datasets.ImageFolder(
    os.path.join(data_dir, "val"),
    transform=val_transform
)
test_dataset = datasets.ImageFolder(
    os.path.join(data_dir, "test"),
    transform=val_transform
)

train_loader = torch.utils.data.DataLoader(
    train_dataset, batch_size=batch_size, shuffle=True
)
val_loader = torch.utils.data.DataLoader(
    val_dataset, batch_size=batch_size
)
test_loader = torch.utils.data.DataLoader(
    test_dataset, batch_size=batch_size
)

# Model: MobileNetV2 backbone + classifier head
model = models.mobilenet_v2(pretrained=True)
#model = models.mobilenet_v2(weights=MobileNet_V2_Weights.IMAGENET1K_V1)

model.classifier[1] = nn.Linear(
    model.classifier[1].in_features,
    num_classes
)
model = model.to(device)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-4)

# Try to load existing checkpoint to avoid unnecessary retraining
start_epoch = 0
if os.path.exists(checkpoint_path):
    checkpoint = torch.load(checkpoint_path, map_location=device)
    model.load_state_dict(checkpoint["model_state_dict"])
    optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
    start_epoch = checkpoint.get("epoch", 0)
    print(f"Loaded checkpoint from {checkpoint_path}. Skipping training.")

# Training loop – only if we did not load a completed checkpoint
if start_epoch == 0:
    for epoch in range(num_epochs):
        model.train()
        total_loss = 0.0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        avg_loss = total_loss / len(train_loader)
        print(f"Epoch {epoch+1}/{num_epochs} - Training Loss: {avg_loss:.4f}")

        # Validation
        model.eval()
        correct = 0
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                preds = outputs.argmax(dim=1)
                correct += (preds == labels).sum().item()
        val_acc = correct / len(val_dataset)
        print(f"Epoch {epoch+1}/{num_epochs} - Validation Accuracy: {val_acc:.4f}")

    # Save checkpoint after training completes
    torch.save({
        "epoch": num_epochs,
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
    }, checkpoint_path)
    print(f"Checkpoint saved to {checkpoint_path}")

else:
    print("Model loaded – proceeding directly to evaluation and export.")

# Final test evaluation
model.eval()
correct = 0
with torch.no_grad():
    for images, labels in test_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        preds = outputs.argmax(dim=1)
        correct += (preds == labels).sum().item()
test_acc = correct / len(test_dataset)
print(f"Test Accuracy: {test_acc:.4f}")

# Export to ONNX for CPU inference
dummy_input = torch.randn(1, 3, 96, 96).to(device)
try:
    torch.onnx.export(
        model,
        dummy_input,
        "medal_classifier.onnx",
        input_names=["input"],
        output_names=["output"],
        opset_version=11,
    )
    print("ONNX model saved as medal_classifier.onnx")
except Exception as e:
    print(f"Failed to export ONNX model: {e}\nThe trained weights are saved at {checkpoint_path}; you can rerun export without retraining.")
