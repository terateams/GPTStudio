import streamlit as st
import numpy as np
from sklearn.decomposition import PCA
import plotly.express as px

# 假设这是你的向量和对应的文本内容
# 在实际应用中，这些数据应该是通过 OpenAI 嵌入模型生成的
vectors = np.random.rand(100, 512)  # 100个512维向量
texts = [f"文本内容{i}" for i in range(100)]  # 对应的文本内容

# 应用PCA降维
pca = PCA(2)
vectors_2d = pca.fit_transform(vectors)

# 创建Plotly散点图
fig = px.scatter(x=vectors_2d[:, 0], y=vectors_2d[:, 1], hover_data=[texts])

# 在Streamlit中展示图表
st.plotly_chart(fig)

# 可以添加一个下拉菜单来选择特定的数据点并显示详细信息
selected_index = st.selectbox("选择数据点", options=range(100))
st.write(f"选中的文本内容: {texts[selected_index]}")
