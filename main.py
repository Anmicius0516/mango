import pygame
import sys
import random

# === 1. 基础配置与常量定义 ===
pygame.init()
pygame.font.init() 

GRID_SIZE = 30  
COLS = 10
ROWS = 20
GAME_WIDTH = COLS * GRID_SIZE
GAME_HEIGHT = ROWS * GRID_SIZE
WINDOW_WIDTH = GAME_WIDTH + 240 # 稍微加宽一点留白，给计分器大舞台
WINDOW_HEIGHT = GAME_HEIGHT

# 颜色大升级 (引入霓虹科技风)
BLACK = (15, 15, 22)         # 更深邃的星空黑
GRID_COLOR = (35, 35, 50)    # 带点暗蓝的网格线
NAVY_BLUE = (22, 28, 45)     # 游戏主区域背景色
WHITE = (240, 240, 255)
PANEL_BG = (30, 38, 60)      # 计分器相框背景色
PANEL_BORDER = (0, 255, 150) # 计分器外框线（霓虹绿）
SCORE_COLOR = (255, 180, 0)  # 分数颜色（亮金色）

SHAPES = {
    'I': [[0,0,0,0], [1,1,1,1], [0,0,0,0], [0,0,0,0]],
    'O': [[1,1,0,0], [1,1,0,0], [0,0,0,0], [0,0,0,0]],
    'T': [[0,1,0,0], [1,1,1,0], [0,0,0,0], [0,0,0,0]],
    'S': [[0,1,1,0], [1,1,0,0], [0,0,0,0], [0,0,0,0]],
    'Z': [[1,1,0,0], [0,1,1,0], [0,0,0,0], [0,0,0,0]],
    'J': [[1,0,0,0], [1,1,1,0], [0,0,0,0], [0,0,0,0]],
    'L': [[0,0,1,0], [1,1,1,0], [0,0,0,0], [0,0,0,0]]
}

SHAPE_COLORS = {
    'I': (0, 240, 240), 'O': (240, 240, 0), 'T': (160, 32, 240),
    'S': (0, 240, 0),   'Z': (240, 0, 0),   'J': (0, 0, 240),   'L': (240, 160, 0)
}

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("芒果方块 - Tetris Pro")
clock = pygame.time.Clock()

# 准备不同字号的字体
font_title = pygame.font.SysFont("simhei", 20, bold=True) # 标题用粗体
font_value = pygame.font.SysFont("arial", 28, bold=True) # 数字用大粗体
font_tips = pygame.font.SysFont("simhei", 16)
#定义游戏结束的字体（用黑体，40号大字，加粗）
game_over_font = pygame.font.SysFont("simhei", 40, bold=True)

# 游戏状态变量 (新增等级和行数计数)
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
score = 0
total_lines = 0
level = 1
game_over = False

# === 2. 方块类 ===
class Tetromino:
    def __init__(self):
        self.type = random.choice(list(SHAPES.keys()))
        self.matrix = SHAPES[self.type]
        self.color = SHAPE_COLORS[self.type]
        self.row = 0
        self.col = 3

    def draw(self):
        for r in range(len(self.matrix)):
            for c in range(len(self.matrix[r])):
                if self.matrix[r][c] == 1:
                    x = (self.col + c) * GRID_SIZE
                    y = (self.row + r) * GRID_SIZE
                    # 边缘留 1 像素黑边，让方块看起来有关节感、更精致
                    pygame.draw.rect(screen, self.color, (x, y, GRID_SIZE - 1, GRID_SIZE - 1))

    def can_move(self, next_row, next_col, next_matrix=None):
        if next_matrix is None:
            next_matrix = self.matrix
            
        for r in range(len(next_matrix)):
            for c in range(len(next_matrix[r])):
                if next_matrix[r][c] == 1:
                    target_row = next_row + r
                    target_col = next_col + c
                    
                    if target_col < 0 or target_col >= COLS or target_row >= ROWS:
                        return False
                    if target_row >= 0 and grid[target_row][target_col] != 0:
                        return False
        return True

    def rotate(self):
        new_matrix = [list(x) for x in zip(*self.matrix[::-1])]
        if self.can_move(self.row, self.col, new_matrix):
            self.matrix = new_matrix

# === 3. 核心控制逻辑 ===
def lock_piece(piece):
    for r in range(len(piece.matrix)):
        for c in range(len(piece.matrix[r])):
            if piece.matrix[r][c] == 1:
                if piece.row + r >= 0:
                    grid[piece.row + r][piece.col + c] = piece.color

