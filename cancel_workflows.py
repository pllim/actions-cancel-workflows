import os
import sys

from github import Github

gh_ref = os.environ['GITHUB_REF']
branch_name = gh_ref.replace('refs/heads/', '')
repo_name = os.environ['GITHUB_REPOSITORY']
g = Github(os.environ.get('GITHUB_TOKEN'))
repo = g.get_repo(repo_name)
workflows_running = repo.get_workflow_runs(branch=branch_name,
                                           status='in_progress')
workflows_queued = repo.get_workflow_runs(branch=branch_name, status='queued')

latest_timestamp = None

for wf in workflows_queued:
    if latest_timestamp is None:
        latest_timestamp = wf.created_at
    elif wf.created_at > latest_timestamp:
        latest_timestamp = wf.created_at

for wf in workflows_running:
    if latest_timestamp is None:
        latest_timestamp = wf.created_at
    elif wf.created_at > latest_timestamp:
        latest_timestamp = wf.created_at

if latest_timestamp is None:
    print(f'No duplicate workflows for {gh_ref} in {repo_name}')
    sys.exit(0)

for wf in workflows_running:
    if wf.created_at < latest_timestamp:
        print(f'Cancelling in-progress {wf}')
        wf.cancel()

for wf in workflows_queued:
    if wf.created_at < latest_timestamp:
        print(f'Cancelling queued {wf}')
        wf.cancel()

print(f'Done checking for duplicate workflows for {gh_ref} in {repo_name}')
