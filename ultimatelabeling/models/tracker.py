import os
import torch
from .polygon import Polygon, Bbox
import json
import cv2
from ultimatelabeling.siamMask.models.custom import Custom
from ultimatelabeling.siamMask.utils.load_helper import load_pretrain
from ultimatelabeling.siamMask.test import siamese_init, siamese_track
from ultimatelabeling.config import RESOURCES_DIR, PRETRAINED_SIAM


class Tracker:
    def __init__(self):
        self.use_cuda = torch.cuda.is_available()
        self.device = torch.device('cuda' if self.use_cuda else 'cpu')
        print('using device {}'.format(self.device))
        torch.backends.cudnn.benchmark = True

    def init(self, img, bbox):
        """
        Arguments:
            img (OpenCV image): obtained from cv2.imread(img_file)
            bbox (BBox)
        """
        raise NotImplementedError

    def track(self, img):
        """
        Output:
            bbox (BBox), polygon (Polygon)
        """
        raise NotImplementedError

    def terminate(self):
        pass


class SiamMaskTracker(Tracker):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cfg = json.load(open(os.path.join(RESOURCES_DIR, "config_vot.json")))
        self.tracker = Custom(anchors=self.cfg['anchors'])
        self.tracker = load_pretrain(self.tracker, PRETRAINED_SIAM , use_cuda=self.use_cuda)
        self.tracker.eval().to(self.device)

        self.state = None

    def init(self, img_file, bbox):
        img = cv2.imread(img_file)
        self.state = siamese_init(img, bbox.center, bbox.size, self.tracker, self.cfg['hp'], use_cuda=self.use_cuda)

    def track(self, img_file):
        img = cv2.imread(img_file)
        self.state = siamese_track(self.state, img.copy(), mask_enable=True, refine_enable=True, use_cuda=self.use_cuda)
        bbox = Bbox.from_center_size(self.state['target_pos'], self.state['target_sz'])
        polygon = Polygon(self.state['ploygon'].flatten())

        return bbox, polygon