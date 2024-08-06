import pygame
import os

class BGM:
	def __init__(self, music_folder):
		"""初始化背景音乐管理"""
		pygame.mixer.init()
		self.music_folder = music_folder
		self.current_track = None

	def play(self, track_name, loops=-1):
		"""播放指定的背景音乐"""
		track_path = os.path.join(self.music_folder, track_name)
		if not os.path.exists(track_path):
			print(f"Track {track_path} not found!")
			return
		pygame.mixer.music.load(track_path)
		pygame.mixer.music.play(loops)
		self.current_track = track_name

	def pause(self):
		"""暂停当前播放的背景音乐"""
		pygame.mixer.music.pause()

	def unpause(self):
		"""继续播放背景音乐"""
		pygame.mixer.music.unpause()

	def stop(self):
		"""停止播放背景音乐"""
		pygame.mixer.music.stop()
		self.current_track = None

	def fadeout(self, time):
		"""淡出背景音乐"""
		pygame.mixer.music.fadeout(time)

	def is_playing(self):
		"""检查是否有音乐正在播放"""
		return pygame.mixer.music.get_busy()