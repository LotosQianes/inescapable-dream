import pygame
import random

class PlayerEffects:
	"""管理玩家特效的类"""

	def __init__(self, player, screen, settings):
		"""初始化特效"""
		self.screen = screen
		self.player = player
		self.settings = settings
		self.trails = []  # 存储拖尾特效的列表
		self.jump_effects = []  # 存储跳跃特效的列表
		self.explosion_effects = []  # 存储爆炸特效的列表
		self.explosion_start_time = 0  # 爆炸开始的时间

	def add_trail(self, rect, color, direction):
		"""添加拖尾特效"""
		for _ in range(1):  # 每次添加多个粒子
			if direction == "right":
				pos = (rect.right, rect.y + random.randint(0, rect.height))
				vel = [random.uniform(1, 3), random.uniform(-1, 1)]
			else:
				pos = (rect.left, rect.y + random.randint(0, rect.height))
				vel = [random.uniform(-1, -3), random.uniform(-1, 1)]
			trail = {
				'pos': [pos[0], pos[1]],
				'vel': vel,
				'size': random.randint(4, 8),
				'color': color,
				'alpha': 255
			}
			self.trails.append(trail)

	def add_jump_effect(self, rect, color):
		"""添加跳跃特效"""
		for _ in range(10):  # 每次添加多个粒子
			pos = (rect.x + random.randint(0, rect.width), rect.bottom)
			vel = [random.uniform(-1, 1), random.uniform(1, 3)]
			effect = {
				'pos': [pos[0], pos[1]],
				'vel': vel,
				'size': random.randint(4, 8),
				'color': color,
				'alpha': 255
			}
			self.jump_effects.append(effect)

	def add_explosion_effect(self, rect, color):
		"""添加爆炸特效"""
		for _ in range(10):  # 每次添加多个粒子
			pos = (rect.centerx, rect.centery)
			vel = [random.uniform(-3, 3), random.uniform(-3, 3)]
			explosion = {
				'pos': [pos[0], pos[1]],
				'vel': vel,
				'size': random.randint(4, 8),
				'color': color,
				'alpha': 255
			}
			self.explosion_effects.append(explosion)

	def update_trails(self):
		"""更新拖尾特效"""
		for trail in self.trails:
			trail['pos'][0] += trail['vel'][0]
			trail['pos'][1] += trail['vel'][1]
			trail['alpha'] -= 5
			if trail['alpha'] <= 0:
				self.trails.remove(trail)

	def update_jump_effects(self):
		"""更新跳跃特效"""
		for effect in self.jump_effects:
			effect['pos'][0] += effect['vel'][0]
			effect['pos'][1] += effect['vel'][1]
			effect['alpha'] -= 10
			if effect['alpha'] <= 0:
				self.jump_effects.remove(effect)

	def update_explosion_effects(self):
		"""更新爆炸特效"""
		if self.explosion_start_time >= 100:
			# 重新聚合成玩家方块
			self.explosion_effects = []
			return True  # 表示玩家已重新聚合
		for explosion in self.explosion_effects:
			explosion['pos'][0] += explosion['vel'][0]
			explosion['pos'][1] += explosion['vel'][1]
			explosion['alpha'] -= 5
			if explosion['alpha'] <= 0:
				self.explosion_effects.remove(explosion)
		return False

	def draw_trails(self):
		"""绘制拖尾特效"""
		for trail in self.trails:
			surf = pygame.Surface((trail['size'], trail['size']), pygame.SRCALPHA)
			surf.fill(trail['color'] + (trail['alpha'],))
			self.screen.blit(surf, trail['pos'])

	def draw_jump_effects(self):
		"""绘制跳跃特效"""
		for effect in self.jump_effects:
			surf = pygame.Surface((effect['size'], effect['size']), pygame.SRCALPHA)
			surf.fill(effect['color'] + (effect['alpha'],))
			self.screen.blit(surf, effect['pos'])

	def draw_explosion_effects(self):
		"""绘制爆炸特效"""
		for explosion in self.explosion_effects:
			surf = pygame.Surface((explosion['size'], explosion['size']), pygame.SRCALPHA)
			surf.fill(explosion['color'] + (explosion['alpha'],))
			self.screen.blit(surf, explosion['pos'])

	def update(self):
		"""更新所有特效"""
		self.update_trails()
		self.update_jump_effects()
		return self.update_explosion_effects()

	def draw(self):
		"""绘制所有特效"""
		self.draw_trails()
		self.draw_jump_effects()
		self.draw_explosion_effects()