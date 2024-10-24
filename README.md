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

> https://download.pytorch.org/whl/cu118

### windows
```shell
 python --version
 pip install D:\BaiduNetdiskDownload\torch-2.3.1+cu118-cp312-cp312-win_amd64.whl # 改为你自己的路径
 pip install -r requirements.txt # pip install -e .
```
### linux

https://download.pytorch.org/whl/cu118/torch-2.3.1%2Bcu118-cp312-cp312-linux_x86_64.whl#sha256=6c03ff41879674cbd661b598cec80fb5e6f7faa225624732a2a197b5471dbd38


## requirements (Deep Learning)

### windows
+ pytorch: https://download.pytorch.org/whl/cu118/torch-2.3.1%2Bcu118-cp312-cp312-win_amd64.whl#sha256=f44c7b64d990a6b1a382d1cd63c359806153974e7db8d16f6780645a8a9c9fe0
```shell
 python --version
 pip install D:\BaiduNetdiskDownload\torch-2.3.1+cu118-cp312-cp312-win_amd64.whl  # 改为你自己的路径
 pip uninstall torchvision torchaudio
 pip install torchvision==0.18.1+cu118 --index-url https://download.pytorch.org/whl/cu118
 pip install -r requirements.txt # pip install -e .
```



