from itertools import cycle
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from matplotlib.lines import Line2D
from matplotlib import rc
import pandas as pd
import os, sys
import json

EXAMPLE_CTRL_JSON = """######### EXAMPLE JSON: #########
{
    "title": "cdf figure", 
    "x_label": "VAR X", 
    "y_label": "", 
    "save_path": "./cdf.pdf", 
    "show_figure": false, 
    "data": [
        {
            "legend": "Baseline", 
            "csv_path": "./similarity_score.csv", 
            "col_name": "baseline", 
            "sample_range": [0, 1.002, 0.001], 
            "count_out_of_range_data": true
        }, 
        {
            "legend": "Tor", 
            "csv_path": "./similarity_score.csv", 
            "col_name": "torsocks", 
            "sample_range": [0, 1.002, 0.001], 
            "count_out_of_range_data": true
        }
    ]
}
"""


def set_plot_options():
    options = {
        # 'backend': 'PDF',
        'font.size': 14,
        'figure.figsize': (4, 2.67),
        'figure.dpi': 100.0,
        'figure.subplot.left': 0.20,
        'figure.subplot.right': 0.97,
        'figure.subplot.bottom': 0.20,
        'figure.subplot.top': 0.90,
        'grid.color': '0.1',
        'grid.linestyle': ':',
        # 'grid.linewidth': 0.5,
        'axes.grid': True,
        # 'axes.grid.axis' : 'y',
        # 'axes.axisbelow': True,
        'axes.titlesize': 'x-small',
        'axes.labelsize': 'small',
        'axes.formatter.limits': (-4, 4),
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'lines.linewidth': 2.0,
        'lines.markeredgewidth': 0.5,
        'lines.markersize': 4,
        'legend.fontsize': 9,
        'legend.fancybox': False,
        'legend.shadow': False,
        'legend.borderaxespad': 0.5,
        'legend.numpoints': 1,
        'legend.handletextpad': 0.5,
        'legend.handlelength': 2.0,
        'legend.labelspacing': .25,
        'legend.markerscale': 1.0,
        # turn on the following to embedd fonts; requires latex
        'ps.useafm': True,
        'pdf.use14corefonts': True,
        'text.usetex' : True,
    }
    for option_key in options:
        matplotlib.rcParams[option_key] = options[option_key]
    if 'figure.max_num_figures' in matplotlib.rcParams:
        matplotlib.rcParams['figure.max_num_figures'] = 50
    if 'figure.max_open_warning' in matplotlib.rcParams:
        matplotlib.rcParams['figure.max_open_warning'] = 50
    if 'legend.ncol' in matplotlib.rcParams:
        matplotlib.rcParams['legend.ncol'] = 50



def data_prepare(df_path, col_name, sample_range, count_out_of_range_data=False):
    """
    sample_range = [start, end, interval], start can be left, end can be right if all data are included.
    count_out_of_range_data = True if out of range data are counted in Denominator
    """
    df = pd.read_csv(df_path)
    df = df[col_name]
    ori_len = len(df)
    df = df[df >= sample_range[0]] if sample_range[0] != 'left' else df
    df = df[df <= sample_range[1]] if sample_range[0] != 'right' else df
    new_len = len(df)
    total_len = ori_len if count_out_of_range_data else new_len
    res = []
    threshold = sample_range[0]
    while threshold <= sample_range[1]:
        num_target = len(df[df <= threshold])
        res.append({"var": threshold, "cd": num_target / total_len})
        threshold +=sample_range[2]
    return res

def parse_cmd(json_path):
    with open(json_path, 'r') as f:
        cmds = json.load(f)
    data_list = []
    legend_list = []
    for data_single in cmds['data']:
        dl = data_prepare(data_single['csv_path'],data_single['col_name'],data_single['sample_range'], count_out_of_range_data=data_single['count_out_of_range_data'])
        data_list.append(dl)
        legend_list.append(data_single['legend'])
    cdf_plot(data_list, legend_list, cmds['title'], cmds['save_path'], xlabel=cmds['x_label'], ylabel=cmds['y_label'], show_figure=cmds['show_figure'])


def cdf_plot(res_data_list, legend_list, title, save_path, xlabel="", ylabel="", show_figure=True):
    # Fixing random state for reproducibility
    set_plot_options()
    lines = ["-", "--", "-.", ":"]
    linecycler = cycle(lines)
    var_num = len(res_data_list)
    plot_idx = 0
    for res in res_data_list:
        plot_idx += 1
        x_direct = []
        y_direct = []
        for r in res:
            x_direct.append(r['var'])
            y_direct.append(r['cd'])
        exec("p%d= plt.plot(x_direct, y_direct,linestyle=next(linecycler))" % plot_idx)
    if len(xlabel) > 0:
        plt.xlabel(xlabel)
    if len(ylabel) > 0:
        plt.ylabel(ylabel)
    if len(title) > 0:
        plt.title(title)
    add_legend = "plt.legend(("
    for i in range(1, var_num):
        add_legend += "p%d[0], " % i
    add_legend += "p%d[0]), (" % var_num
    add_legend += str(legend_list).strip('[]')
    add_legend += "))"
    print(add_legend)
    exec(add_legend)
    axes = plt.gca()
    # axes.set_xlim([xmin,xmax])
    axes.set_ylim([0, 1])
    plt.savefig(save_path)
    if show_figure:
        plt.show()

def generate_example_json():
    print(EXAMPLE_CTRL_JSON)


def main():
    if len(sys.argv) != 2:
        print("Usage: cdf_plot path/to/conf.json")
        exit()
    if sys.argv[1] == '-g':
        generate_example_json()
    else:
        parse_cmd(sys.argv[1])
if __name__ == '__main__':
    main()
