#!/usr/bin/env python
import tmuxp, time, sys, readline
def get_tmux_session():
    return tmuxp.Server().list_sessions()[0]
def get_free_window_name(session):
    i = 0
    tmux_window_name = None
    while True:
        tmux_window_name = 'cssh_tmux_' + str(i)
        print(tmux_window_name)
        try:
            window = session.select_window(tmux_window_name)
        except:
            return tmux_window_name
        i += 1

def start_main_shell(tmux_window_name):
    session = get_tmux_session()
    window = session.select_window(tmux_window_name)
    try:
        while True:
            command = raw_input("> ")
            first = True
            for p in window.panes:
                if first:
                    first = False
                else:
                    p.send_keys(command)
    except EOFError, e:
        window.kill_window()

def setup_window(args):
    session = get_tmux_session()
    tmux_window_name = get_free_window_name(session)
    window = session.new_window(window_name = tmux_window_name)
    pane_base_index = int(window.show_window_option('pane-base-index', g=True))
    first_pane = window.attached_pane()
    panes = []
    servers = []
    servers = filter(lambda x: x != "--sorthosts", args)[1:]
    if "--sorthosts" in servers: servers.sort()
    first_pane.set_width(2)
    for i in range(len(servers)):
        pane = window.split_window(attach=(i%2 == 0))
        pane.set_width(2)
        window.select_layout("even-vertical")
        panes.append(pane)
    # we could also use "main-horizontal" layout
    window.select_layout("tiled")
    time.sleep(1)
    first_pane.send_keys(args[0] + " commander " + tmux_window_name)
    i = 0
    for p in panes:
        p.send_keys("ssh " + servers[i]) 
        i += 1
    first_pane.select_pane()

if len(sys.argv) >= 2 and sys.argv[1] == "commander":
    start_main_shell(sys.argv[2])
else:
    setup_window(sys.argv)
