# ！有条件就创建虚拟环境
调试环境**python 3.10.14 **
cuda 12.1
pip安装所需环境 

```
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```



# ！如何运行
在steg目录下，打开bash/cmd/powershell

```
conda activate <Your virtual env>
streamlit run app.py
```

# ！警告
开梯子全局代理
项目运行较慢 显卡30系以上为佳
其中上传图片在/uploded_images
生成图片在/outputs