from tqdm import tqdm


class UnknownImageFormatError(RuntimeError):
    pass


def sizeof_fmt(
        num: int,
        suffix: str = 'B',
        sep: str = ' '
) -> str:
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return f'{num:3.1f}{sep}{unit}{suffix}'
        num /= 1024.0
    return f'{num:.1f}Yi{suffix}'


def loop_errprint(
        msg: str,
        pbar: tqdm = None
) -> None:
    if pbar is not None:
        pbar.write(msg)
    else:
        print(msg, flush=True)
