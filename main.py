# 中国象棋人机对战游戏（带颜色显示）
from colorama import Fore, Back, Style, init

# 初始化 colorama
init(autoreset=True)

g_map = {    
    "C":"俥",
    "c":"车",
    "M":"傌",
    "m":"马",
    "p":"砲",
    "P":"炮",
    "z":"卒",
    "B":"兵",
    "x":"象",
    "X":"相",
    "s":"士",
    "S":"仕",
    "k":"将",
    "K":"帅",
    " ": " "
}
def getName(charname):
    global g_map
    return g_map[charname]
# 棋盘初始化
def init_board():
    # 棋盘表示：红方大写，黑方小写
    # 将/帅: K/k, 士: S/s, 象: X/x, 马: M/m, 车: C/c, 炮: P/p, 兵/卒: B/z
    board = [
        ['c', 'm', 'x', 's', 'k', 's', 'x', 'm', 'c'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', 'p', ' ', ' ', ' ', ' ', ' ', 'p', ' '],
        ['z', ' ', 'z', ' ', 'z', ' ', 'z', ' ', 'z'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'],
        [' ', 'P', ' ', ' ', ' ', ' ', ' ', 'P', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['C', 'M', 'X', 'S', 'K', 'S', 'X', 'M', 'C']
    ]
    return board

# 打印棋盘（带颜色）
def print_board(board):
    print("当前棋盘状态： 数组表达:\n",board)
    # 打印列坐标（深蓝色）
    print("文字表达:")
    print(Fore.BLUE + "  0  1  2  3  4  5  6  7  8")
    for i in range(10):
        # 打印行坐标（深蓝色）
        print(Fore.BLUE + str(i), end=" ")
        for j in range(9):
            piece = board[i][j]
            name_piece = getName(piece)
            if piece.isupper():  # 红方棋子（红色）
                print(Fore.RED + name_piece, end=" ")
            elif piece.islower():  # 黑方棋子（黑色）
                print(Fore.BLACK + name_piece, end=" ")
            else:  # 空格（默认颜色）
                print("  ", end=" ")
        print()

# 检查移动是否合法
def is_legal_move(board, start, end, player):
    x1, y1 = start
    x2, y2 = end
    piece = board[x1][y1]
    target = board[x2][y2]

    # 检查是否选择自己的棋子
    if (player == 'red' and piece.islower()) or (player == 'black' and piece.isupper()):
        return False

    # 检查目标位置是否为空或是对方的棋子
    if (player == 'red' and target.isupper()) or (player == 'black' and target.islower()):
        return False

    # 车的移动规则
    if piece.lower() == 'c':
        if x1 != x2 and y1 != y2:
            return False
        if x1 == x2:
            step = 1 if y2 > y1 else -1
            for y in range(y1 + step, y2, step):
                if board[x1][y] != ' ':
                    return False
        else:
            step = 1 if x2 > x1 else -1
            for x in range(x1 + step, x2, step):
                if board[x][y1] != ' ':
                    return False
        return True

    # 炮的移动规则
    if piece.lower() == 'p':
        if x1 != x2 and y1 != y2:
            return False
        count = 0  # 记录路径上的棋子数
        if x1 == x2:
            step = 1 if y2 > y1 else -1
            for y in range(y1 + step, y2, step):
                if board[x1][y] != ' ':
                    count += 1
        else:
            step = 1 if x2 > x1 else -1
            for x in range(x1 + step, x2, step):
                if board[x][y1] != ' ':
                    count += 1
        # 如果目标位置为空，路径上不能有棋子
        if target == ' ':
            return count == 0
        # 如果目标位置有棋子，路径上必须有一个棋子（炮架）
        else:
            return count == 1

    # 马的移动规则
    if piece.lower() == 'm':
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        # 马走“日”字
        if not ((dx == 2 and dy == 1) or (dx == 1 and dy == 2)):
            return False
        # 检查是否蹩马腿
        if dx == 2:
            if x2 > x1 and board[x1 + 1][y1] != ' ':
                return False
            if x2 < x1 and board[x1 - 1][y1] != ' ':
                return False
        else:
            if y2 > y1 and board[x1][y1 + 1] != ' ':
                return False
            if y2 < y1 and board[x1][y1 - 1] != ' ':
                return False
        return True

    # 兵/卒的移动规则
    if piece.lower() == 'b' or piece.lower() == 'z':
        dx = x2 - x1
        dy = y2 - y1
        # 红兵
        if piece == 'B':
            if x1 >= 5:  # 未过河
                if not (dx == -1 and dy == 0):  # 只能向前移动一格
                    return False
            else:  # 过河后
                if not (abs(dx) == 1 and dy == 0) and not (dx == 0 and abs(dy) == 1):  # 可以前、左、右移动
                    return False
        # 黑卒
        else:
            if x1 <= 4:  # 未过河
                if not (dx == 1 and dy == 0):  # 只能向前移动一格
                    return False
            else:  # 过河后
                if not (abs(dx) == 1 and dy == 0) and not (dx == 0 and abs(dy) == 1):  # 可以前、左、右移动
                    return False
        return True

    # 象（相）的移动规则
    if piece.lower() == 'x':
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        # 移动必须是对角线两格
        if not (dx == 2 and dy == 2):
            return False
        # 检查是否过河
        if (piece == 'X' and x2 < 5) or (piece == 'x' and x2 > 4):
            return False
        # 检查是否塞象眼
        mid_x = (x1 + x2) // 2
        mid_y = (y1 + y2) // 2
        if board[mid_x][mid_y] != ' ':
            return False
        return True

    # 士（仕）的移动规则
    if piece.lower() == 's':
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        # 移动必须是对角线一格
        if not (dx == 1 and dy == 1):
            return False
        # 检查是否在九宫格内
        if piece == 'S':  # 红士
            if not (7 <= x2 <= 9 and 3 <= y2 <= 5):
                return False
        else:  # 黑士
            if not (0 <= x2 <= 2 and 3 <= y2 <= 5):
                return False
        return True

    # 将/帅的移动规则
    if piece.lower() == 'k':
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        # 移动必须是一格直线
        if not ((dx == 1 and dy == 0) or (dx == 0 and dy == 1)):
            return False
        # 检查是否在九宫格内
        if piece == 'K':  # 红将
            if not (7 <= x2 <= 9 and 3 <= y2 <= 5):
                return False
        else:  # 黑帅
            if not (0 <= x2 <= 2 and 3 <= y2 <= 5):
                return False
        # 检查是否与对方的将/帅直接对面
        if y1 == y2:
            for x in range(min(x1, x2) + 1, max(x1, x2)):
                if board[x][y1] != ' ':
                    return True
            # 如果中间没有棋子，检查是否有对方的将/帅
            if piece == 'K' and any(board[x][y1] == 'k' for x in range(10)):
                return False
            if piece == 'k' and any(board[x][y1] == 'K' for x in range(10)):
                return False
        return True

    return False

# 移动棋子
def move_piece(board, start, end):
    x1, y1 = start
    x2, y2 = end
    board[x2][y2] = board[x1][y1]
    board[x1][y1] = ' '

# 检查是否有一方的将（帅）被吃掉
def check_win(board):
    red_k_exist = any('K' in row for row in board)  # 红方的将是否存在
    black_k_exist = any('k' in row for row in board)  # 黑方的将是否存在
    if not red_k_exist:
        return 'black'  # 红方的将被吃掉，黑方获胜
    if not black_k_exist:
        return 'red'  # 黑方的将被吃掉，红方获胜
    return None  # 游戏继续


def evaluate_move(board, move):

    (x1, y1), (x2, y2) = move
    target_piece = board[x2][y2]

    # 如果目标位置有对方的棋子，赋予较高权重
    if target_piece and target_piece.isupper():
        return 10  # 吃掉对方棋子
    elif (x2, y2) in [(4, 4), (5, 4), (4, 5), (5, 5)]:
        return 5  # 移动到中心区域
    else:
        return 1  # 普通移动

# 简单的 AI 对手
def ai_move(board):

    from random import choices

    # 预生成所有合法的移动
    legal_moves = []
    move_weights = []  # 每个移动的权重

    for x1 in range(10):
        for y1 in range(9):
            for x2 in range(10):
                for y2 in range(9):
                    if is_legal_move(board, (x1, y1), (x2, y2), 'black'):
                        move = ((x1, y1), (x2, y2))
                        legal_moves.append(move)
                        # 根据移动的价值分配权重（这里假设价值由 evaluate_move 函数计算）
                        weight = evaluate_move(board, move)
                        move_weights.append(weight)

    if not legal_moves:
        return None

    # 根据权重选择移动（权重越高，被选中的概率越大）
    return choices(legal_moves, weights=move_weights, k=1)[0]
    
    
# 主游戏循环
def main():
    board = init_board()
    player = 'red'
    print("欢迎来到中国象棋人机对战游戏！")
    print("1、棋子含义,红方/黑方名字和英文字母如下")
    print("   将/帅: K/k, 仕/士: S/s, 相/象: X/x, 傌/马: M/m, 俥/车: C/c, 炮/砲: P/p, 兵/卒: B/z")    
    print("   黑方： 将、车、马、砲、象、士、卒" )
    print("   红方： 帅、俥、傌、炮、相、仕、兵" )
    print("   红方（英文大写）先走，黑方（英文小写）")
    print("2、 输入移动指令，例如：7 7 7 4 表示将红炮(P)从(7行,7列)移动到(7行,4列)。")

    while True:
        print_board(board)        
        winner = check_win(board)
        if winner:
            print(f"游戏结束！{winner} 方获胜！")
            break

        if player == 'red':
            # 玩家输入
            try:
                x1, y1, x2, y2 = map(int, input("请输入红方移动信息(源位置 => 目标位置： 行 列 行 列):").split())
                start, end = (x1, y1), (x2, y2)
                if not is_legal_move(board, start, end, player):
                    print("非法移动，请重试！")
                    continue
                print(f"红方走子： {start} -> {end} 走棋成功！")
            except ValueError:
                print("输入格式错误，请重试！")
                continue
        else:
            # AI 移动
            print("黑方 正在思考...")
            start, end = ai_move(board)
            print(f"黑方移动：{start} -> {end}")

        # 执行移动
        move_piece(board, start, end)

        # 切换玩家
        player = 'black' if player == 'red' else 'red'

# 运行游戏
if __name__ == "__main__":
    main()