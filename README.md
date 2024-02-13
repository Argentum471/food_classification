Flask app anf tg bot for food classification

First, load the models
https://drive.google.com/drive/folders/1P1h7bcjNZuFKtavjYokkzPebYxdHpE56?usp=sharing


Build application
```bash
$ https://github.com/Argentum471/food_classification.git
$ docker-compose up
```

Reuslts
| model    | top1 
|---------|-----|
| resnet18   | 0.73 
| resnet50d     | 0.82 
| tf_efficientnetv2_s.in1k| 0.8288


Training parameters
epochs: 100
optimizer: Adam
scheduler: ReduceLROnPlateau
lr: 3e-4 
