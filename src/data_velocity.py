import collections
import datetime
import json
import pathlib
import sys

import matplotlib.pyplot as plt
import matplotlib.dates as md


def fetch_data(data_file: pathlib.Path) -> collections.Counter:
    """
    Reads the data from the file and keeps only the required fields
    for faster in memory processing.

    :param data_file:
        Data file to read date values from.
    :return:
        Frequency count of timestamps for particular tweets.
    """
    result = list()
    with data_file.open("r", encoding="utf-8", errors="ignore") as fp:
        for line in fp.readlines():
            try:
                json_data = json.loads(line)
            except json.decoder.JSONDecodeError:
                continue
            else:
                timestamp = int(json_data.get("timestamp_ms")) / 1000
                datetime_obj = datetime.datetime.fromtimestamp(timestamp)

                result.append(datetime_obj)

    return collections.Counter(result)


def plot_data(d: collections.Counter, figure_path: pathlib.Path) -> None:
    """
    Plots a line plot for the given Counter object
    and saves the figure to a file.

    :param d:
        Counter object of timestamps to plot
    :param figure_path:
        Path of file to save the plot in.
    """
    x = list(d.keys())
    y = list(d.values())

    plt.plot(x, y)

    plt.xlabel("Date")
    plt.ylabel("Tweets received")

    plt.gca().xaxis.set_major_formatter(md.DateFormatter("%Y-%m-%d %H:%M"))

    plt.savefig(figure_path)
    plt.show()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Missing args: Mention the data file you want to use.")

    file_name = sys.argv[1]
    file_path = pathlib.Path.cwd() / "data" / "velocity" / f"{file_name}.jsonl"

    data = fetch_data(file_path)

    plot_path = pathlib.Path.cwd() / "plots" / "velocity" / f"{file_name}.png"
    plot_data(data, plot_path)
