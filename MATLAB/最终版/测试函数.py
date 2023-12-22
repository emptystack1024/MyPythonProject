import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt


# 计算余弦损失
# def calculate_cosine_loss(theta):
#     theta_rad = math.radians(theta)
#     AM = 1 / math.cos(theta_rad)
#     I_D_0 = 1.366 * 0.7
#     I_D_thera = 1.366 * 0.7 ** (AM ** 0.678)
#     cosine_loss = 1 - (I_D_0 - I_D_thera) / I_D_0
#
#     return cosine_loss
def cosine_loss(month, day):
    D = day_exchange(month, day)

    Sum = 0
    Time = [9, 10.5, 12, 13.5, 15]

    for i in Time:
        # 天顶角
        hudu_td = (np.pi / 2) - As(D, i)
        # 大气质量
        AM = 1 / np.cos(hudu_td)
        # 直接辐射
        Id = 1.353 * 0.7 ** (AM ** 0.678)

        sunshi = (0.7 * 1.353 - Id) / (0.7 * 1.366)
        Sum += 1 - sunshi

    return Sum / 5


# 求太阳赤纬角
# def solar_declination(D):
#     return math.asin(math.sin(2 * math.pi * D / 365) * math.sin(math.radians(23.45)))
def Th(D):
    D -= 80
    if D < 0:
        D += 365

    sin_th = np.sin(2 * np.pi * D / 365) * np.sin(2 * np.pi * 23.45 / 360)  # 太阳赤纬角th的sin值
    hudu_th = math.asin(sin_th)  # 太阳赤纬角th的弧度值

    return hudu_th


# 求太阳时角
def W(Tm):
    return np.pi / 12 * (Tm - 12)


# 求太阳高度角
# def solar_altitude_angle(phi, delta, omega):
#     return math.asin(math.cos(delta) * math.cos(phi) * math.cos(omega) + math.sin(delta) * math.sin(phi))
def As(D, Tm):
    temp_hudu_th = Th(D)
    temp_sin_th = np.sin(temp_hudu_th)

    sin_as = np.cos(temp_hudu_th) * np.cos(39.4 * np.pi / 180) * np.cos(W(Tm)) + temp_sin_th * np.sin(
        39.4 * np.pi / 180)  # 太阳高度角的sin值
    hudu_as = math.asin(sin_as)  # 太阳高度角的弧度值

    return hudu_as


# 求太阳方位角
# def solar_azimuth_angle(a_s, phi, delta):
#     value = (math.sin(delta) - math.sin(a_s) * math.sin(phi)) / (math.cos(a_s) * math.cos(phi))
#     if value > 1:
#         return 1
#     elif value < -1:
#         return -1
#
#     return math.acos(value)
def Ys(D, tm):
    cos_ys = (np.sin(Th(D)) - (np.sin(As(D, tm)) * np.sin(39.4 * np.pi / 180))) / (
            np.cos(As(D, tm)) * np.cos(39.4 * np.pi / 180))  # 太阳方位角的cos值
    if cos_ys > 1:
        cos_ys = 1
    elif cos_ys < -1:
        cos_ys = -1
    hudu_ys = np.arccos(cos_ys);  # 太阳方位角的弧度值

    return (hudu_ys)


# 距离春分的天数
def day_exchange(month, day):
    month = int(month)
    day = int(day)

    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return sum(days_in_month[:month - 1]) + day - 21


# 计算太阳高度角和太阳方位角
def solar_angles(month, day, times, latitude):  # latitude 纬度
    D = day_exchange(month, day)

    delta = Th(D)

    results = []

    for tm in times:
        omega = W(tm)
        a_s = As(D, tm)
        g_s = Ys(D, tm)

        results.append((a_s, g_s))

    return results


# 计算太阳入射向量
def SunAngel(hudu_a_s, hudu_ys):
    # hudu_a_s为太阳高度角的弧度值
    # hudu_ys为太阳方位角的弧度值
    # 返回太阳入射向量
    x = -np.cos(hudu_a_s) * np.sin(hudu_ys)
    y = -np.cos(hudu_a_s) * np.cos(hudu_ys)
    z = -np.sin(hudu_a_s)

    return np.array([x, y, z])

# 计算直接法辐照度
def QDNI(a_s, H):
    G_0 = 1.366
    a = 0.4237 - 0.00821 * (6 - H) ** 2
    b = 0.5055 + 0.00595 * (6.5 - H) ** 2
    c = 0.2711 + 0.01858 * (2.5 - H) ** 2

    if math.sin(a_s) == 0:
        return 0
    else:
        return G_0 * (a + b * math.exp(-c / math.sin(a_s)))


