# Before you start

## capability

+ cuda nvidia capability:  https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html#
  `Table 3 CUDA Toolkit and Corresponding Driver Versions`
+ cuda pytorch capability: https://elenacliu-pytorch-cuda-driver.streamlit.app/ ; https://github.com/elenacliu/pytorch_cuda_driver_compatibilities?tab=readme-ov-file
+ pytorch torchvision capability: https://pytorch.org/get-started/previous-versions/
+ python numpy capability: https://github.com/numpy/numpy/releases

  > v1 newest version: 1.26.4: The Python versions supported by this release are 3.9-3.12




download: 

+ download cuda: https://developer.nvidia.com/cuda-toolkit-archive

+ download pytorch: https://download.pytorch.org/whl/torch/ ; > https://download.pytorch.org/whl/cu118

+ python 3.12

```shell
sudo apt update && sudo apt upgrade -y
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-cache policy python3.12

sudo apt install python3.12
ls /usr/bin/python*
```
+ torch 2.3.1

## requirements

### windows

```shell
 # 手动安装 pytorch: https://download.pytorch.org/whl/torch/
 # https://download.pytorch.org/whl/cu121/torch-2.3.1%2Bcu121-cp312-cp312-linux_x86_64.whl#sha256=b3c586f4ab25e83efffccfb97079e91325329bc228166555c4bb93957753d4ea
 python --version
 pip install pip install torch==2.3.1+cu118  -f https://download.pytorch.org/whl/torch_stable.html
 pip uninstall torchvision torchaudio
 pip install torchvision==0.18.1+cu118 --index-url https://download.pytorch.org/whl/cu118
 
 pip uninstall numpy
 pip install numpy==1.26.4 # 模型使用的老版本 numpy
 
 pip install -r requirements.txt # pip install -e .
```

### linux
+ 安装 python
```shell
sudo apt update && sudo apt upgrade -y
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-cache policy python3.12

sudo apt install python3.12
ls /usr/bin/python*
```
+ 安装 driver

```shell
 sudo add-apt-repository ppa:graphics-drivers/ppa
 sudo apt-get update
 sudo apt-get install nvidia-driver-520
```

+ 安装 cuda

```shell
 nvidia-smi
 # 手动安装 cuda : https://developer.nvidia.com/cuda-toolkit-archive
 # 根据文档操作: wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin......
 # 注意 ⭐️ 最后一步换为 sudo apt-get -y install cuda-x-xx
 sudo apt-get -y install cuda-12.2
 ls /usr/local/cuda-*
 echo 'export PATH=/usr/local/cuda-12.2/bin${PATH:+:${PATH}}' >> ~/.bashrc
 echo 'export LD_LIBRARY_PATH=/usr/local/cuda-12.2/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}' >> ~/.bashrc
 source ~/.bashrc
```

+ 安装依赖

```shell

 # 手动安装 pytorch: https://download.pytorch.org/whl/torch/
 # https://download.pytorch.org/whl/cu121/torch-2.3.1%2Bcu121-cp312-cp312-linux_x86_64.whl#sha256=b3c586f4ab25e83efffccfb97079e91325329bc228166555c4bb93957753d4ea
 python --version
 pip install pip install torch==2.3.1+cu121  -f https://download.pytorch.org/whl/torch_stable.html
 
 pip uninstall torchvision torchaudio
 pip install torchvision==0.18.1+cu121 --index-url https://download.pytorch.org/whl/cu121
 
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

# CUDA

## 如何看本机cuda

### **通过命令行检查 CUDA 版本**

1. **打开命令提示符（CMD）**：

   - 使用快捷键 `Win + R` 打开“运行”窗口，输入 `cmd`，然后按回车。

2. **运行命令检查 CUDA 版本**：

   - 输入以下命令检查 `nvcc`（CUDA 编译器驱动）的版本：

   ```
   nvcc --version
   ```

   这将输出 CUDA 编译器驱动的版本号。例如：

   ```
   nvcc: NVIDIA (R) Cuda compiler driver
   Copyright (c) 2005-2021 NVIDIA Corporation
   Built on Thu_Jan_28_19:32:12_Pacific_Standard_Time_2021
   Cuda compilation tools, release 11.2, V11.2.152
   ```

   上面的输出显示，CUDA 版本为 `11.2`。

3. **检查 CUDA 库文件版本**：

   - 输入以下命令，检查驱动支持的 CUDA 版本：

   ```
   nvidia-smi
   ```

   这会输出类似于以下的内容：

   ```
   +-----------------------------------------------------------------------------+
   | NVIDIA-SMI 455.45.01    Driver Version: 455.45.01    CUDA Version: 11.1     |
   +-----------------------------------------------------------------------------+
   ```

   输出结果中的 `CUDA Version` 即为安装的 CUDA 版本号。

### **通过检查已安装的 CUDA 工具包**

#### Windows

1. **打开文件资源管理器**。

2. 导航到 CUDA 安装目录

   （默认路径）：

   - 通常安装在 `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\` 下。

3. 查看文件夹名称：

   - 在该目录下，你会看到以版本号命名的文件夹（如 `v10.1`、`v11.0` 等），这就是已安装的 CUDA 版本。

#### Linux

你可以通过查看 CUDA 工具包的安装目录来找到安装的版本号。

1. 通常，CUDA 安装在 `/usr/local/cuda` 目录下。如果该目录存在，你可以查看版本文件：

   ```
   cat /usr/local/cuda/version.txt
   ```

   示例输出：

   ```
   CUDA Version 11.2.67
   ```

   这会显示已安装的 CUDA 工具包的版本。

2. 你也可以列出 `/usr/local` 目录下的文件夹名，其中会显示以 `cuda-<version>` 命名的文件夹：

   ```
   ls /usr/local/ | grep cuda
   ```

   示例输出：

   ```
   cuda-10.1
   cuda-11.2
   ```

   这表明系统中安装了多个 CUDA 版本，你可以根据需求选择其中一个版本。