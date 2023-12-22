import numpy as np
import pandas as pd

# 创建一个示例的 NumPy 数组
data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# 将 NumPy 数组转换为 Pandas DataFrame
df = pd.DataFrame(data)

# 指定要导出的 Excel 文件名
excel_file = "output.xlsx"

# 使用 Pandas 将 DataFrame 导出到 Excel 文件
df.to_excel(excel_file, index=False)

print(f"NumPy数组已导出到 {excel_file}")
