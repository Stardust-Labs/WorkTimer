from datetime import date

class Timer:
	def __init__(self):
		# initialize timer variables
		self.timer_on = False

		self.output_date = date.today()
		self.output_hour = 0
		self.output_min  = 0
		self.output_sec  = 0

	def tick(self, master):
		if self.timer_on:
			if self.output_date != date.today():
				self.output_date = date.today()
			self.output_sec += 1
			if self.output_sec >= 60:
				self.output_min += 1
				self.output_sec -= 60
			if self.output_min >= 60:
				self.output_hour += 1
				self.output_min -= 60

			master['date'].config(text=str(self.output_date))
			master['hours'].config(text=str(self.output_hour))
			master['mins'].config(text=str(self.output_min))
			master['secs'].config(text=str(self.output_sec))
			

	def reset(self, master):
		# Turn all things to 0, print to system
		self.output_date = date.today()
		self.output_hour = 0
		self.output_min = 0
		self.output_sec = 0

		master['date'].config(text=str(self.output_date))
		master['hours'].config(text=str(self.output_hour))
		master['mins'].config(text=str(self.output_min))
		master['secs'].config(text=str(self.output_sec))

	def toggle_timer(self, master):
		self.timer_on = not self.timer_on
		if self.timer_on:
			master['toggle_button'].config(text='Stop', background='#0f0')
		else:
			master['toggle_button'].config(text='Start', background='#f00')