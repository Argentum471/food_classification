from dataclasses import dataclass

@dataclass
class PredictResponse:
    img_path: str
    predict: bool
    top_predictions: dict
