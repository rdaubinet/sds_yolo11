import torch
import torch.nn as nn
from torch.nn import functional as F


class CARAFE(nn.Module):
    """
    CARAFE: Content-Aware ReAssembly of FEatures
    ONNX-compatible version using F.unfold
    """
    def __init__(self, c1, c2, kernel_size=3, up_factor=2):
        super(CARAFE, self).__init__()
        self.kernel_size = kernel_size
        self.up_factor = up_factor
        self.down = nn.Conv2d(c1, c1 // 4, 1)
        self.encoder = nn.Conv2d(c1 // 4, self.up_factor ** 2 * self.kernel_size ** 2,
                                 self.kernel_size, 1, self.kernel_size // 2)
        self.out = nn.Conv2d(c1, c2, 1)

    def forward(self, x):
        N, C, H, W = x.size()
        
        # Kernel prediction module
        kernel_tensor = self.down(x)  # (N, Cm, H, W)
        kernel_tensor = self.encoder(kernel_tensor)  # (N, S^2 * Kup^2, H, W)
        kernel_tensor = F.pixel_shuffle(kernel_tensor, self.up_factor)  # (N, Kup^2, S*H, S*W)
        kernel_tensor = F.softmax(kernel_tensor, dim=1)  # (N, Kup^2, S*H, S*W)
        
        # Reshape kernel tensor to match content patches
        # Use explicit view/reshape operations instead of unfold
        kernel_tensor = kernel_tensor.view(N, self.kernel_size ** 2, H, self.up_factor, W, self.up_factor)
        kernel_tensor = kernel_tensor.permute(0, 1, 2, 4, 3, 5).contiguous()  # (N, Kup^2, H, W, S, S)
        kernel_tensor = kernel_tensor.view(N, self.kernel_size ** 2, H, W, self.up_factor ** 2)
        kernel_tensor = kernel_tensor.permute(0, 2, 3, 1, 4).contiguous()  # (N, H, W, Kup^2, S^2)

        # Content-aware reassembly module using F.unfold (better ONNX support)
        # Use ReflectionPad2d or ZeroPad2d instead of F.pad for better compatibility
        pad = nn.ZeroPad2d(self.kernel_size // 2)
        x_padded = pad(x)
        
        # Use F.unfold which has ONNX support
        x_unfolded = F.unfold(x_padded, kernel_size=self.kernel_size, stride=1)
        # x_unfolded shape: (N, C*Kup^2, H*W)
        
        x_unfolded = x_unfolded.view(N, C, self.kernel_size ** 2, H, W)
        x_unfolded = x_unfolded.permute(0, 3, 4, 1, 2).contiguous()  # (N, H, W, C, Kup^2)

        # Content-aware reassembly
        out_tensor = torch.matmul(x_unfolded, kernel_tensor)  # (N, H, W, C, S^2)
        out_tensor = out_tensor.view(N, H, W, -1)
        out_tensor = out_tensor.permute(0, 3, 1, 2).contiguous()  # (N, C*S^2, H, W)
        out_tensor = F.pixel_shuffle(out_tensor, self.up_factor)  # (N, C, H*S, W*S)
        out_tensor = self.out(out_tensor)
        
        return out_tensor