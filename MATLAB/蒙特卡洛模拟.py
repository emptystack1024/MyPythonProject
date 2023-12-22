import numpy as np
import matplotlib.pyplot as plt

# 模拟参数
num_photons = 30000  # 光子数量
cone_angle_degrees = 10.0  # 太阳光锥的半角（以度为单位）
sim_space_radius = 100.0  # 模拟空间的半径

# 初始化计数器
energy_count = 0

# 存储光子位置的列表
x_positions = []
y_positions = []

# 太阳光锥的半角转换为弧度
cone_angle_radians = np.radians(cone_angle_degrees)

# 执行蒙特卡洛模拟
for _ in range(num_photons):
    # 随机生成光子的方向向量（假设在单位圆上均匀分布）
    theta = np.radians(np.random.rand() * 360)  # 随机生成一个角度
    r = np.random.rand() * sim_space_radius

    # 计算光子在模拟空间内的位置
    x_pos = r * np.cos(theta)
    y_pos = r * np.sin(theta)

    # 判断光子是否在太阳光锥内
    if r <= sim_space_radius * np.sin(cone_angle_radians):
        # 存储位置信息
        x_positions.append(x_pos)
        y_positions.append(y_pos)

        # 假设模拟空间中的某种条件，例如太阳光锥的位置和方向
        # 在实际模拟中，这将取决于太阳位置和时间等因素

        # 计算能量流密度，这里简化为 1/r^2
        energy_density = 1 / (r ** 2)

        # 更新计数器
        energy_count += energy_density

# 计算平均能流密度
average_energy_density = energy_count / num_photons

print(f"估计的太阳光锥能流密度：{average_energy_density}")

# 创建二维散点图
plt.figure()
plt.scatter(x_positions, y_positions, c='b', marker='.', label='photons location')

plt.xlabel('X')
plt.ylabel('Y')
plt.title(f'Solar cone energy flow density simulation')

plt.legend()
plt.grid(True)
plt.axis('equal')  # 保持坐标轴比例相等
plt.show()
