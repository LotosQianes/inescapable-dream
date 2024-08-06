#无可逃离之梦
import sys
from time import sleep
import pygame
import time

from settings import Settings
from button import Button
from game_stats import GameStats
from title_scene import TitleScene
from inescapable_dream_bgm import BGM
from dream_server import MoonJeongho
from step_1_scene import Step1Scene
from player_effects import PlayerEffects

class InescapableDream:
	"""管理游戏资源与行为的类"""

	def __init__(self):
		"""初始化游戏并创建资源"""
		pygame.init()

		self.settings = Settings()
		#创建显示窗口,全屏显示
		self.screen = pygame.display.set_mode(
			(0, 0), pygame.FULLSCREEN)
		self.settings.screen_width = self.screen.get_rect().width
		self.settings.screen_high = self.screen.get_rect().height
		#标题
		pygame.display.set_caption("Inescapable Dream, 无可逃离之梦")

		#创建一个存储统计游戏信息的实例
		self.stats = GameStats(self)

		#绘制信息
		self.button = Button(self, "Step 1", "START", "QUIT", "Inescapable Dream")
		self.clock = pygame.time.Clock()
		self.start_time = time.time()
		self.duration = 2 #每个阶段两秒
		self.alpha = 0
		self.fading_in = True #控制字幕淡出

		#创建TitleScene实例
		self.title_scene = TitleScene(self.screen, self.settings)

		#创建MoonJeongho实例
		self.player = MoonJeongho(self.screen)

		#创建关卡一Step1Scene实例
		self.step_1_scene = Step1Scene(self.screen, self.settings)

		#创建玩家活动特效实例
		self.player_effects = PlayerEffects(self.player, self.screen, self.settings)

		#等待计时器
		self.timer = 0

		#创建BGM实例
		#指定音乐文件夹路径
		self.bgm = BGM('E:/python_work/python_work_1/闲时拓展/无可逃离之梦/Music')
		self.play_start_menu_music()


		#等待变量
		self.showing_start = True
		self.start_waiting = False
		self.showing_step_1 = False
		self.alpha_start = False
		self.shrink_factor = 0  # 初始化边框擦除因子
		self.shrinking = False  # 是否正在擦除边框

	def run_game(self):
		"""游戏主循环"""
		while True:
			self._check_events()
			self._update_screen()
			self.clock.tick(60)


	def _check_events(self):
		"""响应键盘鼠标事件"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				start_pos = pygame.mouse.get_pos()
				quit_pos = pygame.mouse.get_pos()
				self._check_start_button(start_pos)
				self._check_quit_button(quit_pos)
			elif event.type == pygame.MOUSEMOTION:
				self._check_mouse_motion(event.pos)

	def _check_start_button(self, start_pos):
		"""显示开始按钮被点击后的动画以及游戏的开始"""
		if self.showing_start and self.button.start_rect.collidepoint(start_pos):
			self.button.move_start()  #移动Start图像,模拟按钮效果
			self.start_game()
			self.shrinking = True  # 开始擦除边框

	def _check_quit_button(self, quit_pos):
		"""关闭按钮被点击后，游戏关闭"""
		if self.button.quit_rect.collidepoint(quit_pos) and self.stats.game_active == False:
			sys.exit()

	def _check_keydown_events(self, event):
		"""响应按键"""
		if event.key == pygame.K_q:
			sys.exit()
		elif event.key == pygame.K_RIGHT:
			self.player.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.player.moving_left = True
		elif event.key == pygame.K_SPACE:
			self.player.jump()

	def _check_keyup_events(self, event):
		"""响应键盘松开事件"""
		if event.key == pygame.K_RIGHT:
			self.player.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.player.moving_left = False

	def _check_mouse_motion(self, mouse_pos):
		"""检查鼠标移动"""
		if self.button.start_rect.collidepoint(mouse_pos):
			self.button.show_start_triangle()
		else:
			self.button.hide_start_triangle()

		if self.button.quit_rect.collidepoint(mouse_pos):
			self.button.show_quit_triangle()
		else:
			self.button.hide_quit_triangle()

	def _update_screen(self):
		"""更新屏幕图像"""
		#绘制屏幕
		self.screen.fill(self.settings.bg_color)

		#全局粒子特效
		self.show_shrinking()

		#标题场景动画
		self.show_title_scene()

		#绘制关卡一图像，剪影以及场景
		self.show_step_1_scene()

		#更新绘制玩家以及其特效
		self.show_player_effects()
		self.show_moonjeongho()
		
		#可见
		pygame.display.flip()

	def _gradient_step_color(self):
		"""管理关卡显示图像的渐变"""

		#计算alpha值，实现渐变效果(两秒渐入，两秒淡出)
		current_time = time.time()
		elapsed_time = current_time - self.start_time

		if self.fading_in:
			if elapsed_time < self.duration:
				self.alpha = int((elapsed_time / self.duration) * 255)
			else:
				self.fading_in = False
				self.start_time = current_time #重置计时器
		else:
			if elapsed_time < self.duration:
				self.alpha = 255 - int((elapsed_time / self.duration) * 255)
			else:
				self.alpha == 0
				self.showing_step_1 = False

	def _gradient_start_color(self):
		"""管理开始按钮的渐变"""

		#计算alpha值，实现渐变效果
		current_time = time.time()
		elapsed_time = current_time - self.start_time

		if self.fading_in:
			if elapsed_time < self.duration:
				self.alpha = int((elapsed_time / self.duration) * 255)
			else:
				self.fading_in = False
				self.start_time = current_time #重置计时器

		elif self.alpha_start:
			if elapsed_time < self.duration:
				self.alpha = 255 - int((elapsed_time / self.duration) * 255)
			else:
				self.alpha == 0

	def play_start_menu_music(self):
		"""播放开始界面的背景音乐"""
		self.bgm.play("不思議の国.wav")  #播放开始界面的背景音乐

	def close_start_menu_music(self):
		"""淡出开始界面的背景音乐"""
		self.bgm.fadeout(2000)  #在2秒内淡出背景音乐

	def start_game(self):
		"""处理点击Start按钮后游戏的开始"""
		self.close_start_menu_music()  #调用音乐淡出
		self.stats.game_active = True
		self.stats.step_1_active = True
		self.showing_start = False
		self.start_waiting = True
		self.fading_in = False
		self.alpha_start = True
		self.start_time = time.time()  #重置计时器

	def show_step_1_scene(self):
		"""处理关卡一场景，图像以及其剪影的出现"""
		if self.showing_step_1:
			self._gradient_step_color()
			self.button.draw_step_1(self.alpha)
		if self.stats.step_1_active:
			self.step_1_scene.update(self.player.rect)
			self.step_1_scene.draw_step_1_floor()
			self.step_1_scene.draw_saw()

	def show_shrinking(self):
		"""处理全局粒子特效"""
		# 渲染粒子特效
		if self.shrinking:
			self.shrink_factor += 1
			if self.shrink_factor >= 10:
				self.shrinking = False  # 完成缩小边框过程
		self.title_scene.render(self.shrink_factor)

	def show_title_scene(self):
		"""处理标题界面的动画活动"""
		#如果游戏没有正式开始，绘制开始以及退出按钮,标题
		if self.showing_start:
			self._gradient_start_color()
			self.button.draw_start(self.alpha)
			self.button.draw_quit(self.alpha)
			self.button.draw_title(self.alpha)
		if self.start_waiting:
			#关闭三角形显示
			self.button.hide_start_triangle()
			self.button.hide_quit_triangle()
			# 等待 start 按钮完全淡出
			if self.alpha == 1 or self.alpha == 2 or self.alpha == 3:
				self.timer += 1
				if self.timer == 100:
					self.start_waiting = False
					self.showing_step_1 = True
					self.fading_in = True
					self.start_time = time.time()  #重置计时器
					self.timer = 0
			else:
				self._gradient_start_color()
				self.button.draw_start(self.alpha)
				self.button.draw_quit(self.alpha)
				self.button.draw_title(self.alpha)

	def show_moonjeongho(self):
		"""管理玩家活动以及绘制"""
		if not self.stats.game_active:
			self.player._update_title_scene()
		if self.stats.step_1_active:
			self.player._update_step_1_scene(self.step_1_scene)
		if not self.player.dead:
			self.player.blitme()

	def show_player_effects(self):
		"""管理玩家特效的绘制"""
		if self.player.moving_right:
			self.player_effects.add_trail(self.player.rect, (255, 255, 255), "left")  # 右边拖尾特效
		if self.player.moving_left:
			self.player_effects.add_trail(self.player.rect, (255, 255, 255), "right")  # 左边拖尾特效
		if self.player.jump_speed > 0 and self.player.jump_sign:
			self.player_effects.add_jump_effect(self.player.rect, (255, 255, 255))  # 底部跳跃特效
		if self.player.dead:
			self.player_effects.add_explosion_effect(self.player.rect, (0, 0, 0))  # 添加爆裂特效
			self.player_effects.explosion_start_time += 1
		if self.player_effects.update():
			self.player.dead = False  # 玩家重新聚合完成，复活
			self.player_effects.explosion_start_time = 0
		self.player_effects.draw()


if  __name__ == '__main__':
	#创建实例运行
	indr = InescapableDream()
	indr.run_game()