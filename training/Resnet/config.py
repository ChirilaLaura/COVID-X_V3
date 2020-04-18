import os
ORIG_INPUT_DATASET = "dataset/images"

BASE_PATH = "dataset"

TRAIN_PATH = os.path.sep.join([BASE_PATH, "training"])
VAL_PATH = os.path.sep.join([BASE_PATH, "validation"])
TEST_PATH = os.path.sep.join([BASE_PATH, "testing"])

TRAIN_SPLIT = 0.8

VAL_SPLIT = 0.1
