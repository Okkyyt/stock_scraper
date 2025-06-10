import re


def parse_time_period(time_str: str) -> dict:
    match = re.match(r"^(\d+)([smhdw])$", time_str.strip().lower())
    if not match:
        raise ValueError("Invalid time format. Use 'Ns', 'Nm', 'Nh', 'Nd', 'Nw'.")

    value, unit = int(match.group(1)), match.group(2)
    if unit == "s":
        # N秒ごとに実行 (例: '*/10' は毎分 0, 10, 20, ..., 50秒に実行)
        return {"second": f"*/{value}"}
    elif unit == "m":
        # N分ごとに実行、00秒に実行
        return {"minute": f"*/{value}", "second": 0}
    elif unit == "h":
        # N時間ごとに実行、00分00秒に実行
        return {"hour": f"*/{value}", "minute": 0, "second": 0}
    elif unit == "d":
        # N日ごとに実行、0時00分00秒に実行
        return {"day": f"*/{value}", "hour": 0, "minute": 0, "second": 0}
    else:
        raise ValueError("Unsupported time unit.")


def revert_time_period(cron_args: dict, time_map: dict) -> str:
    """
    cron_args:
        例: cron_args = {'day': '*/1', 'hour': 0, 'minute': 0, 'second': 0}
    time_map:
        例: time_map = {'day': 'd', 'hour': 'h', 'minute': 'm', 'second': 's'}
    """
    for key, unit_char in time_map.items():
        if key in cron_args:
            value = str(cron_args.get(key))
            if value.startswith("*/"):
                try:
                    num = value.split("/")[1]
                    return f"{num}{unit_char}"
                except IndexError:
                    continue
    raise ValueError(
        f"指定されたcron引数から時間文字列を特定できませんでした: {cron_args}"
    )
