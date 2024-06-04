# drAIve
This repository contains "drAIve", the swaggest drive assistant in the street. This is a project for the AiLab course (2023-2024 a.y)


## SetUp
We will use a virtual environment
```bash
python -m venv env
```
active the virtual environment
- macOS
    ```
    source env/bin/activate
    ```
- Windows
    ```
    myenv\Scripts\activate
    ```
Install ultralytics to use YOLO
```sh
pip install ultralytics
```
Install sklearn to use Kmeans
```sh
pip install scikit-learn
```

## Datasets
- [Crosswalks](https://universe.roboflow.com/lr-tdx/road-mark/browse?queryText=-class%3A%22BUS+LANE%22+-class%3A%22Jeltaya+razmetka%22+-class%3ALiniya+-class%3ALiniya-2+-class%3ALiniya-3+-class%3Anull+-class%3ARomb+-class%3ASLOW+-class%3A%22Strelka+vlevo%22+-class%3A%22Strelka+vpered%22+-class%3A%22Strelka+vpered+%2B+vlevo%22+-class%3A%22Strelka+vpered+%2B+vpravo%22+-class%3A%22Strelka+vpravo%22+-class%3AVelosiped+class%3APerehod&pageSize=50&startingIndex=0&browseQuery=true)

- [Road signs](https://www.kaggle.com/datasets/andrewmvd/road-sign-detection)
