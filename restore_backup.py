#!/usr/bin/env python3
import argparse
import os
import urwid

class RestoreBackupGui(urwid.Widget):
	def draw_screen(self):
		if self.loop is not None:
			self.loop.draw_screen()
	def on_backup_selected(self, backup_file, *args, **kwargs):
		self.selected_file = backup_file
		raise urwid.ExitMainLoop()
		

	def __init__(self, ctfd_root:str, backup_dir:str):
		self.selected_file = None
		print("Backup Dir: {}".format(backup_dir))
		print("CTF Root: {}".format(ctfd_root))
		self.backup_dir = backup_dir
		self.ctfd_root = ctfd_root
		body = [urwid.Text("Select backup to restore:")]
		for f in reversed(sorted(os.listdir(self.backup_dir))):
			chk = urwid.CheckBox(f, user_data=f, on_state_change=self.on_backup_selected)
			body.append(urwid.AttrMap(chk, None, focus_map='reversed'))
		list_walker = urwid.SimpleFocusListWalker(contents=body)
		self.loop = urwid.MainLoop(urwid.ListBox(list_walker))

if __name__ == "__main__":
	cfg = argparse.ArgumentParser()
	cfg.add_argument("--backup-dir", type=str, default="~/backups")	
	cfg.add_argument("--ctfd-root", type=str, default="~/CTFd")	
	args = cfg.parse_args()
	gui = RestoreBackupGui(os.path.expanduser(args.ctfd_root), os.path.expanduser(args.backup_dir))
	gui.loop.run()
	selected = gui.selected_file.label
	print("Backup file selected: {}".format(selected))
	database = "{}/CTFd/ctfd.db".format(os.path.expanduser(args.ctfd_root))
	os.remove(database)
	print("Restoring Database")
	command = "sqlite3 {} < {}/{}".format(database, os.path.expanduser(args.backup_dir), selected)
	print(command)
	os.popen(command)
	print("Success")
