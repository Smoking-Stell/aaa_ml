import torch
import torch.nn as nn
import numpy as np
import os
import random


class AlexNet(nn.Module):
    def __init__(self, in_channels, num_classes):
        super().__init__()

        # Инициализируйте необходимое количество conv слоёв
        self.conv1 = nn.Conv2d(in_channels=in_channels, out_channels=96,
                               kernel_size=11, padding=2, stride=4)
        self.conv2 = nn.Conv2d(in_channels=96, out_channels=256,
                               kernel_size=5, padding=2, stride=1)
        self.conv3 = nn.Conv2d(in_channels=256, out_channels=384,
                               kernel_size=3, padding=1, stride=1)
        self.conv4 = nn.Conv2d(in_channels=384, out_channels=384,
                               kernel_size=3, padding=1, stride=1)
        self.conv5 = nn.Conv2d(in_channels=384, out_channels=256,
                               kernel_size=3, padding=1, stride=1)

        # Инициализируйте maxpool и relu слои
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2)
        self.relu = nn.ReLU()

        # Инициализируйте необходимое количество linear слоёв
        self.linear1 = nn.Linear(in_features=6*6*256, out_features=100, bias=True)
        self.linear2 = nn.Linear(in_features=100, out_features=100, bias=True)
        self.linear3 = nn.Linear(in_features=100, out_features=num_classes, )

    def forward(self, x):
        x = self.conv1(x)
        x = self.relu(x)
        x = self.maxpool(x)
        x = self.conv2(x)
        x = self.relu(x)
        x = self.maxpool(x)
        x = self.conv3(x)
        x = self.relu(x)
        x = self.conv4(x)
        x = self.relu(x)
        x = self.conv5(x)
        x = self.relu(x)
        x = self.maxpool(x)
        out = x.flatten(1)
        out = self.linear1(out)
        out = self.relu(out)
        out = self.linear2(out)
        out = self.relu(out)
        out = self.linear3(out)
        return out


def seed_everything(seed=42):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

seed_everything()
input_image = torch.randn(1, 3, 224, 224)

alexnet = AlexNet(in_channels=3, num_classes=10)
result = alexnet(input_image)

print(torch.allclose(result, torch.tensor([[ 0.0367,  0.0385, -0.0191, -0.0138,  0.0834, -0.0005, -0.0089, -0.0301,
         -0.0403,  0.0383]]), atol=1e-4
              ))


