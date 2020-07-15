# -*- coding: utf-8 -*-

import torch
import torch.nn as nn
from torchvision.models import densenet121,resnet18,resnet34,densenet201,densenet169
import torch.nn.functional as F
import torch._utils
from torchvision import transforms
import torchvision.transforms as T
from PIL import Image
from class_id import label_id_names
class Dense201(nn.Module):
    def __init__(self, n_classes = 54):
        super(Dense201, self).__init__()
        planes = 1920
        self.features = densenet201(pretrained=False).features
        self.classifier = nn.Linear(planes,n_classes)
        nn.init.constant_(self.classifier.bias, 0)
        # nn.init.normal_(self.classifier.weight, std=0.001)
        self.bottleneck_g = nn.BatchNorm1d(planes)
        self.bottleneck_g.bias.requires_grad_(False)  # no shift

    def forward(self, x):
        x = self.features(x)
        out = F.relu(x, inplace=True)
        out = F.avg_pool2d(out, kernel_size=7, stride=1).view(x.size(0), -1)
        out = F.dropout(out,p=0.2)
        out = self.bottleneck_g(out)
        out = self.classifier(out)
        return out


trans=T.Compose([
            transforms.Scale(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            T.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
        ])

if __name__ == "__main__":
    model = Dense201()
    model.load_state_dict(torch.load('model_bestbestacc.pth'))
    model.eval()
    img = Image.open('static/image/img_4793.jpg')
    img = trans(img)
    img = img.unsqueeze(0)
    out = model(img)
    outputs = F.softmax(out, dim=1)
    with torch.no_grad():
        pred_score = model(img)
        pred_score = F.softmax(pred_score.data,dim=1)
        if pred_score is not None:
                pred_label = torch.argsort(pred_score[0], descending=True)[:1][0].item()
                result = {'result': label_id_names[str(pred_label)]}
        else:
            result = {'result': 'predict score is None'}

    classname = result['result']
    print(classname)
