from app.classifier.src.onnx_predictor import ClassifierWrapper
import yaml
SYSTEM_CONFIG_PATH = './app/classifier/src/config.yaml'
with open(SYSTEM_CONFIG_PATH, 'r') as f:
    config = yaml.safe_load(f)
classification_wrapper = ClassifierWrapper(config)

