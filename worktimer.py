from tkinter import Tk, Label, Button, Text, Frame, Entry
from tkinter import N, E, S, W, END
from tkinter import messagebox
from tkinter.ttk import Notebook

from datetime import date

import os

from timer import *

class WorkTimer:
	def __init__(self, master):
		# initialize the master
		self.master = master
		master.title("SDL Work Timer")

		# timer counter
		self.timers = 0

		# master dictionary
		# this will contain indexed dictionaries representing instances of
		# the work timer.  Those dictionaries will contain timers so that the clocks remain separate.
		'''
		{
			'notebook1': {
				'masterframe': masterframe, # this is the frame containing the entire timer
				'timer': timerobject, # this is the timer object, holding timer
									  # functions and numbers
				'toggle_button', timer_toggler, # needs to be accessible to alter color
				'date': date_label,
				'hours': hour_label,
				'mins': min_label,
				'secs': second_label,
				'desc': short_text,

				'filename': filename_entry,
				'todo': todo_editor,
				'done': done_editor,
				'notes': notes_editor,
			},
		}
		'''
		self.timer_dict = {}

		self.timerframe = Frame(self.master, padx=10, pady=10)
		self.systemframe = Frame(self.master, padx=10, pady=10)

		self.timer_notebook = Notebook(self.timerframe)

		self.create_timer(self.timer_dict, self.timer_notebook)

		# <> system frame elements <>
		# instantiate system frame elements
		self.new_timer_button = Button(self.systemframe, width=10, text='New timer', command=lambda: self.create_timer(self.timer_dict, self.timer_notebook))
		self.system_label = Label(self.systemframe, text='System:', anchor=W)
		self.system_output = Label(self.systemframe, text='Loading...', anchor=W)
		self.system_copyright = Label(self.systemframe, text='Designed and Developed by Stardust Labs', anchor=E)

		# grid system frame elements

		self.system_label.grid(row=0, column=0, sticky=W)
		self.system_output.grid(row=0, column=1)
		self.new_timer_button.grid(row=0, column=2)
		self.system_copyright.grid(row=1, column=0, columnspan=3, sticky=E)

		# grid master elements
		self.timer_notebook.grid()
		self.timerframe.grid(row=0, column=0)
		self.systemframe.grid(row=1, column=0)

		self.tick()

		self.system_output.config(text='Ready')

	def create_timer(self, timer_dict, notebook):
		# name the timer and instantiate it within the master dictionary
		self.timers += 1
		name = 'notebook' + str(self.timers)
		self.timer_dict[name] = {}
		this_timer = self.timer_dict[name]
		this_timer['id'] = self.timers

		# initialize dictionary abstractions
		this_timer['masterframe'] = Frame(notebook, padx=5, pady=5)
		masterframe = this_timer['masterframe']
		this_timer['timer'] = Timer()

		# frames used to contain timer elements
		timerframe = Frame(masterframe, padx=10, pady=10)
		textframe =  Frame(masterframe, padx=10, pady=10)

		# <> Timerframe Elements <>

		# instantiate timer buttons
		this_timer['toggle_button'] = Button(timerframe, width=9, text="Start", background='#f00', command=lambda: this_timer['timer'].toggle_timer(this_timer))
		timer_reset_button =          Button(timerframe, width=9, text='Reset', command=lambda: this_timer['timer'].reset(this_timer))
		save_timelog_button =         Button(timerframe, width=9, text='Save', command=lambda: self.save_timelog(this_timer))

		# container frame for output, will be inline with other items
		timer_outputframe = Frame(timerframe)

		# instantiate output items
		date_label =          Label(timer_outputframe, text='Date:', anchor=W)
		this_timer['date'] =  Label(timer_outputframe, text=str(this_timer['timer'].output_date))
		hour_label =          Label(timer_outputframe, text='Hour:', anchor=W)
		this_timer['hours'] = Label(timer_outputframe, text=str(this_timer['timer'].output_hour))
		min_label =           Label(timer_outputframe, text='Min:', anchor=W)
		this_timer['mins'] =  Label(timer_outputframe, text=str(this_timer['timer'].output_min))
		sec_label =           Label(timer_outputframe, text='Sec:', anchor=W)
		this_timer['secs'] =  Label(timer_outputframe, text=str(this_timer['timer'].output_sec))

		# grid output items to timer_outputframe so it can be grid later
		date_label.grid         (row=0, column=0, sticky=W)
		hour_label.grid         (row=1, column=0, sticky=W)
		min_label.grid          (row=2, column=0, sticky=W)
		sec_label.grid          (row=3, column=0, sticky=W)
		this_timer['date'].grid (row=0, column=1, sticky=E)
		this_timer['hours'].grid(row=1, column=1, sticky=E)
		this_timer['mins'].grid (row=2, column=1, sticky=E)
		this_timer['secs'].grid (row=3, column=1, sticky=E)

		# instantiate description label and entry
		description_label =  Label(timerframe, text='Desc:', anchor=E)
		this_timer['desc'] = Entry(timerframe)
		def change_tab(event, self=self, tab_id=this_timer['id'] - 1, entry=this_timer['desc']):
			return self.update_tab(event, tab_id, entry)
		this_timer['desc'].bind('<KeyRelease>', change_tab)

		# grid timerframe elements
		this_timer['toggle_button'].grid(row=0, column=0, pady=5)
		timer_reset_button.grid         (row=1, column=0, pady=5)
		save_timelog_button.grid        (row=2, column=0, pady=5)
		timer_outputframe.grid          (row=3, column=0, pady=5)
		description_label.grid          (row=4, column=0, sticky=W)
		this_timer['desc'].grid         (row=5, column=0)

		# <> Textframe Elements <>
		filename_frame =    Frame(textframe)
		text_editor_frame = Notebook(textframe)
		text_system_frame = Frame(textframe)

		# instantiate filename_frame elements
		filename_label =         Label(filename_frame, text='Filename:')
		this_timer['filename'] = Entry(filename_frame, width=50)

		# grid filename_frame elements
		filename_label.grid        (row=0, column=0)
		this_timer['filename'].grid(row=0, column=1)

		# instantiate text editors
		this_timer['todo'] =  Text(text_editor_frame, font=('consolas', '10'), width=75, height=17)
		this_timer['done'] =  Text(text_editor_frame, font=('consolas', '10'), width=75, height=17)
		this_timer['notes'] = Text(text_editor_frame, font=('consolas', '10'), width=75, height=17)

		# grid text editors and add them to the notebook
		this_timer['todo'].grid (padx=5)
		this_timer['done'].grid (padx=5)
		this_timer['notes'].grid(padx=5)
		text_editor_frame.add(this_timer['todo'], text='TODO')
		text_editor_frame.add(this_timer['done'], text='DONE')
		text_editor_frame.add(this_timer['notes'], text='NOTES')

		# instantiate text system elements
		text_save_button = Button(text_system_frame, text='Save Report', command=lambda: self.save_report(this_timer), anchor=E)
		text_load_button = Button(text_system_frame, text='Load Report', command=lambda: self.load_report(this_timer), anchor=E)

		# grid text system elements
		text_save_button.grid(row=0, column=0, padx=5, pady=5, sticky=E)
		text_load_button.grid(row=0, column=1, padx=5, pady=5, sticky=E)

		# instantiate notebook delete button
		timer_delete_button = Button(text_system_frame, text='Delete Timer', command=lambda: self.destroy_timer(this_timer), anchor=E)

		# grid notebook delete button
		timer_delete_button.grid(row=0, column=2, padx=5, pady=5, sticky=E)

		# grid all textframe internal frames
		filename_frame.grid   (row=0, column=0)
		text_editor_frame.grid(row=1, column=0)
		text_system_frame.grid(row=2, column=0)

		# grid submaster frames
		timerframe.grid(row=0, column=0)
		textframe.grid(row=0, column=1)

		# add the timer to the main notebook
		this_timer['masterframe'].grid()
		notebook.add(this_timer['masterframe'], text='New Timer')

	def destroy_timer(self, timer):
		name = timer['desc'].get()
		title = 'Deleting timer {timer_name}'.format(timer_name=name)
		message = 'Are you sure you want to delete {timer_name}?'.format(timer_name=name)
		destroy = messagebox.askquestion(title, message)
		if destroy:
			self.timer_notebook.forget(timer['masterframe'])

	def save_timelog(self, timer):
		self.system_update('Logging {desc} time...'.format(desc=timer['desc'].get()))
		description = timer['desc'].get()

		time = '{date} {h}:{m}:{s} - {desc}\r\n'.format(
			date = timer['timer'].output_date,
			h = timer['timer'].output_hour,
			m = timer['timer'].output_min,
			s = timer['timer'].output_sec,
			desc = description,
		)

		with open('timelog.txt', 'a') as timelog:
			timelog.write(time)

		self.system_update('{desc} time logged.'.format(desc=timer['desc'].get()))

	def save_report(self, timer):
		self.system_update('Saving {desc} report...'.format(desc=timer['desc'].get()))
		todo_header = '---=== TODO ===---\r\n\r\n'
		done_header = '---=== DONE ===---\r\n\r\n'
		notes_header = '---=== NOTES ===---\r\n\r\n'

		todo_body = timer['todo'].get('1.0', END)
		done_body = timer['done'].get('1.0', END)
		notes_body = timer['notes'].get('1.0', END)

		output_text = '{todo_h}{todo}\r\n\r\n{done_h}{done}\r\n\r\n{notes_h}{notes}'.format(
			todo_h = todo_header,
			todo = todo_body,
			done_h = done_header,
			done = done_body,
			notes_h = notes_header,
			notes = notes_body,
		)

		filename = timer['filename'].get()

		with open('reports/' + filename + '.txt', 'w') as report:
			report.write(output_text)

		self.system_update('{desc} report saved.'.format(desc=timer['desc'].get()))

	def load_report(self, timer):
		self.system_update('Loading {file}'.format(file=timer['filename'].get()))

		filename = timer['filename'].get()

		with open(filename + '.txt', 'r') as report:
			input_text = report.read()

			input_text = input_text.split('---=== DONE ===---')
			todo_text = input_text[0]
			input_text = input_text[1].split('---=== NOTES ===---')
			done_text = input_text[0]
			notes_text = input_text[1]

			todo_text = todo_text.replace('---=== TODO ===---', '').replace('\r\n', '')
			done_text = done_text.replace('\r\n', '')
			notes_text = notes_text.replace('\r\n', '')

			timer['todo'].delete('1.0', END)
			timer['todo'].insert(END, todo_text)
			timer['done'].delete('1.0', END)
			timer['done'].insert(END, done_text)
			timer['notes'].delete('1.0', END)
			timer['notes'].insert(END, notes_text)

		self.system_update('{file} loaded.'.format(file=timer['filename'].get()))

	def tick(self):
		for work_timer in self.timer_dict:
			self.timer_dict[work_timer]['timer'].tick(self.timer_dict[work_timer])
		self.systemframe.after(1000, self.tick)

	def update_tab(self, event, tab_id, entry_widget):
		updated_title = entry_widget.get()
		self.timer_notebook.tab(tab_id, text=updated_title)

	def system_update(self, sys_text):
		self.system_output.config(text=sys_text)