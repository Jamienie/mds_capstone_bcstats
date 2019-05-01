Contributor Code of Conduct
================

As maintainers of this project we are committed to respecting the ideas and opinions of others and fostering an open and welcoming environment for everyone interested in participating in this project.

We are committed to making participation in this project a harassment-free experience for everyone, regardless of level of experience, gender, gender identity and expression, sexual orientation, disability, personal appearance, body size, race, ethnicity, age, or religion.

Examples of unacceptable behaviour by participants include the use of sexual language or imagery, derogatory comments or personal attacks, trolling, public or private harassment, insults, or other unprofessional conduct.

Project maintainers have the right and responsibility to remove, edit, or reject comments, commits, code, issues, and other contributions that are not aligned to this Code of Conduct. Project maintainers who do not follow the Code of Conduct may be removed from the project team.

Instances of abusive, harassing, or otherwise unacceptable behaviour may be reported by opening an issue.


# Contributing

### How to Contribute
This project will be managed using Git branching. Branches will be task oriented and deleted as soon as the task is completed.

#### How to Create, Push and Delete Branches

1. Clone the master repository to your computer locally `git clone <master_repo_URL>`
2. Create task/feature branch of the master repository on Bash/Terminal `git branch <feature_branch_name>`
3. Link the master and branch `git push -u origin <feature_branch_name>`
4. Switch *head* to the branch `git checkout <feature_branch_name>`
5. Work on the local repository and git add and commit the changes to the repository with `git add <file_name>` and `git commit -m"<commit_message>"`
6. Then push the changes to the repository with `git push`
7. Send a pull request from the branch to master (see Pull Request section for more details on messages, reviews and accepting)
8. Once all work has been completed on the branch, please delete the branch promptly. There are three parts of a branch that need to be deleted.
    -  One team member needs to delete the remote branch. It can either be deleted by hitting the garbage/trash bin button next to the branch name on the GitHub branch tab or in Bash/Terminal with the command `git push origin --delete <feature_branch_name>`
    - Each team member will have to delete their own local branch by `git branch -d <feature_branch_name>`
    - Each team member will have to prune the local remote connection with the command `git remote prune origin`

To check what branches are local `git branch -a`


**Reminder to not push .Rhistory or .ipyn check points**

#### How to Update your Branch

1. When your branch is behind, check which branch you are in, then do `git pull`

2. If you need your branch to match up with the master branch. Checkout the master branch, do a git pull, then checkout your feature branch and do `git merge master`

3. If the files you want aren't there locally, try pushing and pulling from the master and the branch and maybe a git merge and then push and pull again

4. When your are trying to git pull and the error message about upstaged changes occurs. There are two methods that are essentially equivalent
 - `git stash` will "stash" your changes and you can restore with `git stash pop` or remove completely with `git stash drop`.
 - `git reset --hard`



### Communication
To ensure open and transparent communication create an issue in the master repository. When there are task oriented issues, before working on the task add a comment assigning the task to yourself.
If you see a bug or typo either create an issue so the teammate responsible for the file is aware or fix the issue yourself and send a pull request.

For more general communication such as organizing meetings our Slack channel will be used.

### Commit Messages
When adding new files or making changes to existing files, write simple and descriptive commit messages. For readability have:
- one commit message per task
- the title of the file (add the purpose if the title is not a good description)
- the changes in the file is being updated

### Pull Request Messages & Review
Once a pull request has been create assign the other team members as reviewers. For major or critical updates/tasks try to have both other team mates post a review before the pull request is accepted.

Any team member can accept a pull request, ie not just the team member who made the request can accept the pull request.

Smaller administrative tasks like changing folder names or creating a template can be accepted with out other teammates reviews.


### Outside & Future Contributors
This repository has been created for a course project and may not be monitored after the course. If you would like to comment or ask questions about the analysis, post an issue and one of the contributors may respond.




This Code of Conduct is adapted from the [Contributor Covenant](http:contributor-covenant.org), [version 1.0.0](http://contributor-covenant.org/version/1/0/0/).
