import torch
import torch.nn as nn
from torch.nn import functional as F


class CARAFE(nn.Module):
    """
    CARAFE: Content-Aware ReAssembly of FEatures
    Simplified ONNX-compatible version using standard operations only
    
    This version sacrifices some of the original CARAFE's sophisticated content-aware
    reassembly for ONNX/TensorRT compatibility while maintaining learnable upsampling.
    """
    def __init__(self, c1, c2, kernel_size=3, up_factor=2):
        super(CARAFE, self).__init__()
        self.kernel_size = kernel_size
        self.up_factor = up_factor
        
        # Compress channels
        self.compress = nn.Conv2d(c1, c1 // 4, 1)
        
        # Learnable upsampling kernel prediction
        self.upsample_conv = nn.Conv2d(
            c1 // 4, 
            (c1 // 4) * (up_factor ** 2), 
            kernel_size, 
            1, 
            kernel_size // 2
        )
        
        # Content processing
        self.content_conv = nn.Conv2d(c1, c1 * (up_factor ** 2), 1)
        
        # Final output projection
        self.out = nn.Conv2d(c1, c2, 1)

    def forward(self, x):
        # Learnable upsampling branch (predicts how to upsample)
        up = self.compress(x)
        up = self.upsample_conv(up)
        up = F.pixel_shuffle(up, self.up_factor)
        
        # Content branch (carries the actual content)
        content = self.content_conv(x)
        content = F.pixel_shuffle(content, self.up_factor)
        
        # Content-aware modulation: use upsampling prediction to modulate content
        out = content * torch.sigmoid(up)
        out = self.out(out)
        
        return out
