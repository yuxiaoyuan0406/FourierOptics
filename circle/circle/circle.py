import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

def circle(X, Y, radius):
    '''
    输入array类
    要求是相等正方形
    返回值是一个形状一样的正方形array
    '''

    Z = np.zeros_like(X)    # 创建相似的array

    R = np.sqrt(np.square(X) + np.square(Y))

    i, j = 0, 0             # 定义循环标记
    for z in np.nditer(Z, op_flags=['readwrite']):      # 定义迭代器对象, 操作标记为'可读可写'
        if j == len(X[0]):      # 判断循环标记状态, 防止超出范围
            i = i + 1           # 到行结尾时要进行 行号 加一操作
            j = 0               # 并且将列号归零

        if R[i][j] <= radius:
            z[...] = 1          # 这里将到原点距离小于radius的对应的z修改为1
        else:
            z = 0               # 其他都是0
        j = j + 1           # 每次循环后列号加一
    return Z                # 循环结束返回array z

def draw_fft(Z):
    '''
    输入数据
    绘制傅里叶变换图
    '''
    Z_fft2 = np.fft.fft2(Z)     # 傅里叶变换
    Z_fft2_sh = abs(np.fft.fftshift(Z_fft2))    # 位移

    plt.subplot(121)            # 子图, 第一行
    plt.imshow(Z)               # 绘制原图
    plt.title('Original')

    plt.subplot(122)
    plt.imshow(Z_fft2_sh)       # 绘制傅里叶频谱
    plt.title('fft2-shift')

    plt.show()                  # 显示图片

    return Z_fft2, Z_fft2_sh

def plot_3D(X, Y, Z):
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)
 
    # Customize the z axis.
    ax.set_zlim(-1.01, 1.01)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
 
    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()

def main():
    X = np.arange(-5, 5, 0.01)  # 生成数据
    Y = np.arange(-5, 5, 0.01)

    X,Y = np.meshgrid(X, Y)     # 编织

    Z = circle(X, Y, 0.08)       # 生成圆孔

    Z_fft2, Z_fft2_sh = draw_fft(Z)

    val = abs(Z_fft2_sh[0][0])      # 归一化
    for x in np.nditer(Z_fft2_sh):
        if abs(x) > val:
            val = abs(x)
    for z in np.nditer(Z_fft2_sh, op_flags=['readwrite']):
        z[...] = z / val

    plot_3D(X, Y, Z_fft2_sh)    # 画图

if __name__ == '__main__':
    main()

