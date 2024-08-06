class GameStats:
	"""跟踪游戏统计信息"""

	def __init__(self, ai_game):
		#初始化统计信息
		self.settings = ai_game.settings

		#游戏处于非活动状态
		self.game_active = False

		#游戏未处于第一关
		self.step_1_active = False