# 计算大气透过率
def atmospheric(d_HR):
    return 0.99321 - 0.000117 * d_HR - 0.0000014 * d_HR ** 2


# 计算倾斜角的函数
def QXJ(D, tm, x, y):
    # a_s为太阳高度角
    hudu_a_s = As(D, tm)

    # ys为太阳方位角
    jiaodu_ys = Ys(D, tm)
    hudu_ys = jiaodu_ys * np.pi / 180

    # 计算太阳入射向量
    Sun = SunAngel(hudu_a_s, hudu_ys)

    # 计算集日镜出射向量
    Out = np.array([x, y, 80])

    # 归一化
    Sun = Sun / np.linalg.norm(Sun)
    Out = Out / np.linalg.norm(Out)

    # 法向量
    Normal = Sun + Out
    Normal = Normal / np.linalg.norm(Normal)

    # 计算倾斜角
    hudu_qxj = np.arccos(np.dot(Normal, [0, 0, 1]))

    return hudu_qxj


# 计算结果
def calc_results(mirror_area, mirror_positions_df, output_excel=False):
    # 计算每个集日镜和集热他中心的距离
    mirror_positions_df['d_HR'] = (mirror_positions_df[('x坐标 (m)')] ** 2 + mirror_positions_df[
        ('y坐标 (m)')] ** 2) ** 0.5

    # 计算纬度和时间
    latitude = math.radians(39.4)
    times = [9, 10.5, 12, 13.5, 15]
    sun_angles = []

    for month in range(1, 13):
        angles = solar_angles(month, 21, times, latitude)
        # angles ———— 存储太阳高度角和太阳方位角的数组
        for time, (a_s, g_s) in zip(times, angles):
            sun_angles.append([
                month,
                time,
                a_s,
                g_s
            ])

    sun_angles_df = pd.DataFrame(sun_angles, columns=['月份', '日期', '太阳高度角', '太阳方位角'])

    H = 3  # 可能是3
    sun_angles_df['DNI'] = sun_angles_df['太阳高度角'].apply(lambda x: QDNI(x, H))

    # 计算大气透过率
    mirror_positions_df['n_at'] = mirror_positions_df['d_HR'].apply(atmospheric)
    eta_ref = 0.92

    # !!!!sun_angles_df['cosine_loss'] = sun_angles_df['太阳高度角'].apply(lambda x: cosine_loss(x))
    temp_month = sun_angles_df['月份']
    temp_time = sun_angles_df['日期']
    sun_angles_df['cosine_loss'] = sun_angles_df.apply(lambda com: cosine_loss(com['月份'], com['日期']), axis=1)

    # sun_angles_df['n_cos'] = 1 - sun_angles_df['cosine_loss']
    sun_angles_df['n_cos'] = sun_angles_df['cosine_loss']

    sun_angles_df['shadow_loss'] = sun_angles_df.apply(lambda com: 0.1 if 170 <= com['太阳方位角'] <= 190 else 0,
                                                       axis=1)
    sun_angles_df['n_sb'] = sun_angles_df['shadow_loss']  # n_sb 取值 1 或者 0.9

    # 如何计算 n_trunc？？？
    sun_angles_df['total_reflected_energy'] = sun_angles_df['DNI'] * mirror_area * sun_angles_df['n_sb']
    sun_angles_df['shadow_loss_energy'] = sun_angles_df['DNI'] * mirror_area * sun_angles_df['shadow_loss']
    sun_angles_df['collector_received_energy'] = 0.92 * sun_angles_df['total_reflected_energy']
    sun_angles_df['n_trunc'] = sun_angles_df['collector_received_energy'] / sun_angles_df['total_reflected_energy'] - \
                               sun_angles_df['shadow_loss_energy']



    norgod_df = pd.merge(mirror_positions_df.assign(key=1), sun_angles_df.assign(key=1), on='key').drop('key', axis=1)
    norgod_df['n'] = norgod_df['n_at'] * norgod_df['n_cos'] * norgod_df['n_sb'] * norgod_df['n_trunc'] * eta_ref

    # '平均光学效率'
    everage_optional_efficiency_per_month = norgod_df.groupby(['月份'])['n'].mean()
    # '平均余弦效率'
    everage_cosine_efficiency_per_month = norgod_df.groupby(['月份'])['n_cos'].mean()
    # '平均阴影效率'
    everage_shadow_efficiency_per_month = norgod_df.groupby(['月份'])['n_sb'].mean()
    # '平均截断效率'
    everage_truncation_efficiency_per_month = norgod_df.groupby(['月份'])['n_trunc'].mean()

    # 输出热功率
    norgod_df['output_thermal_power'] = norgod_df['n'] * norgod_df['DNI']
    everage_ouput_thermal_power_per_month = norgod_df.groupby(['月份'])['output_thermal_power'].mean()

    result_df = pd.DataFrame({
        '月份': everage_optional_efficiency_per_month.index,
        '平均光学效率': everage_optional_efficiency_per_month.values,
        '平均余弦效率': everage_cosine_efficiency_per_month.values,
        '平均阴影效率': everage_shadow_efficiency_per_month.values,
        '平均截断效率': everage_truncation_efficiency_per_month.values,
        '平均输出热功率': everage_ouput_thermal_power_per_month.values
    })

    if output_excel:
        result_df.to_excel('result.xlsx')
    return result_df['平均输出热功率'].mean(), np.mean(
        mirror_positions_df.shape[0] * mirror_area * result_df['平均输出热功率'] / 1000)
    # print(f"单位镜面面积平均输出热功率：{result_df['平均输出热功率'].mean()} ")
    # print(f"总输出热功率：{} kW")


