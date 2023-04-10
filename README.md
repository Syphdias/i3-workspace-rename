## About
This script renames the focused i3 workspace. It can change the color and number
of the workspace as well. It is best used in conjunction with `rofi` to call it
interactively – examples below.

- Documentation (and FAQ – if any) can be found in this README.
- There is currently no package to install the script.
  You need to download it from [here](
  https://raw.githubusercontent.com/Syphdias/i3-workspace-rename/main/i3-workspace-rename.py)
  or clone the repository.
- Feel free to file issues to report bugs, ask questions,
  or request features.
- Feel free to open a pull request. Please use the [black](
  https://github.com/psf/black) code formatter.


## Motivation
It was inspired by two other projects:
- [i3-rename-workspace] from [infokiller/i3-workspace-groups]
- [wsmgr]

Both were not quite what I was looking for but you should check out both to see
if they fit your needs better than this does.

I wanted the tool to
- easily rename a workspace
- change workspace index
- highlight name in a color


## Requirements
```sh
pip install --user -r requirements.txt
```
It is specifically useful together with `rofi`.


## Usage
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

## Examples with `rofi`

### Simple example with `rofi`
```
rofi -show rename -modi 'rename:~/bin/i3-workspace-rename.py'
```

### More complex example as i3 shortcut
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
