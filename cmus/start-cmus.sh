#!/bin/bash
if [ -n "$TMUX" ]; then
    SESSION=$(tmux display-message -p '#S')
else
    echo "错误：未指定 tmux 会话名，且当前不在 tmux 中。"
    usage
fi

# 检查会话是否存在
if ! tmux has-session -t "$SESSION" 2>/dev/null; then
    echo "错误：tmux 会话 '$SESSION' 不存在。"
    exit 1
fi

# 检查窗口中是否存在名为 "cmus" 的窗口
if tmux list-windows -t "$SESSION" -F '#{window_name}' | grep -qx "cmus"; then
    echo "窗口 'cmus' 已存在，切换过去。"
    # 切换到该窗口
    tmux select-window -t "$SESSION":"cmus"
    # 如果不在 tmux 中，则 attach 到会话
    if [ -z "$TMUX" ]; then
        tmux attach-session -t "$SESSION"
    fi
else
    echo "窗口 'cmus' 不存在，创建新窗口。"
    # 创建新窗口，上方 cava，下方 cmus
    tmux new-window -t "$SESSION" -n "cmus" "cava"
    tmux split-window -v -l 60% -t "$SESSION":"cmus" "cmus"
    # 如果不在 tmux 中，则 attach 到会话
    if [ -z "$TMUX" ]; then
        tmux attach-session -t "$SESSION"
    fi
fi
