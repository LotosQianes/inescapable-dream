import pygame

# 初始化 Pygame
pygame.init()

# 设置屏幕尺寸
screen_width = 400
screen_height = 300
screen = pygame.display.set_mode((screen_width, screen_height))

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)  # 门的内部颜色

# 画门的函数
def draw_pixel_door(screen, x, y, width, height, frame_width):
    # 画门框顶部和弧度部分
    for i in range(frame_width):
        pygame.draw.line(screen, BLACK, (x + frame_width - i, y + i), (x + width - frame_width + i, y + i))
    
    # 画弧度部分（左上和右上）
    for i in range(1, frame_width):
        pygame.draw.line(screen, BLACK, (x + frame_width - i, y + i), (x + frame_width, y + i))
        pygame.draw.line(screen, BLACK, (x + width - frame_width + i, y + i), (x + width - frame_width, y + i))

    # 画门框左右两边
    for i in range(height):
        pygame.draw.line(screen, BLACK, (x, y + i), (x + frame_width, y + i))
        pygame.draw.line(screen, BLACK, (x + width - frame_width, y + i), (x + width, y + i))

    # 画门框底部
    for i in range(frame_width):
        pygame.draw.line(screen, BLACK, (x + i, y + height - i), (x + width - i, y + height - i))
    
    # 画门内灰色部分
    pygame.draw.rect(screen, GRAY, (x + frame_width, y + frame_width, width - 2 * frame_width, height - frame_width))

# 主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)  # 背景色
    draw_pixel_door(screen, 120, 50, 80, 100, 4)  # 画门，调整宽度和高度以及框架宽度以匹配参考图

    pygame.display.flip()

pygame.quit()