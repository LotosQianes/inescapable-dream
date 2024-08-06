import pygame
import random

class TitleScene:
	def __init__(self, screen, settings):
		"""初始化场景特效"""
		self.screen = screen
		self.settings = settings

		#粒子列表
		self.particles = []

	def draw_border(self, shrink_factor=0):
		"""绘制边框"""
		border_color = (106, 57, 6)
		border_thickness = 10

		# 调整边框的厚度
		current_thickness = max(border_thickness - shrink_factor, 0)

		if current_thickness <= 0:
			return  # 边框完全消失

		# 使用 current_thickness 绘制边框，不移动边框位置
		pygame.draw.rect(self.screen, border_color,
			(0, 0, self.settings.screen_width, current_thickness))  # 上边框
		pygame.draw.rect(self.screen, border_color,
			(0, 0, current_thickness, self.settings.screen_high))  # 左边框
		pygame.draw.rect(self.screen, border_color,
			(0, self.settings.screen_high - current_thickness, self.settings.screen_width, current_thickness))  # 下边框
		pygame.draw.rect(self.screen, border_color,
			(self.settings.screen_width - current_thickness, 0, current_thickness, self.settings.screen_high))  # 右边框


	def draw_particles(self):
		"""绘制粒子效果"""
		if len(self.particles) < 100:
			#这里列表particles使用了嵌套结构
			#即为particles[[x, y], [vx, vy], radius]
			self.particles.append([[random.randint(0, self.settings.screen_width),random.randint(0, self.settings.screen_high)], #随机生成粒子的位置，确保粒子在屏幕内
			  [random.uniform(-1, 1), random.uniform(-1, 1)],	#随机粒子的速度，确保以任意方向移动
			   random.randint(2, 4)])	#随机粒子的半径

		for particle in self.particles:
			particle[0][0] += particle[1][0]	#更新粒子x坐标
			particle[0][1] += particle[1][1]	#更新粒子y坐标
			particle[2] -= 0.01		#逐渐缩小粒子半径
			if particle[2] <= 0:	#当粒子半径小于0时从粒子列表中抹除
				self.particles.remove(particle)

			pygame.draw.circle(self.screen, (255, 255, 255),\
			 (int(particle[0][0]), int(particle[0][1])), int(particle[2]))

	def render(self, shrink_factor=0):
		"""渲染场景特效"""
		self.draw_border(shrink_factor)
		self.draw_particles()