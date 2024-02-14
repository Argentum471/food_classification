Flask app and tg bot for food classification

First, load the models
https://drive.google.com/drive/folders/1P1h7bcjNZuFKtavjYokkzPebYxdHpE56?usp=sharing


Build application
```bash
$ https://github.com/Argentum471/food_classification.git
$ docker-compose up
```

Bot: https://t.me/GastronomyGeniusBot

If you have .env, put it in root

Reuslts
| model    | top1 
|---------|-----|
| resnet18   | 0.73 
| resnet50d     | 0.82 
| tf_efficientnetv2_s.in1k| 0.88


Training parameters
| Parameter | Value            |
|-----------|------------------|
| epochs    | 100              |
| optimizer | Adam             |
| scheduler | ReduceLROnPlateau|
| lr        | 3e-4             |



How to improve
1. more epochs
2. more data for worst classes
3. new architecture
4. more specified augmentations
   
