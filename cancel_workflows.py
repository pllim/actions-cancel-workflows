import os

from github import Github

gh_ref = os.environ['GITHUB_REF']
repo_name = os.environ['GITHUB_REPOSITORY']
g = Github(os.environ.get('GITHUB_TOKEN'))
repo = g.get_repo(repo_name)
workflows = repo.get_workflow_runs(branch=gh_ref)

for wf in workflows:
    if wf.status != 'completed':
        print(f'Cancelling {wf}')
        wf.cancel()

print(f'Done checking for duplicate workflows for {gh_ref} in {repo_name}')
