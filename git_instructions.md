# git setup instructions

1.) Basic Setup:
- [Download Git](https://git-scm.com/downloads)
- [Setting Username](https://docs.github.com/en/get-started/getting-started-with-git/setting-your-username-in-git)
- [Setting Email](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-user-account/managing-email-preferences/setting-your-commit-email-address)

2.) After getting setup with Git - you are going to want to perform these steps to create a local git instance and track the remote (what you see on the browser) repository:
In command prompt, or git bash, or whatever mac users use; follow these steps:
- create the folder you want to store the project (it should be empty) code in and type `git init`
- go to the [repository web page](https://github.com/jredmond47/fraud_detection_project) and click the "Code" button; next click the clip board icon to copy the repo link
- go back to command prompt and type `git remote add upstream paste_link_here`
  - this will give you the ability to start tracking the remote on your local machine 
  - type `git remote -v` and you will see that adding the remote link created two remotes for you:
      - pushing (for pushing your work up to github) and
      - pulling (for pulling new changes down from github)
- next you can type `git pull upstream master` and that will pull what is in the remote repo down to local
- next create your own branch - this is where you will make your own changes to the code so that we don't conflict with one another's work  
  - type `git checkout -b my_name upstream/master`  

3.) When you make changes to your local branch, and you want them to be reflected in remote, type the following:
- `git add .`
- `git commit -m "commit message explaining changes"`
- `git push upstream my_name`
- this is move what's on your local up to your own branch in remote

4.) If the changes in your personal branch are ready to be merged into the master branch, read [this article](https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) about creating and merging pull requests.

Never push directly to master from your local git instance.

Please reach out if you have any questions.
