import torch
import albumentations as A
import timm
import yaml
from albumentations.pytorch import ToTensorV2
import cv2
import torch.nn.functional as F


class ClassificationWrapper:
    def __init__(self, config):
        self.labels = config["LABELS"]
        self.model_path = config["MODEL_PATH"]
        self.model = self.load_chkpt()
        self.transforms = A.Compose([
            A.Resize(224, 224),
            A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
            ToTensorV2(),
        ])

    def load_chkpt(self):
        ckpt = self.model_path
        model = timm.create_model('resnet18', num_classes=101, pretrained=False).eval()
        checkpoint = torch.load(ckpt, map_location='cpu')
        model.load_state_dict(checkpoint)
        model.eval()
        return model

    def predict(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        transformed_image = self.transforms(image=image)["image"]
        input_tensor = torch.tensor(transformed_image).unsqueeze(0)
        with torch.no_grad():
            output = self.model(input_tensor)
        probabilities = F.softmax(output, dim=1)
        top5_probs, top5_classes = torch.topk(probabilities, 5)

        top5_probs_list = top5_probs.squeeze().tolist()
        top5_classes_list = top5_classes.squeeze().tolist()

        # Map class indices to labels
        top5_labels = [self.labels[class_idx] for class_idx in top5_classes_list]
        results = [(label, round(prob, 3)) for label, prob in zip(top5_labels, top5_probs_list)]
        return results