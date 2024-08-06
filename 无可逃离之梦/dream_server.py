import pygame

class MoonJeongho:
	"""玩家MoonJeongho的类"""

	def __init__(self, screen):
		"""初始化玩家并设置其起始位置"""
		self.screen = screen
		self.screen_rect = screen.get_rect()

		#设置玩家的尺寸和颜色
		self.width, self.height = 50, 50
		self.color = (0, 0, 0)

		#创建玩家的矩形
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.midbottom = self.screen_rect.midbottom

		#存储玩家位置的小数值
		self.x = float(self.rect.x)
		self.y = float(self.rect.y)

		#移动标志
		self.moving_right = False
		self.moving_left = False
		self.jump_sign = False

		#移动速度
		self.speed = 5
		self.jump_speed = self.player_jump_speed = 20
		self.gravity = 1
		self.vertical_speed = 0

		#确保玩家不会在空中连续跳跃
		self.can_jump = True

		#玩家死亡
		self.dead = False

	def update(self):
		"""根据移动标志调整玩家的位置"""

		#跳跃逻辑
		if self.jump_sign and self.can_jump:
			self.y -= self.jump_speed
			self.jump_speed -= self.gravity
			if self.jump_speed < -self.player_jump_speed:
				self.jump_speed = self.player_jump_speed
				self.jump_sign = False

		#更新玩家的rect对象
		self.rect.x, self.rect.y = int(self.x), int(self.y)

	def _update_title_scene(self):
		"""更新标题界面的玩家位置和边界检查"""
		# 确保玩家不会超出屏幕边界
		if self.moving_right and self.rect.right < self.screen_rect.right - 10:
			self.x += self.speed
		if self.moving_left and self.rect.left > 10:
			self.x -= self.speed
		if self.rect.bottom > self.screen_rect.bottom - 10:
			self.y = self.screen_rect.bottom - 10 - self.height
			self.can_jump = True

		#跳跃逻辑
		if self.jump_sign and self.can_jump:
			self.y -= self.jump_speed
			self.jump_speed -= self.gravity
			if self.y >= self.screen_rect.bottom - self.height - 10:
				self.y = self.screen_rect.bottom - self.height - 10
				self.jump_speed = self.player_jump_speed
				self.jump_sign = False

		#更新玩家的rect对象
		self.rect.x, self.rect.y = int(self.x), int(self.y)

	def _update_step_1_scene(self, step_1_scene):
		"""更新游戏场景的玩家位置和边界检查"""
		self.player_step_1_scene = step_1_scene

		# 确保玩家不会超出屏幕边界
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.x += self.speed
		if self.moving_left and self.rect.left > 0:
			self.x -= self.speed
		if self.rect.bottom > self.player_step_1_scene.floor_y + 1:
			self.y = self.player_step_1_scene.floor_y - self.height + 1
			self.can_jump = True

		#跳跃逻辑
		if self.jump_sign and self.can_jump:
			self.y -= self.jump_speed
			self.jump_speed -= self.gravity
			if self.y >= self.player_step_1_scene.floor_y - self.height:
				self.y = self.player_step_1_scene.floor_y - self.height
				self.jump_speed = self.player_jump_speed
				self.jump_sign = False

		# 更新玩家的rect对象
		self.rect.x, self.rect.y = int(self.x), int(self.y)

		if self.player_step_1_scene.check_collision(self.rect):
			self.dead = True
			

	def blitme(self):
		"""在指定位置绘制玩家"""
		pygame.draw.rect(self.screen, self.color, self.rect)

	def jump(self):
		"""使玩家跳跃"""
		if self.can_jump:
			self.jump_sign = True