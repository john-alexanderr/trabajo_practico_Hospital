import os

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BLUE = "\033[94m"


def color(text: str, *codes: str) -> str:
    return "".join(codes) + text + RESET


def clean_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def print_title(text: str) -> None:
    width = 48
    print()
    print(color("╔" + "═" * (width - 2) + "╗", CYAN, BOLD))
    print(color(f"║ {text:^{width-4}} ║", CYAN, BOLD))
    print(color("╚" + "═" * (width - 2) + "╝", CYAN, BOLD))
    print()


def print_subtitle(text: str) -> None:
    print()
    print(color(f"─── {text} ───", YELLOW, BOLD))
    print()


def print_ok(msg: str) -> None:
    print(color(f"  ✓ {msg}", GREEN))


def print_fail(msg: str) -> None:
    print(color(f"  ✗ {msg}", RED))


def print_warn(msg: str) -> None:
    print(color(f"  ⚠ {msg}", YELLOW))


def print_info(msg: str) -> None:
    print(color(f"  ℹ {msg}", BLUE))


def print_sep() -> None:
    print(color("  " + "─" * 46, DIM))


def print_table(data: list[dict]) -> None:
    if not data:
        print_warn("No hay registros para mostrar.")
        return

    keys = list(data[0].keys())
    headers = [k.replace("_", " ").title() for k in keys]

    col_widths = [len(h) for h in headers]
    for row in data:
        for i, k in enumerate(keys):
            val_len = len(str(row.get(k, "")))
            if val_len > col_widths[i]:
                col_widths[i] = val_len

    col_widths = [min(w, 40) for w in col_widths]

    sep = "  ╠" + "╤".join("═" * (w + 2) for w in col_widths) + "╣"
    top = "  ╔" + "╤".join("═" * (w + 2) for w in col_widths) + "╗"
    bot = "  ╚" + "╧".join("═" * (w + 2) for w in col_widths) + "╝"

    print(color(top, CYAN))
    header_row = "  ║ " + " │ ".join(f"{h:<{col_widths[i]}}" for i, h in enumerate(headers)) + " ║"
    print(color(header_row, CYAN, BOLD))
    print(color(sep, CYAN))

    for row in data:
        vals = [str(row.get(k, ""))[:col_widths[i]] for i, k in enumerate(keys)]
        line = "  ║ " + " │ ".join(f"{v:<{col_widths[i]}}" for i, v in enumerate(vals)) + " ║"
        print(line)

    print(color(bot, CYAN))
    print_info(f"Total: {len(data)} registro(s)")
