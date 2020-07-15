这是一个基于Tornato框架的web网页，该网页是和之前的一个比赛相关的，上传一张图片，网页自动识别出该图片的类别，识别数据是西安的名胜古迹和美食，包含了54类，可以上传本地的图片，识别该图片属于啥。

![](E:\project\Dog-Breed-Identification-Gluon-master\image\fig.png)

### 安装运行步骤

1.下载解压

```pytho
git clone https://github.com/jackcywang/Web-Application-of-DeepLearning-.git
```

2.下载权重 到Web-Application-of-DeepLearning-目录

权重地址[百度云盘](https://pan.baidu.com/s/1HHe8hysDr_UVX6I4o62EfQ)，密钥0z6q

3.执行

```python
cd Web-Application-of-DeepLearning-
python app.py
```

4. 在浏览器中输入`http://127.0.0.1:8000`先选择一张图片，然后点击提交，就会出现上图的预测结果

![](E:\project\Dog-Breed-Identification-Gluon-master\image\fig2.png)