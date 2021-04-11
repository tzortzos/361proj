# TA Scheduler

CS 361  
Spring 2021  
Group 4

- Chris Wojta
- Isaiah Holt
- Jacob Tzortzos
- Josiah Hilden
- Nathan Leverence

## Contributing

### Getting started

1. Pull repository into pycharm
2. Add venv
	- Go to `File > Settings > Project > Python Interpreter`
	- Click on the gear and then add
	- Create the new directory next to the project directory
3. Add configuration
	- Go to drop down just to the left of the run button
	- Click `Edit Configurations`
	- Click Add and select `Django Server`
	- Add the following to the end of the env section:  
	  `,DJANGO_SETTINGS_MODULE=project.settings`  
	  (Mind the comma, it is there to separate the value from the default one)
	- Click Ok

### Contributing workflow

1. [Create a new branch](#branch-naming-conventions)
3. Set up virtual environment
4. Make changes & [Commit](#commit-expectations)
5. Test to make sure your code is up to standards
6. [Submit a pull request](#pull-request-expectations)

### Branch Naming Conventions

The naming convention of a branch depends on what kind of change you are making.
If you are attempting to add a new feature the format should be (in all lowercase):
`< first name >_feature_< snake case feature name >`, whereas for a bugfix you
would do `< first name >_bugfix_< snake case bug name >`. It is important that
you include as much information as possible in these so that the team can tell at
a glance what is being worked on.

### Commit Expectations

A commit serves three functions: keeping track of changes over time in a growing
codebase, reminding you of what parts you have already completed, and giving
others a quick overview of what you are working on.  
To these ends each commit message should have two parts:

1. A Short but Descriptive Title  
   Should contain a summary of what you changed in that commit
2. A longer (often in list format) description which enumerates individual
   conceptual changes made  
   These will often also contain a short description of the work that you still
   need to do to drive whatever you are working on to completion, though that may
   also (and probably should) be documented somewhere more readily available to you.

These commit messages are in [markdown](https://www.markdownguide.org/cheat-sheet)
format. For example:

```markdown
Added new `create_user` post request method to `AdminUserPanel`

- Created method for request in AdminUserPanel
    - Returns blank page with "Done" on it as of right now
- Added route to AdminRouter
- Next I need to begin implementing the actual request handle
```

That last line may seem obvious by the first, but there is still value in laying
you what you intend to do next explicitly, both for yourself and others. It is not
hard to forget what you were working on.

### Pull Request Expectations

A pull request should have at least three things before it is considered ready
for review.

1. A descriptive title  
   A person with no idea what task you were working on before should at least have
   an idea as to what you did.
2. A link to the trello card for the **single** task that your pull reflects
3. A descriptive body  
   The body should contain a high level overview of the individual changes you
   made, what parts of the application you changed, etc.  
   This may be in list form.

You may also wish to include links to related pull requests, issues, or branches which
may affect your changes.

A relatively simple example of the general principle can be seen in the pull
[Charter/13](https://github.com/cs361-spring2021-team4/Charter/pull/13).

When a pull request is merged make sure to delete the branch so that we do not
end up with a bunch of stale branches in the repo. The option will present itself
once the pull is merged.
