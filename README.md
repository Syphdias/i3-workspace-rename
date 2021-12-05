# Preamble
This was inspired by two other projects:
- [i3-rename-workspace] from [infokiller/i3-workspace-groups]
- [wsmgr]

Both were not quite what I was looking for but you should check out both to see
if they fit your needs better than this does.

# What I wanted the tool to do
- Easily rename a workspace
- Change workspace index
- highlight name in a color

# Requirements
- `rofi`
- `i3ipc`

# Usage
```console
❯ ./i3-workspace-rename.py -h
usage: i3-workspace-rename.py [-h] [--print-string PRINT_STRING]
                              [--default-color DEFAULT_COLOR]
                              [--prefix PREFIX] [--swap-workspace]
                              [renamestring]

positional arguments:
  renamestring          New name for workspace. Optionally provide color or
                        number separated by colons, e.g. red:new_name:7 (order
                        does not matter)

optional arguments:
  -h, --help            show this help message and exit
  --print-string PRINT_STRING
                        Define what to print if not arguments are given.
  --default-color DEFAULT_COLOR
                        Default color for workspace name if not given in
                        renamestring
  --prefix PREFIX       Prefix before workspace name (after number and colon)
  --swap-workspace      Swap workspace index with existing workspace if
                        desired number is already in use
```

# Examples with `rofi`

## Simple example with `rofi`
```
rofi -show rename -modi 'rename:~/bin/i3-workspace-rename.py'
```

## More complex example as i3 shortcut
```
bindsym $mod+Tab exec --no-startup-id \
    LC_ALL=en_US.UTF-8 rofi -i -lines 10 -eh 1 -width 50 -padding 50 -opacity 85 -font 'MesloLGS NF Regular 16' \
    -modi 'combi#rename:~/bin/i3-workspace-rename.py --default-color A9C03F' \
    -show combi \
    -combi-modi 'rename:~/bin/i3-workspace-rename.py --default-color A9C03F#window'
```

[infokiller/i3-workspace-groups]: https://github.com/infokiller/i3-workspace-groups
[i3-rename-workspace]: https://github.com/infokiller/i3-workspace-groups/blob/master/scripts/i3-rename-workspace
[wsmgr]: https://github.com/stapelberg/wsmgr-for-i3
