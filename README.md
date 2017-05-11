# cssh_tmux

An SSH multiplexer based on tmux (like csshx).

## Video demo

[![Watch the video](https://img.youtube.com/vi/1RUzW5CrIXk/0.jpg)](https://www.youtube.com/watch?v=1RUzW5CrIXk)

## Usage

./cssh_tmux.py host1 host2 ....

## How it works

cssh_tmux creates a new window with ssh clients started for given host in their own pane.
The first pane contain a leader prompt, which will forward its inputs to all the other panes.