def check_clear_lines():
    global score, total_lines, level
    lines_cleared = 0
    
    r = ROWS - 1
    while r >= 0:
        if 0 not in grid[r]:
            lines_cleared += 1
            del grid[r]
            grid.insert(0, [0 for _ in range(COLS)])
        else:
            r -= 1
            
    if lines_cleared > 0:
        total_lines += lines_cleared
        # 经典计分：消单行100，双行300，三行500，四行800（鼓励多消）
        rewards = [0, 100, 300, 500, 800]
        score += rewards[min(lines_cleared, 4)]
        
        # 每消 5 行升一级，方块会越来越快！
        level = (total_lines // 5) + 1
        new_speed = max(100, 400 - (level - 1) * 50)
        pygame.time.set_timer(FALL_EVENT, new_speed)

def draw_hud_panel():
    """绘制高科技计分大相框面板"""
    panel_x = GAME_WIDTH + 20
    panel_w = 200
    
    # 1. 绘制『SCORE 计分大卡片』
    pygame.draw.rect(screen, PANEL_BG, (panel_x, 30, panel_w, 90), border_radius=8)
    pygame.draw.rect(screen, PANEL_BORDER, (panel_x, 30, panel_w, 90), width=2, border_radius=8)
    
    lbl_score = font_title.render("SCORE", True, WHITE)
    val_score = font_value.render(str(score).zfill(6), True, SCORE_COLOR) # 不足6位用0补齐，像街机一样
    screen.blit(lbl_score, (panel_x + 15, 40))
    screen.blit(val_score, (panel_x + 15, 70))
    
    # 2. 绘制『DATA 数据统计卡片（等级与消除行）』
    pygame.draw.rect(screen, PANEL_BG, (panel_x, 150, panel_w, 140), border_radius=8)
    pygame.draw.rect(screen, PANEL_BORDER, (panel_x, 150, panel_w, 140), width=1, border_radius=8)
    
    lbl_level = font_title.render("LEVEL", True, WHITE)
    val_level = font_value.render(f"Lv.{level}", True, WHITE)
    lbl_lines = font_title.render("LINES", True, WHITE)
    val_lines = font_value.render(str(total_lines), True, (0, 191, 255))
    
    screen.blit(lbl_level, (panel_x + 15, 160))
    screen.blit(val_level, (panel_x + 15, 185))
    screen.blit(lbl_lines, (panel_x + 15, 225))
    screen.blit(val_lines, (panel_x + 15, 250))
    
    # 3. 底部操作指南提示
    pygame.draw.rect(screen, (25, 25, 35), (panel_x, 420, panel_w, 150), border_radius=8)
    tips = ["▲ : 变形 (Rotate)", "◀ ▶ : 左右移动", "▼ : 加速下落", "Ctrl+C : 退出游戏"]
    for i, tip in enumerate(tips):
        txt = font_tips.render(tip, True, (150, 150, 160))
        screen.blit(txt, (panel_x + 10, 435 + i * 26))

def draw_grid_and_map():
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] != 0:
                pygame.draw.rect(screen, grid[r][c], (c * GRID_SIZE, r * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))

    for c in range(COLS + 1):
        pygame.draw.line(screen, GRID_COLOR, (c * GRID_SIZE, 0), (c * GRID_SIZE, GAME_HEIGHT))
    for r in range(ROWS + 1):
        pygame.draw.line(screen, GRID_COLOR, (0, r * GRID_SIZE), (GAME_WIDTH, r * GRID_SIZE))

# === 4. 游戏初始化 ===
current_piece = Tetromino()

FALL_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(FALL_EVENT, 400) 

# === 5. 游戏主循环 ===
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if not game_over:
            if event.type == FALL_EVENT:
                if current_piece.can_move(current_piece.row + 1, current_piece.col):
                    current_piece.row += 1
                else:
                    lock_piece(current_piece)
                    check_clear_lines() 
                    current_piece = Tetromino()
                    if not current_piece.can_move(current_piece.row, current_piece.col):
                        game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if current_piece.can_move(current_piece.row, current_piece.col - 1):
                        current_piece.col -= 1
                elif event.key == pygame.K_RIGHT:
                    if current_piece.can_move(current_piece.row, current_piece.col + 1):
                        current_piece.col += 1
                elif event.key == pygame.K_DOWN:
                    if current_piece.can_move(current_piece.row + 1, current_piece.col):
                        current_piece.row += 1
                elif event.key == pygame.K_UP:
                    current_piece.rotate()

    # --- 画面渲染 ---
    screen.fill(BLACK) 
    pygame.draw.rect(screen, NAVY_BLUE, (0, 0, GAME_WIDTH, GAME_HEIGHT))
    
    draw_grid_and_map()
    
    if not game_over:
        current_piece.draw()
    else:
        go_text = game_over_font.render("GAME OVER", True, (255, 50, 50))
        screen.blit(go_text, (GAME_WIDTH // 2 - 100, GAME_HEIGHT // 2 - 20))
        
    draw_hud_panel() # 渲染大升级后的高级计分面板

    pygame.display.flip()
    clock.tick(60)