# 计算集日镜的位置
def calculate_mirror_positions_around_tower(number_of_mirrors, mirror_size):
    start_distance = 100

    spacing = mirror_size + 5

    positions = []
    current_distance = start_distance
    current_angle = 0
    delta_angle = 2 * np.pi / (current_distance / spacing)

    for _ in range(number_of_mirrors):
        x = current_distance * np.cos(current_angle)
        y = current_distance * np.sin(current_angle)
        positions.append([x, y])

        current_angle += delta_angle
        if current_angle >= 2 * np.pi:
            current_angle -= 2 * np.pi
            current_distance += spacing
            delta_angle = 2 * np.pi / (current_distance / spacing)

    return positions


number_of_mirrors_test = 1457
mirror_size_test = 8

# test: 测试输出平均功率最大
max_value = 0
max_number = 0
max_size = 0

results = []
for number_of_mirrors_test in range(500, 3000, 50):
    # print(number_of_mirrors_test)
    for mirror_size_test in range(2, 8):
        output_thermal_power_per_month, output_thermal_power = calc_results(
            mirror_size_test ** 2,
            pd.DataFrame(calculate_mirror_positions_around_tower(number_of_mirrors_test, mirror_size_test),
                         columns=['x坐标 (m)', 'y坐标 (m)'])
        )

        # if output_thermal_power >= 60:
        results.append((number_of_mirrors_test, mirror_size_test, output_thermal_power_per_month, output_thermal_power))

        if output_thermal_power_per_month > max_value:
            max_value = output_thermal_power
            max_number = number_of_mirrors_test
            max_size = mirror_size_test
pd.DataFrame(results, columns=['镜面数量', '镜面尺寸', '平均输出热功率', '总输出热功率']).to_excel('result2.xlsx')

print(max_value, max_number, max_size)
locs = pd.DataFrame(calculate_mirror_positions_around_tower(max_number, max_size), columns=['x坐标 (m)', 'y坐标 (m)'])
# locs = pd.DataFrame(calculate_mirror_positions_around_tower(1050, 7), columns=['x坐标 (m)', 'y坐标 (m)'])
# locs = pd.DataFrame(calculate_mirror_positions_around_tower(1457, 8), columns=['x坐标 (m)', 'y坐标 (m)'])
output_thermal_power_per_month, output_thermal_power = calc_results(
    mirror_size_test ** 2,
    locs
)

locs.to_excel('locs2.xlsx')

file = pd.ExcelFile("C:\\code\\pythonProject\\jupy_test\\MATLAB\\最终版\\locs2.xlsx")
df = file.parse('Sheet1')

# 提取 x 和 y 坐标
x_coords = df['x坐标 (m)']
y_coords = df['y坐标 (m)']

# 创建散点图
plt.scatter(x_coords, y_coords, label='Points', color='blue', marker='.')

# 添加标签和标题
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.title('Scatter Plot of Coordinates')

# 显示图例
plt.legend()

# 显示图形
plt.show()