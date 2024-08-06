import pygame
import math

class Step1Scene:
	def __init__(self, screen, settings):
		"""初始化关卡一场景生成"""
		self.screen = screen
		self.settings = settings

		self.color = (106, 57, 6)

		#初始化地板的位置和尺寸
		self.floor_width = self.settings.screen_width
		self.floor_height = 0
		self.floor_x = 0
		self.floor_y = self.settings.screen_high - self.floor_height

		#地板上升速度
		self.floor_speed = 1

		#圆锯参数
		self.saw_color = (106, 57, 6)
		self.saw_center_color = (106, 57, 6)
		self.saw_center_x = self.floor_width * 3 // 4
		self.saw_center_y = self.floor_y
		self.saw_radius = 50  #可调整大小
		self.saw_num_teeth = 20
		self.saw_hole_radius = 10
		self.saw_angle_speed = 0.05
		self.saw_angle = 0

		#标记地板是否完全升起
		self.floor_risen = False

		#标记圆锯是否可上升
		self.saw_half_risen = False

		#标记圆锯是否能继续行动
		self.operation_sawing = False

	def update(self, player_rect):
		"""更新地板和圆锯的位置"""
		#如果地板还没有上升到屏幕的六分之一高度，则继续上升
		if self.floor_y > self.settings.screen_high * 5 / 6:
			self.floor_height += self.floor_speed
			self.floor_y -= self.floor_speed
		else:
			self.floor_risen = True  # 地板已经完全升起

		#如果玩家接近圆锯片，圆锯片升起
		if player_rect.right + 140 > self.saw_center_x and not self.operation_sawing:
			self.saw_half_risen = True
			self.saw_center_y -= 10
			if self.saw_center_y <= 900:
				self.operation_sawing = True

		#更新圆锯角度，实现旋转效果
		if self.floor_risen:
			self.saw_angle += self.saw_angle_speed

	def draw_step_1_floor(self):
		"""绘制关卡一地上板块1"""
		pygame.draw.rect(self.screen, self.color, (self.floor_x, self.floor_y, self.floor_width, self.floor_height))

	def draw_saw(self):
		"""绘制圆锯"""
		if self.floor_risen:
			if not self.saw_half_risen:
				self.saw_center_y = self.floor_y + self.floor_height // 2  # 确保圆锯片位置在地板内
			cx, cy = self.saw_center_x, self.saw_center_y
			points = []

			for i in range(self.saw_num_teeth * 2):
				angle_i = (i * math.pi) / self.saw_num_teeth + self.saw_angle
				if i % 2 == 0:
					x = cx + (self.saw_radius * math.cos(angle_i))
					y = cy + (self.saw_radius * math.sin(angle_i))
				else:
					x = cx + ((self.saw_radius - 10) * math.cos(angle_i))
					y = cy + ((self.saw_radius - 10) * math.sin(angle_i))
				points.append((x, y))

			pygame.draw.polygon(self.screen, self.saw_color, points)
			pygame.draw.circle(self.screen, self.saw_center_color, (cx, cy), self.saw_hole_radius)

	def check_collision(self, player_rect):
		"""检查玩家是否与圆锯片碰撞"""
		if self.floor_risen:
			saw_rect = pygame.Rect(self.saw_center_x - self.saw_radius,
									self.saw_center_y - self.saw_radius,
								   self.saw_radius * 2,
								    self.saw_radius * 2)
			return player_rect.colliderect(saw_rect)
		return False

	def render(self):
		"""渲染关卡一场景"""
		self.draw_step_1_floor()
		self.draw_saw()