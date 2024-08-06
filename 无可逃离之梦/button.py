import pygame.font
from time import sleep
import time

class Button:
	"""管理渲染文字以及按钮属性的类"""
	def __init__(self, ai_game, msg, start, quit, title):
		"""初始化按钮属性"""
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()

		#设计关卡显示尺寸
		self.step_width, self.step_height = 600, 300
		self.text_color = (255, 255, 255)
		self.text_shadow_color = (0, 0, 0)

		#设计关卡显示的按钮属性
		self.rect = pygame.Rect(0, 0, self.step_width, self.step_height)
		self.rect.center = self.screen_rect.center

		#设计开始显示尺寸
		self.start_width, self.start_height = 900, 200
		self.start_color = (106, 57, 6)
		self.start_shadow_color = (0, 0, 0)

		#设计开始显示的按钮属性
		self.start_rect = pygame.Rect(0, 0, self.start_width, self.start_height)
		self.start_rect.center = self.screen_rect.center

		#设计退出显示尺寸
		self.quit_width, self.quit_height = 900, 200
		self.quit_color = (106, 57, 6)
		self.quit_shadow_color = (0, 0, 0)

		#设计退出显示的按钮属性
		self.quit_rect = pygame.Rect(0, 0, self.start_width, self.start_height)
		self.quit_rect.center = self.screen_rect.center

		#设计标题显示尺寸
		self.title_width, self.title_height = 900, 200
		self.title_color = (106, 57, 6)
		self.title_shadow_color = (0, 0, 0)

		#设计标题显示的按钮属性
		self.title_rect = pygame.Rect(0, 0, self.title_width, self.title_height)
		self.title_rect.center = self.screen_rect.center

		font_path = 'E:/python_work/python_work_1/闲时拓展/无可逃离之梦/Monocraft-nerd-fonts-patched.ttf'
		self.font = pygame.font.Font(font_path, 200)

		self._prep_step_msg(msg)
		self._prep_start_msg(start)
		self._prep_quit_msg(quit)
		self._prep_title_msg(title)

		#设计按钮旁三角的属性
		self.triangle_color = (106, 57, 6)
		#创建一个30*30的透明表面
		self.start_triangle_surface = pygame.Surface((30, 30), pygame.SRCALPHA)
		self.quit_triangle_surface = pygame.Surface((30, 30), pygame.SRCALPHA)
		self.start_triangle_rect = self.start_triangle_surface.get_rect()
		self.quit_triangle_rect = self.quit_triangle_surface.get_rect()
		#控制三角显示
		self.start_triangle_visible = False
		self.quit_triangle_visible = False
		#创建三角图案
		self.start_triangle = self._create_start_triangle()
		self.quit_triangle = self._create_quit_triangle()

	def _prep_step_msg(self, msg):
		#渲染关卡名称
		#关卡名称
		self.msg_image = self.font.render(msg, True, self.text_color)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center

		#关卡剪影
		self.msg_shadow_image = self.font.render(msg, True, self.text_shadow_color)
		self.msg_shadow_image_rect = self.msg_shadow_image.get_rect()
		self.msg_shadow_image_rect.center = self.rect.center

		#调整像素偏移量，说明xy轴的偏移量
		offset_x, offset_y = -5, 5
		self.msg_shadow_image_rect.move_ip(offset_x, offset_y)

	def draw_step_1(self, alpha):
		#绘制Step 1以及其剪影
		self.msg_image.set_alpha(alpha)
		self.msg_shadow_image.set_alpha(alpha)
		self.screen.blit(self.msg_shadow_image, self.msg_shadow_image_rect)
		self.screen.blit(self.msg_image, self.msg_image_rect)

	def _prep_start_msg(self, start):
		#渲染开始按钮
		start_font = pygame.font.Font('E:/python_work/python_work_1/闲时拓展/无可逃离之梦/Monocraft-nerd-fonts-patched.ttf', 130)
		self.start_image = start_font.render(start, True, self.start_color)
		self.start_image_rect = self.start_image.get_rect()
		self.start_image_rect.center = self.start_rect.center

		#调整剪影偏移量
		offset_x, offset_y = 0, 200
		self.start_image_rect.move_ip(offset_x, offset_y)

		#渲染开始按钮剪影
		self.start_shadow_image = start_font.render(start, True, self.start_shadow_color)
		self.start_shadow_image_rect = self.start_shadow_image.get_rect()
		self.start_shadow_image_rect.center = self.start_rect.center

		#调整剪影偏移量
		offset_x, offset_y = -5, 205
		self.start_shadow_image_rect.move_ip(offset_x, offset_y)

		# 调整碰撞检测矩形的位置
		self.start_rect.move_ip(0, 200)

	def draw_start(self, alpha):
		#绘制Start以及其剪影,指示特效
		self.start_image.set_alpha(alpha)
		self.start_shadow_image.set_alpha(alpha)
		self.screen.blit(self.start_shadow_image, self.start_shadow_image_rect)
		self.screen.blit(self.start_image, self.start_image_rect)

		if self.start_triangle_visible:
			self.screen.blit(*self.start_triangle)

	def _prep_quit_msg(self, quit):
		#渲染退出按钮
		quit_font = pygame.font.Font('E:/python_work/python_work_1/闲时拓展/无可逃离之梦/Monocraft-nerd-fonts-patched.ttf', 130)
		self.quit_image = quit_font.render(quit, True, self.quit_color)
		self.quit_image_rect = self.quit_image.get_rect()
		self.quit_image_rect.center = self.quit_rect.center

		#调整剪影偏移量
		offset_x, offset_y = 0, 400
		self.quit_image_rect.move_ip(offset_x, offset_y)

		#渲染退出按钮剪影
		self.quit_shadow_image = quit_font.render(quit, True, self.quit_shadow_color)
		self.quit_shadow_image_rect = self.quit_shadow_image.get_rect()
		self.quit_shadow_image_rect.center = self.quit_rect.center

		#调整剪影偏移量
		offset_x, offset_y = -5, 405
		self.quit_shadow_image_rect.move_ip(offset_x, offset_y)

		# 调整碰撞检测矩形的位置
		self.quit_rect.move_ip(0, 400)

	def draw_quit(self, alpha):
		#绘制quit以及其剪影,指示特效
		self.quit_image.set_alpha(alpha)
		self.quit_shadow_image.set_alpha(alpha)
		self.screen.blit(self.quit_shadow_image, self.quit_shadow_image_rect)
		self.screen.blit(self.quit_image, self.quit_image_rect)

		if self.quit_triangle_visible:
			self.screen.blit(*self.quit_triangle)

	def _prep_title_msg(self, title):
		#渲染退标题按钮
		title_font = pygame.font.Font('E:/python_work/python_work_1/闲时拓展/无可逃离之梦/Monocraft-nerd-fonts-patched.ttf', 140)
		self.title_image = title_font.render(title, True, self.title_color)
		self.title_image_rect = self.title_image.get_rect()
		self.title_image_rect.center = self.title_rect.center

		#调整剪影偏移量
		offset_x, offset_y = 0, -300
		self.title_image_rect.move_ip(offset_x, offset_y)

		#渲染标题按钮剪影
		self.title_shadow_image = title_font.render(title, True, self.title_shadow_color)
		self.title_shadow_image_rect = self.title_shadow_image.get_rect()
		self.title_shadow_image_rect.center = self.title_rect.center

		#调整剪影偏移量
		offset_x, offset_y = -5, -295
		self.title_shadow_image_rect.move_ip(offset_x, offset_y)

		# 调整碰撞检测矩形的位置
		self.title_rect.move_ip(0, 400)

	def draw_title(self, alpha):
		#绘制title以及其剪影,指示特效
		self.title_image.set_alpha(alpha)
		self.title_shadow_image.set_alpha(alpha)
		self.screen.blit(self.title_shadow_image, self.title_shadow_image_rect)
		self.screen.blit(self.title_image, self.title_image_rect)

	def  _create_start_triangle(self):
		"""绘制按钮三角图案"""
		pygame.draw.polygon(self.start_triangle_surface, self.triangle_color, [(0, 0), (30, 15), (0, 30)])
		self.start_triangle_rect.midright = self.start_image_rect.midleft
		self.start_triangle_rect.x -= 100
		return self.start_triangle_surface, self.start_triangle_rect

	def  _create_quit_triangle(self):
		"""绘制按钮三角图案"""
		pygame.draw.polygon(self.quit_triangle_surface, self.triangle_color, [(0, 0), (30, 15), (0, 30)])
		self.quit_triangle_rect.midright = self.quit_image_rect.midleft
		self.quit_triangle_rect.x -= 100
		return self.quit_triangle_surface, self.quit_triangle_rect

	def show_start_triangle(self):
		#控制start三角显现
		self.start_triangle_visible = True

	def show_quit_triangle(self):
		#控制quit三角显现
		self.quit_triangle_visible = True

	def hide_start_triangle(self):
		#控制start三角消失
		self.start_triangle_visible = False

	def hide_quit_triangle(self):
		#控制quit三角消失
		self.quit_triangle_visible = False

	def move_start(self):
		#开始按钮点击反馈
		self.start_image_rect.move_ip(-5, 5)
		self.start_rect.move_ip(-5, 5)
		self.blinking = True