import requests
import sublime
import os
import subprocess

class GitHubAccount:
    def __init__(self):
        self.session = requests.Session()
        self.settings = sublime.load_settings('github_issue.sublime-settings')
        api_token = self.settings.get('token', '')
        self.username = self.settings.get('username', '')
        password = self.settings.get('password', '')
        if api_token:
            self.session.headers['Authorization'] = 'token %s' % api_token
        elif self.username and password:
            self.session.auth = (self.username, password)
        else:
            raise Exception("Please check the authentication settings!")

    def join_issue_url(self, repo_name=None, issue_number=None):
        API_URL = 'https://api.github.com/repos'
        if repo_name:
            if not issue_number:
                return '/'.join([API_URL, self.username, repo_name, 'issues'])
            else:
                return '/'.join([API_URL, self.username, repo_name, 'issues', issue_number])
        else:
            raise Exception("Please check whether the repo_name is correct.")


def get_github_repo_name():
    '''
    Find the repo name. It essentially does two attempts:
    - First it try the open folder's name
    - If the first attempt fails, it tries to run "git config --get remote.origin.url" in current directory
    '''
    current_window = sublime.active_window()
    # open_folders = current_window.folders()
    # repo_name = None
    # if open_folders:
    #     for folder_path in open_folders:
    #         path, folder_name = os.path.split(folder_path)
    #         if self.account['self.username'][folder_name].get()[0] == 200:
    #             repo_name = folder_name
    #             break
    file_name = current_window.active_view().file_name()
    folder = os.path.abspath(os.path.dirname(file_name))
    cmd = ['git', '-C', folder, 'config', '--get', 'remote.origin.url']
    try:
        repo_url = subprocess.check_output(' '.join(cmd), shell=True)
        _, raw_repo_name = os.path.split(repo_url)
        raw_repo_name = raw_repo_name.decode('utf-8')
        raw_repo_name = raw_repo_name.replace("\n", "")
        repo_name = raw_repo_name.replace("\r", "")
    except:
        raise Exception("Error in find repo URL!")
    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]
    return repo_name