# Shortcut Setup

如果你想把这套方案变成：

`手柄 Share 键 -> 手柄映射软件发出快捷键 -> 快捷指令执行 -> 只截主屏`

那就按下面这套配。

## 推荐目标

- 只截主屏
- 保存到 `~/Pictures/GameScreenshots`
- 不依赖常驻 Python 监听器

## 方式一：直接把下面脚本贴进快捷指令

在 Mac 的「快捷指令」App 里：

1. 新建一个快捷指令
2. 名字建议：`主屏截图`
3. 添加动作：`运行 Shell 脚本`
4. 脚本内容填下面这段：

```bash
mkdir -p "$HOME/Pictures/GameScreenshots"
/usr/sbin/screencapture -x -D 1 "$HOME/Pictures/GameScreenshots/XboxScreenshot_$(date +%Y-%m-%d_%H-%M-%S).png"
```

5. 给这个快捷指令分配一个键盘快捷键  
推荐：`Control + Option + Command + S`

然后在你的手柄映射软件里，把 `Share` 键映射成：

`Control + Option + Command + S`

## 方式二：复用仓库里的脚本

如果你不想把脚本正文直接贴进快捷指令，也可以在快捷指令里改成：

```bash
zsh "/Users/lantianxing/Documents/Playground/main_screen_screenshot.sh"
```

这样快捷指令只负责调用仓库里的脚本。

## 为什么更推荐快捷指令方案

- 不需要额外常驻监听器
- 更接近系统级使用方式
- 你已经有手柄映射软件，可以直接把组合键发给 macOS

## 你还需要手动做的一步

目前用可调用工具无法直接“创建快捷指令并绑定键盘快捷键”，所以这一步必须在快捷指令 App 里手动完成一次。

完成以后，平时你只需要：

`Share 键 -> 快捷键 -> 快捷指令 -> 主屏截图`
