import cv2
import numpy as np

def group_contours(contours, tolerance=0.2, min_group_size=3):
    groups = []
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        group = [contour]
        for j, contour2 in enumerate(contours):
            if i != j:
                cx, cy, cw, ch = cv2.boundingRect(contours[j])
                mean_h = sum(cv2.boundingRect(c)[3] for c in group) / len(group)
                mean_w = sum(cv2.boundingRect(c)[2] for c in group) / len(group)
                mean_center_y = sum((cv2.boundingRect(c)[1] + cv2.boundingRect(c)[3]) / 2.0 for c in group) / len(group)
                current_center_y = ((cy + ch) / 2.0)
                mean_area = sum(cv2.contourArea(c) for c in group) / len(group)
                current_area = cv2.contourArea(contours[j])

                if (abs(ch - mean_h) / mean_h < 0.2 and
                    abs(cw - mean_w) / mean_w < 0.5 and
                    abs(current_center_y - mean_center_y) / mean_h < 0.2 and
                    abs(current_area - mean_area) / mean_area < 0.5): #0.65
                    group.append(contour2)

        groups.append(group)

    # Merge intersecting bounding rectangles into single groups
    merged_groups = []
    for group in groups:
        if len(group) >= min_group_size:
            # Ensure all contours in the group are non-empty before merging
            non_empty_contours = [c for c in group if len(c) > 0]
            if non_empty_contours:
                merged_rect = cv2.boundingRect(np.vstack(non_empty_contours))
                merged_groups.append(merged_rect)

    # Further merge groups if their bounding rectangles intersect
    final_groups = []
    while merged_groups:
        rect1 = merged_groups.pop(0)
        x1, y1, w1, h1 = rect1
        merge_occurred = False
        for i, rect2 in enumerate(merged_groups):
            x2, y2, w2, h2 = rect2
            if (x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2):
                # Merge rect1 and rect2 into a single rectangle
                new_x = min(x1, x2)
                new_y = min(y1, y2)
                new_w = max(x1 + w1, x2 + w2) - new_x
                new_h = max(y1 + h1, y2 + h2) - new_y
                merged_groups[i] = (new_x, new_y, new_w, new_h)
                merge_occurred = True
                break
        if not merge_occurred:
            final_groups.append(rect1)

    return final_groups

def colorize_image(image, cluster_centers, labels):
    colorized_image = np.zeros_like(image, dtype=np.uint8)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            cluster_index = labels[i, j]
            colorized_image[i, j] = int(cluster_centers[cluster_index][0])

    return colorized_image