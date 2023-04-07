import os
import sys

import cv2
import numpy as np


sys.path.append(os.path.dirname(__file__))

DETECTOR_NORMS_DICT = {
    "SIFT": (cv2.SIFT_create(), cv2.NORM_L2),
    "ORB": (cv2.ORB_create(), cv2.NORM_HAMMING),
    "AKAZE": (cv2.AKAZE_create(), cv2.NORM_HAMMING),
    "BRISK": (cv2.BRISK_create(), cv2.NORM_HAMMING),
}
FLANN_INDEX_KDTREE = 0
FLANN_INDEX_LSH = 6


def algorithm(left_image, right_image, detector_name: str = "SIFT"):
    left_image_gray = cv2.cvtColor(left_image, cv2.COLOR_BGR2GRAY)
    right_image_gray = cv2.cvtColor(right_image, cv2.COLOR_BGR2GRAY)

    F, kps1, kps2, matches, img1_draw, img2_draw, img_Keypoint_matches = \
        find_fundamental_matrix(left_image_gray, right_image_gray, detector_name)

    return kps1, kps2, matches, img1_draw, img2_draw, img_Keypoint_matches


def find_fundamental_matrix(img1, img2, detector_name: str = "SIFT", ratio: float = 0.6):
    all_kps1, all_kps2, matches, img1_draw, img2_draw, img_Keypoint_matches = \
        match_features(img1, img2, detector_name, ratio)
    kps1 = np.asarray([all_kps1[m.queryIdx].pt for m in matches])
    kps2 = np.asarray([all_kps2[m.trainIdx].pt for m in matches])

    num_keypoints = len(matches)
    if num_keypoints < 7:
        return None, kps1, kps2

    flag = cv2.FM_7POINT if num_keypoints == 7 else cv2.FM_8POINT

    F, mask = cv2.findFundamentalMat(kps1, kps2, flag)

    # get inlier keypoints
    kps1 = kps1[mask.ravel() == 1]
    kps2 = kps2[mask.ravel() == 1]

    return F, kps1, kps2, matches, img1_draw, img2_draw, img_Keypoint_matches


def match_features(img1, img2, detector_name: str = "SIFT", ratio: float = 0.6):
    assert img1.ndim == 2 and img1.dtype == np.uint8, "img1 is invalid"
    assert img2.ndim == 2 and img2.dtype == np.uint8, "img2 is invalid"

    keypoint_detector, keypoint_matcher = _init_detector_matcher(detector_name)

    kps1, des1 = keypoint_detector.detectAndCompute(img1, None)
    kps2, des2 = keypoint_detector.detectAndCompute(img2, None)
    matches = keypoint_matcher.knnMatch(des1, des2, k=2)

    img_draw_L = cv2.drawKeypoints(
        img1, kps1, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    img_draw_R = cv2.drawKeypoints(
        img1, kps1, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # matches = [m[0] for m in matches if len(m) == 2 and m[0].distance < ratio * m[1].distance]

    matches = [m[0] for m in matches if len(m) == 2 and m[0].distance < ratio * m[1].distance]

    img_Keypoint_matches = cv2.drawMatches(img1, kps1,
                                           img2, kps2, matches, None)

    return kps1, kps2, matches, img_draw_L, img_draw_R, img_Keypoint_matches


def _init_detector_matcher(detector_name: str):
    try:
        detector, norm = DETECTOR_NORMS_DICT[detector_name]
    except KeyError:
        detector, norm = DETECTOR_NORMS_DICT["ORB"]

    flann_params = (
        dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        if norm == cv2.NORM_L2
        else dict(algorithm=FLANN_INDEX_LSH, table_number=6, key_size=12, multi_probe_level=1)
    )
    matcher = cv2.FlannBasedMatcher(flann_params, {})
    return detector, matcher
