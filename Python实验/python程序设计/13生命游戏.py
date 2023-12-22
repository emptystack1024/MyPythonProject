def game_of_life(m, n, board):
    # 这两个列表表示一个细胞周围的八个方向
    dx = [-1, -1, -1, 0, 0, 1, 1, 1]
    dy = [-1, 0, 1, -1, 1, -1, 0, 1]
    # 定义一个和输入状态矩阵一样大小的零矩阵存储更新后的状态
    tmp = [[0] * n for _ in range(m)]
    # 遍历所有细胞，进行状态更新
    for i in range(m):
        for j in range(n):
            cnt = 0
            # 统计周围活着的细胞数量
            for k in range(8):
                ni, nj = i + dx[k], j + dy[k] # ni,nj表示当前细胞的周围八个格子的坐标
                if 0 <= ni < m and 0 <= nj < n: # 保证还在矩阵的边界内
                    cnt += board[ni][nj] # board[ni][nj]为1说明周围有一个活着的细胞
            if board[i][j]: # 如果当前细胞是活着的
                if cnt < 2 or cnt > 3: # 如果周围活细胞数量不符合条件1,2，则该细胞在下一刻状态更新后死亡
                    tmp[i][j] = 0
                else: # 如果周围活细胞数量符合条件3，则该细胞在下一刻状态更新后仍然存活
                    tmp[i][j] = 1
            else: # 如果当前细胞是死亡的
                if cnt == 3: # 如果周围恰好有三个活细胞，则该细胞在下一刻状态更新后复活
                    tmp[i][j] = 1
                else: # 否则该细胞在下一刻状态更新后仍然死亡
                    tmp[i][j] = 0
    return tmp # 返回更新后的状态

# t 组测试数据
t = int(input())
for _ in range(t):
    m, n = map(int, input().split())
    board = []
    # 读入状态矩阵
    for i in range(m):
        row = list(map(int, list(input().strip())))
        board.append(row)
    # 进行一次状态更新
    res = game_of_life(m, n, board)
    # 输出更新后的状态矩阵
    for row in res:
        print(''.join(map(str, row)))