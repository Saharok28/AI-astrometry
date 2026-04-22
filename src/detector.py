import torch
import torchvision
from torchvision.models.detection import FasterRCNN_ResNet50_FPN_Weights


class AsteroidDetector:

    def __init__(self, model_path=None):
        self.model = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    def load_model(self, model_path=None):
        """Load pre-trained Faster R-CNN; fine-tune weights from model_path if given."""
        self.model = torchvision.models.detection.fasterrcnn_resnet50_fpn(
            weights=FasterRCNN_ResNet50_FPN_Weights.DEFAULT
        )
        self.model.to(self.device)
        self.model.eval()

    def predict(self, image_tensor):
        """Run inference on a [C, H, W] float32 tensor. Returns model prediction dicts."""
        if self.model is None:
            raise ValueError("Call load_model() first.")
        with torch.no_grad():
            return self.model([image_tensor.to(self.device)])
