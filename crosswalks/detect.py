import cv2
import numpy as np
from sklearn.cluster import KMeans

from utils import colorize_image, group_contours

def process_image(img):
    # make ROI
    height, _ = img.shape[:2]
    roi = img[height // 3:, :]

    lab_img = cv2.cvtColor(roi, cv2.COLOR_BGR2LAB)
    l_channel, _, _ = cv2.split(lab_img)


    mean = np.mean(l_channel.flatten())

    l_channel_reshaped = l_channel.reshape(-1, 1)
    num_clusters = 3 if mean < 55 else 4 if mean < 75 else 5 if mean < 110 else 11

    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(l_channel_reshaped)

    cluster_centers = kmeans.cluster_centers_
    labels = kmeans.predict(l_channel_reshaped)
    labels = labels.reshape(l_channel.shape)

    #colorize the image based on the kmeans labels
    cluster_image = colorize_image(l_channel, cluster_centers, labels)
    max_value = np.max(cluster_image)

    # prepere for threshold
    max_mask = (cluster_image == max_value)

    # thresholding
    max_br_image = np.zeros_like(cluster_image)
    max_br_image[max_mask] = 255
    max_br_image[~max_mask] = 0

    # do Morphology to reduce the noise in and around possible crosswalks
    kernel = np.ones((3, 3), np.uint8)
    morph = cv2.morphologyEx(max_br_image, cv2.MORPH_OPEN, kernel)
    kernel = np.ones((5, 5), np.uint8)
    morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel)

    # find contours
    cntrs = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cntrs = cntrs[0] if len(cntrs) == 2 else cntrs[1]

    contours = roi.copy()
    good_contours = []

    for contour in cntrs:
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        x, y, w, h = cv2.boundingRect(approx)
        aspect_ratio = w / float(h)
        area = cv2.contourArea(contour)

        if 0.15 <= aspect_ratio <= 7 and h > 10 and 60 < area < 8000:
            good_contours.append(contour)
            cv2.drawContours(contours, [contour], -1, (0, 0, 255), 1)

    # Aggregate the groups that have an intersection between their boxes
    # The boxes of the groups are defined by taking the minimum x, minimum y, maximum x, and maximum y
    groups = group_contours(good_contours)

    result = roi.copy()
    for i, rect in enumerate(groups):
        x_min, y_min, w, h = rect

        # draw on the image applied with the roi
        cv2.rectangle(result, (x_min, y_min), (x_min + w, y_min + h), (0, 255, 0), 2)

        # save original image rectangle
        groups[i] = (x_min, y_min + height // 3, w, h)
    return ([roi, cluster_image, morph, contours, result], groups)