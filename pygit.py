import os.path
import re
from subprocess import check_output


class Git:

	@staticmethod
	def config(name, mail, flag=None):
		if not re.match(r'[^@]+@[^@]+\.[^@]+', mail):
			return "Mail not valid!"
		if not re.match(r'[A-Za-z0-9]+', name) or name == "":
			return "Name not valid!"

		if flag == "global" or flag == "g" or flag == 1:
			check_output(f"git --global config user.name {name}", shell=True)
			check_output(f"git --global config user.email {mail}", shell=True)
		elif flag == "system" or flag == "s" or flag == 2:
			check_output(f"git --system config user.name {name}", shell=True)
			check_output(f"git --system config user.email {mail}", shell=True)
		elif flag is None:
			check_output(f"git config user.name {name}", shell=True)
			check_output(f"git config user.email {mail}", shell=True)
		else:
			return "Flag not valid!"

		return True

	@staticmethod
	def init(folder=None, branch=None):
		if os.path.exists(f"{folder}.git") or os.path.exists(f"{folder}/.git"):
			return "Repository already exists!"
		if not len(os.listdir(folder)) == 0:
			return "Directory not empty!"
		if not re.match(r'[A-Za-z0-9]+', branch) or branch == "":
			return "Branch name not valid!"

		if folder is not None:
			if not os.path.exists(folder):
				try: os.makedirs(folder)
				except OSError: return "Error creating directory!"
			if branch is not None:
				check_output(f"git init --separate-git-dir='{folder}' --initial-branch='{branch}'", shell=True)
			else:
				check_output(f"git init --separate-git-dir='{folder}'", shell=True)
		else:
			cwd = os.getcwd()
			if not len(os.listdir(cwd)) == 0:
				return "Directory not empty!"
			if branch is not None:
				check_output(f"git init --initial-branch='{branch}'", shell=True)
			else:
				check_output(f"git init", shell=True)

		return True

	@staticmethod
	def clone(url, folder):
		if not re.match(r'https://[^@]+\.[^@]+/[^@]+\.git', url):
			return "Invalid repository.git url!"
		if os.path.exists(f"{folder}.git") or os.path.exists(f"{folder}/.git"):
			return "Repository already exists!"
		if not len(os.listdir(folder)) == 0:
			return "Directory not empty!"

		if not os.path.exists(folder):
			try: os.makedirs(folder)
			except OSError: return "Error creating directory!"
		check_output(f"git clone {url} {folder}", shell=True)

		return True

	@staticmethod
	def reset(mode, branch):
		if not re.match(r'[A-Za-z0-9]+', branch) or branch == "":
			return "Branch name not valid!"
		match mode:
			case "soft":
				check_output(f"git reset --soft origin/{branch}", shell=True)
			case "mixed":
				check_output(f"git reset --mixed origin/{branch}", shell=True)
			case "hard":
				check_output(f"git reset --hard origin/{branch}", shell=True)
			case "merge":
				check_output(f"git reset --merge origin/{branch}", shell=True)
			case "keep":
				check_output(f"git reset --keep origin/{branch}", shell=True)
			case _ :
				return "Invalid reset mode!"
		
		return True

	@staticmethod
	def fetch(force=None):
		if force is True:
			check_output(f"git fetch --all", shell=True)
		elif force is None:
			check_output(f"git fetch --all --force", shell=True)
		else:
			return "Invalid force boolean!"
		return True

	@staticmethod
	def checkout(branch):
		if not re.match(r'[A-Za-z0-9]+', branch) or branch == "":
			return "Branch name not valid!"
		check_output(f"git checkout {branch}", shell=True)

		return True

	@staticmethod
	def pull(force=None):
		if force is True:
			check_output(f"git pull --force", shell=True)
		elif force is None:
			check_output(f"git pull", shell=True)
		else:
			return "Invalid force boolean!"
		return True

	@staticmethod
	def push(src, dst, force=None):
		if not re.match(r'[A-Za-z0-9]+', src):
			return "Source branch not valid!"
		if not re.match(r'[A-Za-z0-9]+', dst):
			return "Destination branch not valid!"

		if force is not None and not True and not False:
			return "Invalid force boolean!"
		if force is True:
			check_output(f"git push -f origin {src}:{dst}", shell=True)
		else:
			check_output(f"git push origin {src}:{dst}", shell=True)

		return True

	@staticmethod
	def commit(msg):
		check_output(f"git commit -m '{msg}'", shell=True)
		return True

	@staticmethod
	def latest(url, branch):
		if not re.match(r'https://[^@]+\.[^@]+/[^@]+\.git', url):
			return "Invalid repository.git url!"
		if not re.match(r'[A-Za-z0-9]+', branch) or branch == "":
			return "Branch name not valid!"

		out = check_output(f"git ls-remote {url} refs/heads/{branch}", shell=True)
		if out != '':
			commit = out.decode("utf-8").split("	")[0]
			return commit
		else:
			return "Error getting ref data!"
