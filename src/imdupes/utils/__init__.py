from tqdm import tqdm


def loop_errprint(
        msg: str,
        pbar: tqdm = None
) -> None:
    if pbar is not None:
        pbar.write(msg)
    else:
        print(msg, flush=True)
