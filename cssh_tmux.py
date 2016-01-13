#!/usr/bin/env python
import tmuxp, time, sys, readline, os, subprocess

def get_tmux_session():
    return tmuxp.Server().attached_sessions()[0]

def start_main_shell():
    session = get_tmux_session()
    window = session.attached_window()
    history_path = os.path.join(os.path.expanduser("~"), ".cssh_tmux.history")
    prompt = subprocess.Popen(["ssh-add", "-l"], stdout=subprocess.PIPE).communicate()[0].split()[-2].split("/")[-1].split(".")[0]
    prompt += "> "
    try:
        readline.read_history_file(history_path)
    except IOError:
        pass
    try:
        while True:
            try:
                command = raw_input(prompt)
            except KeyboardInterrupt:
                None
                print("")
            first = True
            for p in window.panes:
                if first:
                    first = False
                else:
                    if command == None:
                        p.cmd("send-keys", "^C")
                    else:
                        p.send_keys(command)
    except EOFError, e:
        readline.write_history_file(history_path)
        window.kill_window()

def setup_window(args):
    session = get_tmux_session()
    window = session.new_window()
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
    first_pane.send_keys(args[0] + " commander")
    i = 0
    for p in panes:
        p.send_keys("ssh " + servers[i]) 
        i += 1
    first_pane.select_pane()

if len(sys.argv) >= 1 and sys.argv[1] == "commander":
    start_main_shell()
else:
    setup_window(sys.argv)
