# Before you start

## capability

+ 手动安装 cuda 11.8
+ python 3.12 
+ cuda nvidia capability:  https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html#
  `Table 3 CUDA Toolkit and Corresponding Driver Versions`
+ cuda pytorch capability: https://elenacliu-pytorch-cuda-driver.streamlit.app/
+ download pytorch: https://download.pytorch.org/whl/torch/
+ pytorch torchvision capability: https://pytorch.org/get-started/previous-versions/

## requirements (Machine Learning)

### windows
+ pytorch: https://download.pytorch.org/whl/cu118/torch-2.3.1%2Bcu118-cp312-cp312-win_amd64.whl#sha256=f44c7b64d990a6b1a382d1cd63c359806153974e7db8d16f6780645a8a9c9fe0
```shell
 python --version
 pip install init\torch-2.3.1+cu118-cp312-cp312-win_amd64.whl

 pip uninstall numpy
 pip install numpy==1.26.4 # 模型使用的老版本 numpy
 
 pip install -r requirements.txt # pip install -e .
```

## requirements (Deep Learning)

### windows
+ pytorch: https://download.pytorch.org/whl/cu118/torch-2.3.1%2Bcu118-cp312-cp312-win_amd64.whl#sha256=f44c7b64d990a6b1a382d1cd63c359806153974e7db8d16f6780645a8a9c9fe0
```shell
 python --version
 pip install init\torch-2.3.1+cu118-cp312-cp312-win_amd64.whl
 pip uninstall torchvision torchaudio
 pip install torchvision==0.18.1+cu118 --index-url https://download.pytorch.org/whl/cu118
 
 pip uninstall numpy
 pip install numpy==1.26.4 # 模型使用的老版本 numpy
 
 pip install -r requirements.txt # pip install -e .
```