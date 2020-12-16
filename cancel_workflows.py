import os
import sys

from github import Github

workflow_lookup_cache = {}
workflow_name = os.environ['GITHUB_WORKFLOW']
event_name = os.environ['GITHUB_EVENT_NAME']
if event_name in ('pull_request_target', 'pull_request'):
    branch_name = os.environ['GITHUB_HEAD_REF']
else:
    gh_ref = os.environ['GITHUB_REF']
    branch_name = gh_ref.replace('refs/heads/', '')
repo_name = os.environ['GITHUB_REPOSITORY']
g = Github(os.environ.get('GITHUB_TOKEN'))
repo = g.get_repo(repo_name)
workflows_running = repo.get_workflow_runs(branch=branch_name,
                                           status='in_progress')
workflows_queued = repo.get_workflow_runs(branch=branch_name, status='queued')

latest_timestamp = None
workflows_list = [workflows_queued, workflows_running]

for wlist in workflows_list:
    for wf in wlist:
        wid = wf.workflow_id
        if wid in workflow_lookup_cache:
            wname = workflow_lookup_cache[wid]
        else:
            wname = repo.get_workflow(str(wid)).name
            workflow_lookup_cache[wid] = wname
        if wname != workflow_name:
            continue
        if latest_timestamp is None:
            latest_timestamp = wf.created_at
        elif wf.created_at > latest_timestamp:
            latest_timestamp = wf.created_at

if latest_timestamp is None:
    print(f'No duplicate workflows for {workflow_name} workflow for '
          f'{branch_name} branch in {repo_name}\n\n'
          f'lookup: {workflow_lookup_cache}')
    sys.exit(0)

for wlist in workflows_list:
    for wf in wlist:
        if wf.created_at < latest_timestamp:
            print(f'Cancelling {wf.status} {wf}')
            wf.cancel()

print(f'Done checking for duplicate workflows for {workflow_name} for '
      f'{branch_name} branch in {repo_name}')
