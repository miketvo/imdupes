from tqdm import tqdm


class UnknownImageFormatError(RuntimeError):
    pass


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return f'{num:3.1f}{unit}{suffix}'
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
