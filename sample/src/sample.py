# 2点間の距離を計算するサンプル
import math


def distance(p, q):
    """2点 p, q の距離を返す"""
    return math.hypot(p[0] - q[0], p[1] - q[1])


if __name__ == "__main__":
    print(distance((0, 0), (3, 4)))  # 5.0 を表示する
