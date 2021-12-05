#!/usr/bin/env python3
# feture ideas:
# - save favourites in cache file and print them to be found by rofi
# TODO: write README.md (rofi combi example, requirements i3ipc, mode of
#                        support: best-effort, scratch own itch,
#                        force rename `!rename bla`)
from argparse import ArgumentParser
import re

PANGO_COLOR_NAMES = {
    "aliceblue", "antiquewhite", "aqua", "aquamarine", "azure", "beige",
    "bisque", "black", "blanchedalmond", "blue", "blueviolet", "brown",
    "burlywood", "cadetblue", "chartreuse", "chocolate", "coral",
    "cornflowerblue", "cornsilk", "crimson", "cyan", "darkblue", "darkcyan",
    "darkgoldenrod", "darkgray", "darkgreen", "darkgrey", "darkkhaki",
    "darkmagenta", "darkolivegreen", "darkorange", "darkorchid", "darkred",
    "darksalmon", "darkseagreen", "darkslateblue", "darkslategray",
    "darkslategrey", "darkturquoise", "darkviolet", "deeppink", "deepskyblue",
    "dimgray", "dimgrey", "dodgerblue", "firebrick", "floralwhite",
    "forestgreen", "fuchsia", "gainsboro", "ghostwhite", "gold", "goldenrod",
    "gray", "green", "greenyellow", "grey", "honeydew", "hotpink",
    "indianred", "indigo", "ivory", "khaki", "lavender", "lavenderblush",
    "lawngreen", "lemonchiffon", "lightblue", "lightcoral", "lightcyan",
    "lightgoldenrodyellow", "lightgray", "lightgreen", "lightgrey",
    "lightpink", "lightsalmon", "lightseagreen", "lightskyblue",
    "lightslategray", "lightslategrey", "lightsteelblue", "lightyellow",
    "lime", "limegreen", "linen", "magenta", "maroon", "mediumaquamarine",
    "mediumblue", "mediumorchid", "mediumpurple", "mediumseagreen",
    "mediumslateblue", "mediumspringgreen", "mediumturquoise",
    "mediumvioletred", "midnightblue", "mintcream", "mistyrose", "moccasin",
    "navajowhite", "navy", "oldlace", "olive", "olivedrab", "orange",
    "orangered", "orchid", "palegoldenrod", "palegreen", "paleturquoise",
    "palevioletred", "papayawhip", "peachpuff", "peru", "pink", "plum",
    "powderblue", "purple", "rebeccapurple", "red", "rosybrown", "royalblue",
    "saddlebrown", "salmon", "sandybrown", "seagreen", "seashell", "sienna",
    "silver", "skyblue", "slateblue", "slategray", "slategrey", "snow",
    "springgreen", "steelblue", "tan", "teal", "thistle", "tomato",
    "turquoise", "violet", "wheat", "white", "whitesmoke", "yellow",
    "yellowgreen",
}


def pango_color_string(color):
    """Returns the string if it is a pango color, returns empty string it not

    This also adds a # if there was none before
    """
    # Hi, if you see this and know a better way and perferms the same as
    # `color in PANGO_COLOR_NAMES or re.match("#[0-9a-fA-F]{3,12}$", color)`
    if color in PANGO_COLOR_NAMES:
        return color
    if re.match("#[0-9a-fA-F]{3,12}$", color):
        return color
    if re.match("[0-9a-fA-F]{3,12}$", color):
        # prepend # if it was not given because you cannot use # in rofi args
        return f"#{color}"

    return ""


def parse_string(renamestring, i3):
    rename_elements = renamestring.split(":")

    number = None
    color = None
    name_elements = []
    for i in rename_elements:
        # pick first element that looks like a color
        if not color:
            if pango_color := pango_color_string(i):
                color = pango_color
                continue

        # pick first element that looks like a number
        if not number and i.isnumeric():
            number = i
            continue

        # since i is not a number or color, it must be part of the name
        name_elements.append(i)

    # find current ws number if no new number wanted
    if not number:
        tree = i3.get_tree()
        number = tree.find_focused().workspace().num

    # stitch name back together
    name = ":".join(name_elements)

    return number, color, name


def clean_workspace_name(dirty_name):
    clean_name = dirty_name.replace("\\", "\\\\").replace('"', '\\"')
    return clean_name


def string_for_rename(name, number, color="", prefix="", default_color=""):
    name = clean_workspace_name(name)

    # use default color if no new color wanted
    if not color:
        color = pango_color_string(default_color)

    color_start, color_end = "", ""
    if color:
        color_start = f"<span color='{color}'>"
        color_end = "</span>"

    return f"{number}:{prefix}{color_start}{name}{color_end}"


def rename_workspace(
        i3, name, number, color="", prefix="", default_color="", workspace=""):
    rename_string = string_for_rename(
        name, number, color, prefix, default_color)

    workspace_quote = ""
    workspace_string = ""
    if workspace:
        workspace_quote = "\""

        number_of_workspace = workspace[:workspace.find(":")]
        name_of_workspace = workspace[workspace.find(":")+1:]

        workspace_string = string_for_rename(
            name_of_workspace, number_of_workspace)

    i3.command(
        f'rename workspace '
        f'{workspace_quote}{workspace_string}{workspace_quote} '
        f'to "{rename_string}"')


def main(args):
    if args.renamestring and args.renamestring != args.print_string:
        from i3ipc import Connection
        i3 = Connection()

        number, color, name = parse_string(args.renamestring, i3)

        workspaces = i3.get_workspaces()
        # if other workspace has wanted number, give it the old number
        if (args.swap_workspace and
                int(number) in [ws.num for ws in workspaces]):
            # remote workspace will get number of the current/local workspace
            number_for_remote_workspace = (
                i3.get_tree().find_focused().workspace().num)

            full_workspace_name = (
                [ws for ws in workspaces if ws.num == int(number)][0].name)
            name_for_remote_workspace = (
                full_workspace_name[full_workspace_name.find(":")+1:])

            rename_workspace(
                i3,
                name_for_remote_workspace,
                number_for_remote_workspace,
                workspace=full_workspace_name)

        rename_workspace(
            i3, name, number, color, args.prefix, args.default_color)
    else:
        print(args.print_string)
        exit(0)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "renamestring", nargs="?",
        help="New name for workspace. Optionally provide color or number "
        "separated by colons, e.g. red:new_name:7 (order does not matter)")
    parser.add_argument(
        "--print-string", default="workspace",
        help="Define what to print if not arguments are given.")
    parser.add_argument(
        "--default-color", default="",
        help="Default color for workspace name if not given in renamestring")
    parser.add_argument(
        "--prefix", default="",
        help="Prefix before workspace name (after number and colon)")
    parser.add_argument(
        "--swap-workspace", default=False, action="store_true",
        help="Swap workspace index with existing workspace if desired number "
        "is already in use")
    # TODO: This might be a new featue to change workspace number to the next
    # unsued number instead of swapping numbers
    # parser.add_argument(
    #     "--unique", default=False, action="store_true")

    args = parser.parse_args()
    main(args)
