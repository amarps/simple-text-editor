# Amar Panji Senjaya
from tkinter import *
import tkinter.filedialog
import tkinter.messagebox as msg

class main(Tk):

	def __init__(self, *args, **kwargs):
		Tk.__init__(self, *args,**kwargs)
		self.text = Text(self, undo=True)
		self.menubar = Menu(self)
		Tk.config(self,menu=self.menu())
		self.shortcut_bar()
		self.show_line_number = IntVar()
		self.show_line_number.set(1)
		self.line_numbers_bar = Text(width=4,padx=3, takefocus=0, border=0,background='green', state='disabled', wrap='none')
		self.line_numbers_bar.pack(side='left', fill='y')
		self.on_content_changed()		

		self.content_text()
		self.inputBinding()

	def menu(self):
		file_menu = Menu(self.menubar, tearoff=0)
		edit_menu = Menu(self.menubar, tearoff=0)
		view_menu = Menu(self.menubar, tearoff=0)
		about_menu = Menu(self.menubar, tearoff=0)
		list_menu = ['File','Edit','View','About'],[file_menu,edit_menu,view_menu,about_menu]
		list_file = ['Baru','Buka','Simpan','Simpan Sebagai'], ['maju','mundur', 'ambil','salin','taro','cari'],\
					['Layout','Perbesar','perkecil','pengaturan'],['tentang','tolong']
		list_fungsi = [self.maju,self.mundur, self.ambil,self.salin,self.taro,self.cari],[self.baru,self.buka, self.simpan,self.simpanSebagai],\
					[self.maju,self.mundur, self.ambil,self.salin,self.taro],[self.maju,self.mundur, self.ambil,self.salin,self.taro]
		for i in range (0,6):
			edit_menu.add_command(label=list_file[1][i], command=list_fungsi[0][i])
			if i <=3:
				self.menubar.add_cascade(label=list_menu[0][i], menu=list_menu[1][i])
				file_menu.add_command(label=list_file[0][i], command=list_fungsi[1][i])
				view_menu.add_command(label=list_file[2][i], command=list_fungsi[2][i])
			if i <= 1:
				about_menu.add_command(label=list_file[3][i], command=list_fungsi[3][i])

		return self.menubar
	def inputBinding(self):
		sc = ['f','z','Shift-z','v','c','x','s','o','Shift-s']
		ss = [self.cari, self.mundur,self.maju,self.taro,self.salin,self.ambil,self.simpan,self.buka,self.simpanSebagai,self.baru]
		for i in range(len(sc)):
			self.text.bind('<Control-'+sc[i]+'>', ss[i])
			self.text.bind('<Control-'+sc[i].title()+'>', ss[i])
		self.text.bind('<Any-KeyPress>', self.on_content_changed)
		
	def content_text(self):
		scrollbar = Scrollbar(self.text)
		self.text.pack(expand='yes', fill='both')
		self.text.configure(yscrollcommand=scrollbar.set)
		scrollbar.config(command=self.text.yview)
		scrollbar.pack(side='right', fill='y')

	def buka(self,event=None):
		input_file_name = tkinter.filedialog.askopenfilename(defaultextension=".txt",
			filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
		if input_file_name:
			global file_name
			file_name = input_file_name
			self.text.delete(1.0, END)
			with open(file_name) as _file:
				self.text.insert(1.0, _file.read())

	def simpan(self,event=None):
		global file_name
		if not file_name:
			self.simpanSebagai()
		else:
			baru(file_name)	
		return "break"

	def simpanSebagai(self,event=None):
		input_file_name = tkinter.filedialog.asksaveasfilename( 
			defaultextension=".txt", filetypes=[("All Files", "*.*"),
			("Text Documents", "*.txt")])
		if input_file_name:
			global file_name
			file_name = input_file_name
			baru(file_name)
		return "break"

	def baru(file_name,event=None):
		try :
			content = self.text.get(1.0, 'end')
			with open(file_name, 'w') as the_file:
				the_file.write(content)	
		except IOError:
			pass

	def shortcut_bar(self):
		b = Frame(self, height=25, background='blue')
		b.pack(fill='x')

	def cari(self, event=None):
		search_toplevel = Toplevel(self)
		search_toplevel.title('Find Text')
		search_toplevel.transient(self)
		search_toplevel.resizable(False, False)
		Label (search_toplevel, text="Find All :").grid(row=0, column=0, sticky='e')
		search_entry_widget = Entry(search_toplevel, width=25)
		search_entry_widget.grid(row=0,column=1,padx=2,pady=2 , sticky='we')
		search_entry_widget.focus_set()
		ignore_case_value = IntVar()
		Checkbutton(search_toplevel,text='Ignore Case', variable=ignore_case_value).grid(row=1, column=1, sticky='e',padx=2, pady=2)
		Button(search_toplevel, text="Find All", underline=0, command=lambda: self.search_output(search_entry_widget.get(),ignore_case_value.get(),self.text, search_toplevel,search_entry_widget)).grid(row=0, column=2, sticky='e' + 'w', padx=2, pady=2)

	def search_output(self,needle, if_ignore_case, content_text, search_toplevel, search_box):
		content_text.tag_remove('match', '1.0', END)
		matches_found = 0
		if needle:
			start_pos = '1.0'
			while True:
				start_pos = content_text.search(needle,start_pos, nocase=if_ignore_case, stopindex=END)
				if not start_pos:
					break
				end_pos = '{}+{}c'.format(start_pos, len(needle))
				content_text.tag_add('match', start_pos, end_pos)
				matches_found += 1
				start_pos = end_pos
			content_text.tag_config(
				'match', foreground='red', background='yellow')
		search_box.focus_set()
		search_toplevel.title('{} matches found'.format(matches_found))

	def get_line_number(self):
		output = ''
		if self.show_line_number.get():
			row, col = self.text.index("end").split('.')
			for i in range(1, int(row)):
				output += str(i)+'\n'
		return output
		
	def update_line_numbers(self):
		line_numbers = self.get_line_number()
		self.line_numbers_bar.config(state='normal')
		self.line_numbers_bar.delete('1.0', 'end')
		self.line_numbers_bar.insert('1.0', line_numbers)
		self.line_numbers_bar.config(state='disabled')

	def highlight_line(interval=100):
		self.text.tag_remove("active_line",1.0, "end")
		self.text.tag_add("active_line", "inster linestart", "insert lineend+1c")
		self.text.tag_after(interval, toggle_highlight)

	def undo_hightlight():
		self.text.tag_remove("active_line", 1.0, "end")

	def ambil(self,event=None):
		self.text.event_generate("<<Cut>>")

	def maju(self,event=None):
		self.text.event_generate("<<Redo>>")

	def mundur(self,event=None):
		self.text.event_generate("Undo")

	def salin(self,event=None):
		self.text.event_generate("<<Copy>>")

	def taro(self,event=None):
		self.text.event_generate("<<Paste>>")

	def on_content_changed(self,event=None):
		self.update_line_numbers()

app = main()
app.mainloop()
