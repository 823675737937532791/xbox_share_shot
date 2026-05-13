# Xbox Share Shot

一个尽量轻量的 macOS 主屏截图方案。

这版仓库默认推荐的用法是：

`手柄 Share 键 -> 手柄映射软件发出快捷键 -> macOS 快捷指令 -> 运行截图脚本`

这样不需要你每次重新启动一个常驻监听脚本，也更接近系统级工作流。

## 推荐方案

默认目标：

- 只截主屏
- 保存到 `~/Pictures/GameScreenshots`
- 文件名前缀：`XboxScreenshot`

核心脚本是：

- `main_screen_screenshot.sh`

它做的事情很简单：

1. 创建 `~/Pictures/GameScreenshots`
2. 调用 macOS 自带的 `screencapture`
3. 只截 `display_index = 1`
4. 按时间戳保存 PNG

## 最终效果

推荐链路是：

`Share 键 -> 映射软件 -> Control + Option + Command + S -> 快捷指令 -> main_screen_screenshot.sh`

你只需要在手柄映射软件里把 Share 键映射成一个冷门组合键，然后让 macOS 快捷指令绑定同一个快捷键。

## 快速开始

### 1. 给脚本执行权限

```bash
chmod +x main_screen_screenshot.sh
```

### 2. 手动测试脚本

```bash
zsh "./main_screen_screenshot.sh"
```

成功后，截图会出现在：

```text
~/Pictures/GameScreenshots
```

### 3. 配置快捷指令

详细步骤见：

- `SHORTCUT_SETUP.md`

你需要在「快捷指令」App 里新建一个快捷指令，比如：

- 名字：`主屏截图`
- 动作：`运行 Shell 脚本`
- 内容：

```bash
zsh "/Users/lantianxing/Documents/Playground/main_screen_screenshot.sh"
```

然后给它分配快捷键，例如：

```text
Control + Option + Command + S
```

最后在你的手柄映射软件里，把 Share 键映射成同一个快捷键即可。

## 为什么现在主推快捷指令

- 不依赖前台常驻监听器
- 不怕手柄断开再连后脚本状态乱掉
- 逻辑更简单
- 更适合长期日常使用

## 项目文件

```text
.
├── SHORTCUT_SETUP.md
├── config.example.ini
├── install.sh
├── main_screen_screenshot.sh
├── README.md
├── requirements.txt
├── take_screenshot.py
└── xbox_share_shot.py
```

## install.sh 现在做什么

安装脚本现在只负责：

1. 创建默认配置目录
2. 复制 `config.example.ini`
3. 确保 `main_screen_screenshot.sh` 可执行
4. 在 `~/Applications` 放一个便于手动测试的启动器

它不会再默认帮你生成旧的监听模式启动器。

## 旧监听模式

仓库里仍然保留：

- `xbox_share_shot.py`
- `take_screenshot.py`

这是之前的“Python 监听手柄按钮 -> 调用截图 helper”方案，主要作为兼容和参考保留。

如果你就是想自己跑监听器，它依然能用；但对当前需求来说，不再是首选方案。

## 旧监听模式配置

配置文件示例在：

- `config.example.ini`

当前默认值：

```ini
[mapper]
button_index = 15
debounce_seconds = 0.7

[screenshot]
save_dir = ~/Pictures/GameScreenshots
filename_prefix = XboxScreenshot
display_index = 1
```

## 已知限制

目前可调用工具可以帮你准备脚本、配置、文档和仓库内容，但不能可靠地替你在「快捷指令」App 里自动创建快捷指令并分配键盘快捷键。

所以这一步仍然需要你在图形界面里手动做一次。

做完后，日常就不需要再碰这套配置了。

## License

MIT
