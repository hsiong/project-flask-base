# Before you start

## capability

+ cuda nvidia capability:  https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html#
  `Table 3 CUDA Toolkit and Corresponding Driver Versions`
+ cuda pytorch capability: https://elenacliu-pytorch-cuda-driver.streamlit.app/ ; https://github.com/elenacliu/pytorch_cuda_driver_compatibilities?tab=readme-ov-file
+ pytorch torchvision capability: https://pytorch.org/get-started/previous-versions/

+ python 3.12
+ torch 2.3.1
+ download cuda: https://developer.nvidia.com/cuda-toolkit-archive
+ download pytorch: https://download.pytorch.org/whl/torch/ ; > https://download.pytorch.org/whl/cu118

## requirements

### windows

+ pytorch: https://download.pytorch.org/whl/cu118/torch-2.3.1%2Bcu118-cp312-cp312-win_amd64.whl#sha256=f44c7b64d990a6b1a382d1cd63c359806153974e7db8d16f6780645a8a9c9fe0
```shell
# 手动安装 cuda 11.8
 python --version
 pip install onnx_model\torch-2.3.1+cu118-cp312-cp312-win_amd64.whl
 pip uninstall torchvision torchaudio
 pip install torchvision==0.18.1+cu118 --index-url https://download.pytorch.org/whl/cu118
 
 pip uninstall numpy
 pip install numpy==1.26.4 # 模型使用的老版本 numpy
 
 pip install -r requirements.txt # pip install -e .
```

### linux
+ https://download.pytorch.org/whl/cu118/torch-2.3.1%2Bcu118-cp312-cp312-linux_x86_64.whl#sha256=6c03ff41879674cbd661b598cec80fb5e6f7faa225624732a2a197b5471dbd38

```shell
# 手动安装 cuda 11.8 : https://developer.nvidia.com/cuda-toolkit-archive


 python --version
 pip install onnx_model/torch-2.3.1+cu118-cp312-cp312-linux_x86_64.whl
 
 pip uninstall torchvision torchaudio
 pip install torchvision==0.18.1+cu118 --index-url https://download.pytorch.org/whl/cu118
 
 pip uninstall numpy
 pip install numpy==1.26.4 # 模型使用的老版本 numpy
 
 pip install -r requirements.txt # pip install -e .
```

### mac

```
python --version
pip uninstall torchvision torchaudio
pip install torch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1

pip uninstall numpy
pip install numpy==1.26.4 # 模型使用的老版本 numpy

pip install -r requirements-mac.txt # pip install -e .
```