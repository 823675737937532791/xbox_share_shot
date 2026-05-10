# Xbox Share Shot

一个尽量轻量的 macOS 小工具。

它会监听 Xbox 手柄上的一个固定按钮，然后调用 macOS 自带的 `screencapture` 把截图保存到你指定的目录。

这个项目最初就是为 Xbox 手柄“分享/截图键”做的，所以默认配置已经按下面这套来：

- 默认按钮编号：`15`
- 默认保存目录：`~/Desktop/游戏截图`
- 默认文件名前缀：`XboxScreenshot`

## 适用场景

- 想把 Xbox 手柄某个按钮映射成截图
- 想要一个非常轻量、依赖少、逻辑简单的方案
- 想自己改保存目录，而不是被系统默认截图目录限制

## 已知前提

- 当前实现依赖 `pygame` 读取手柄按钮
- 截图调用的是 macOS 自带的 `/usr/sbin/screencapture`
- 这套方案在普通图形会话里工作更稳定
- 有些环境里，完全后台化的 `launchd` 方式会不稳定

换句话说，如果你发现“前台运行可以，后台常驻不稳定”，这不是你的配置错了，而是 macOS/云环境权限模型本身比较挑。

## 快速安装

```bash
chmod +x install.sh
./install.sh
```

安装脚本会做几件事：

1. 创建虚拟环境 `.venv`
2. 安装 `pygame`
3. 生成配置文件 `~/.config/xbox-share-shot/config.ini`
4. 生成两个可双击启动的 `.command` 文件到 `~/Applications`

生成的启动器：

- `~/Applications/Xbox Share Shot.command`
- `~/Applications/Detect Xbox Share Button.command`
- `~/Applications/Stop Xbox Share Shot.command`

## 使用方法

### 1. 先检测按钮编号

如果你不是用默认的 Xbox 分享键，先双击：

`~/Applications/Detect Xbox Share Button.command`

然后按一下手柄按钮，终端里会打印类似：

```text
Button index: 15
```

### 2. 修改配置

配置文件路径：

```text
~/.config/xbox-share-shot/config.ini
```

默认内容：

```ini
[mapper]
button_index = 15
debounce_seconds = 0.7

[screenshot]
save_dir = ~/Desktop/游戏截图
filename_prefix = XboxScreenshot
```

可改项：

- `button_index`
- `debounce_seconds`
- `save_dir`
- `filename_prefix`

### 3. 启动监听

双击：

`~/Applications/Xbox Share Shot.command`

保持这个终端窗口开着，然后按你的手柄按钮截图。

### 4. 停止监听

双击：

`~/Applications/Stop Xbox Share Shot.command`

## 命令行用法

```bash
.venv/bin/python3 xbox_share_shot.py --config ~/.config/xbox-share-shot/config.ini
```

检测模式：

```bash
.venv/bin/python3 xbox_share_shot.py --config ~/.config/xbox-share-shot/config.ini --detect
```

临时覆盖按钮编号：

```bash
.venv/bin/python3 xbox_share_shot.py --config ~/.config/xbox-share-shot/config.ini --button-index 15
```

## 项目结构

```text
.
├── config.example.ini
├── install.sh
├── README.md
├── requirements.txt
├── take_screenshot.py
└── xbox_share_shot.py
```

## 为什么拆成两个 Python 文件

这不是为了“架构好看”，而是为了稳定。

在一些环境里，监听手柄的长驻进程自己直接截图会失败；但让监听进程只负责收按钮，再拉起一个短命 helper 去截图，反而更稳。

所以现在的结构是：

1. `xbox_share_shot.py` 负责监听按钮
2. `take_screenshot.py` 负责真正截图

## 后续可以加什么

- 多按钮映射
- 成功提示方式可配置
- 自动开机启动
- 针对不同游戏切换不同保存目录

## 当前建议

如果你已经验证自己的按钮编号固定，而且主要需求只是“随时改保存目录”，那就只改 `config.ini` 里的 `save_dir` 就够了。

这也是这个项目故意保持轻量的原因：

- 不强绑复杂 UI
- 不强绑系统快捷键模拟
- 不把行为做得太重
- 先把“稳定截图”放在第一位

## License

MIT
