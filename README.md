# Status: Archived

Use other workflows out there that are implemented in TypeScript or JavaScript,
as that is much faster due to lack of Docker spin-up overhead. One example
workflow out there is https://github.com/styfle/cancel-workflow-action .

If you must use this, it should still work but there are no plans to
further develop this Action.

# GitHub Action to cancel duplicate workflows

In the event of quick successive pushes to a branch or a pull request,
this action attempts to cancel all older duplicate workflows.
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
