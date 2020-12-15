# GitHub Action to cancel duplicate workflows

In the event of quick successive pushes to a branch or a pull request,
this action attempts to cancel all duplicate workflows but the latest one.
You should run this at the beginning of your workflow.
In your CI workflow YAML, add this:

```
jobs:
  cancel_previous:
    name: Cancel previous duplicate workflows
    runs-on: ubuntu-latest
    steps:
    - name: Cancel
      uses: pllim/actions-cancel-workflows@main
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  # Probably wants to wait till older workflows cancelled first.
  # Placeholder for actual CI jobs.
  actual_ci:
    needs: cancel_previous
    ...
```
