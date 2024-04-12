import torch
cuda_available=torch.cuda.is_available()
if cuda_available:
    num_cuda_available=torch.cuda.device_count
    print(num_cuda_available)

else:
    print("nonono")