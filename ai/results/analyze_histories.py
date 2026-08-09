import json
import os

models = ['improved_cnn', 'mobilenet_v2', 'efficientnet_b0']
base_path = 'C:/Users/Lenovo/Desktop/VisionInspectIA/ai/results'

for model in models:
    history_path = os.path.join(base_path, model, 'history.json')
    if os.path.exists(history_path):
        with open(history_path) as f:
            history = json.load(f)
        
        print(f'=== {model} ===')
        epochs_trained = len(history['loss'])
        print(f'  Epochs trained: {epochs_trained}')
        
        best_val_loss = min(history['val_loss'])
        best_val_acc = max(history['val_accuracy'])
        best_epoch = history['val_loss'].index(best_val_loss) + 1
        
        print(f'  Best val loss: {best_val_loss:.4f} at epoch {best_epoch}')
        print(f'  Best val accuracy: {best_val_acc:.4f}')
        print(f'  Final train accuracy: {history["accuracy"][-1]:.4f}')
        print(f'  Final val accuracy: {history["val_accuracy"][-1]:.4f}')
        print(f'  Final train loss: {history["loss"][-1]:.4f}')
        print(f'  Final val loss: {history["val_loss"][-1]:.4f}')
        print(f'  Train/Val accuracy gap: {abs(history["accuracy"][-1] - history["val_accuracy"][-1]):.4f}')
        print(f'  Train/Val loss gap: {abs(history["loss"][-1] - history["val_loss"][-1]):.4f}')
        print()
