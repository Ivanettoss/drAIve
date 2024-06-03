from split_dataset import split_dataset
from normalize_annotation import normalize_annotation

if __name__ == "__main__":
    '''
    We start with an XML annotation which is not suitable for YOLO,
    so we convert it into the right annotation format.
    '''
    normalize_annotation("./road_sign/dataset/annotations", "./road_sign/dataset/labels")

    '''
    Then we have to divide the dataset into training, test, and validation sets. 
    For YOLO, we decide to use an 80/10/10 split, following best practices and paying 
    attention to class distribution.
    '''
    split_dataset("./road_sign/dataset/images", "./road_sign/dataset/labels")
