import onnxruntime as ort
import numpy as np
import cv2 as cv


class ClassifierWrapper:
    def __init__(self, config):
        self.session = ort.InferenceSession(config["MODEL_PATH"],
                                            providers=[
                                                'CPUExecutionProvider']
                                            )
        self.session.set_providers(['CPUExecutionProvider'])
        self.input_names = [na.name for na in self.session.get_inputs()]
        self.output_names = [na.name for na in self.session.get_outputs()]
        self.img_size = tuple(self.session.get_inputs()[0].shape[-1:-3:-1])
        self.labels = config["LABELS"]

    def predict(self, *x):
        assert len(x) == len(self.input_names), \
            (f"Inconsistent number of inputs. "
             f"Got {len(x)}, epected {len(self.input_names)}")

        inputs_dict = {k: v for k, v in zip(self.input_names, x)}
        pred = self.session.run(None, inputs_dict)
        return pred

    def preprocess(self, img):
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        img = cv.resize(img, self.img_size)
        img = np.transpose(img, (2, 0, 1))
        img = np.expand_dims(img, 0)
        return img

    def __call__(self, img):
        img = self.preprocess(img)
        probabilities = self.predict(img)[0]
        sorted_probs = sorted(probabilities, reverse=True)
        top5_probs_list = sorted_probs[:5]
        top5_classes_list = sorted(range(len(probabilities)), key=lambda i: probabilities[i], reverse=True)[:5]
        top5_labels = [self.labels[class_idx] for class_idx in top5_classes_list]
        results = [(label, round(prob, 3)) for label, prob in zip(top5_labels, top5_probs_list)]
        return results
