# git 操作入门

## 准备

假设你已经 clone 了当前仓库，并且你的终端位置已经位于仓库目录中。

## 查询状态

查询状态常用的命令有 `git status` 和 `git branch`。

前者用于查询更改文件情况，后者用于展示所有分支。

```text
chatbot-system$ git status
On branch develop
Your branch is up to date with 'origin/develop'.

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        doc/

nothing added to commit but untracked files present (use "git add" to track)
```

```text
chatbot-system$ git branch
* develop
  lhy_dev
  main
  master
```

这里星号表示你当前所在的分支。

## 写代码之前

```bash
# 首先安装 pre-commit
pip install pre-commit          # 安装 pre-commit 用于检查提交
pre-commit install              # 将 pre-commit 挂载到 git 操作

git pull                        # 更新代码，始终基于最新版本进行开发
```

假设你现在已经在 `develop` 分支了，如果不在，请执行 `git checkout develop`。

然后，你需要创建你自己的分支，进行代码开发。

```bash
git checkout -b demo_dev        # 请自行把 demo 换成你的标识符，表示基于当前分支创建分支 demo_dev 并且切换到新分支上
```

## 写代码之后

你这时候已经写完了代码，你需要进行如下操作。

```bash
git add <file>                  # 添加 <file>，表示准备提交这个文件，如果 <file> 是个目录，表示准备（递归地）提交这个目录下的所有文件
git commit -m <commit-message>  # 提交，<commit-message> 需要是字符串，如 "add function"，用来给你本次的提交进行备注
```

通常来说，`git commit` 可能会失败，因为 `pre-commit` 的检查。

但是因为 `pre-commit` 会尽力去自动修复代码问题，因此这时候你应该尝试重复前面的 `add` 和 `commit` 步骤。

## 提交到远程

如果远程没有你的分支，你一般需要

```bash
git push -u origin demo_dev
```

这样就能提交，如果已经有了你的分支，你通常只需要 `git push` 即可。

（如果提示你远程存在冲突，那么请额外加上 `-f` 参数）

## 开始下一轮开发

如果你的提交已经通过 `Merge Request` 进入了 `develop` 分支，一般需要你更新 develop 分支，并重新创建你自己的分支，当然你也可以使用 `rebase`。

假设你目前处于 `develop` 分支。

删除原分支并重新创建

```bash
git pull
git branch -D demo_dev
git checkout -b demo_dev
```

使用 rebase 来解决

```bash
git pull
git checkout demo_dev
git rebase develop
```

## 其他问题

遇到其他问题可以咨询我，其中有意义的问题将加入开发文档中。
