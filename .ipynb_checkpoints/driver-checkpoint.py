import argparse
import os
import process

import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap


def get_parser():
    parser = argparse.ArgumentParser(
        description='Driver program, please define input file')

    parser.add_argument('--input_file', type=str, default='',
                        help='Input gene counts txt file')
    parser.add_argument('--sample_num', type=int, default=20,
                        help='Interested gene counts should be 1-50')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = get_parser()

    if not os.path.exists(args.input_file):
        raise FileNotFoundError('Input file not found')
    if args.sample_num <= 0 or args.sample_num > 50:
        raise ValueError('sample number should be 1-50')

    # Get gene list from parse_input function
    header, gene = process.parse_input(args.input_file)

    # Significant list
    sig_list_pos = []
    sig_list_neg = []

    # sort by class attributes and find most significant Gene
    gene.sort(key=lambda Gene: Gene.fast_of)
    fast_of_neg = gene[:args.sample_num]
    fast_of_pos = gene[(0 - args.sample_num):]
    fast_of_pos.reverse()
    sig_list_pos = sig_list_pos + fast_of_pos
    sig_list_neg = sig_list_neg + fast_of_neg

    process.write_data(fast_of_neg, fast_of_pos, 'Fast', 'OF', 0)

    gene.sort(key=lambda Gene: Gene.fast_off)
    fast_off_neg = gene[:args.sample_num]
    fast_off_pos = gene[(0 - args.sample_num):]
    fast_off_pos.reverse()
    sig_list_pos = sig_list_pos + fast_off_pos
    sig_list_neg = sig_list_neg + fast_off_neg

    process.write_data(fast_off_neg, fast_off_pos, 'Fast', 'OFF', 1)

    gene.sort(key=lambda Gene: Gene.fast_dpf)
    fast_dpf_neg = gene[:args.sample_num]
    fast_dpf_pos = gene[(0 - args.sample_num):]
    fast_dpf_pos.reverse()
    sig_list_pos = sig_list_pos + fast_dpf_pos
    sig_list_neg = sig_list_neg + fast_dpf_neg

    process.write_data(fast_dpf_neg, fast_dpf_pos, 'Fast', 'DPF', 2)

    gene.sort(key=lambda Gene: Gene.of_off)
    of_off_neg = gene[:args.sample_num]
    of_off_pos = gene[(0 - args.sample_num):]
    of_off_pos.reverse()
    sig_list_pos = sig_list_pos + of_off_pos
    sig_list_neg = sig_list_neg + of_off_neg

    process.write_data(of_off_neg, of_off_pos, 'OF', 'OFF', 3)

    gene.sort(key=lambda Gene: Gene.of_dpf)
    of_dpf_neg = gene[:args.sample_num]
    of_dpf_pos = gene[(0 - args.sample_num):]
    of_dpf_pos.reverse()
    sig_list_pos = sig_list_pos + of_dpf_pos
    sig_list_neg = sig_list_neg + of_dpf_neg

    process.write_data(of_dpf_neg, of_dpf_pos, 'OF', 'DPF', 4)

    gene.sort(key=lambda Gene: Gene.off_dpf)
    off_dpf_neg = gene[:args.sample_num]
    off_dpf_pos = gene[(0 - args.sample_num):]
    off_dpf_pos.reverse()
    sig_list_pos = sig_list_pos + off_dpf_pos
    sig_list_neg = sig_list_neg + off_dpf_neg

    process.write_data(off_dpf_neg, off_dpf_pos, 'OFF', 'DPF', 5)

    sig_set_pos = set(sig_list_pos)
    sig_set_neg = set(sig_list_neg)
    sig_list_pos = list(sig_set_pos)
    sig_list_neg = list(sig_set_neg)
    sig_list_pos.sort(key=lambda Gene: Gene.total_diff, reverse=True)
    sig_list_neg.sort(key=lambda Gene: Gene.total_diff)

    matrix_pos = []
    matrix_neg = []

    for obj in sig_list_pos:
        matrix_pos.append([obj.fast_of, obj.fast_off, obj.fast_dpf,
                           obj.of_off, obj.of_dpf, obj.off_dpf])
    for obj in sig_list_neg:
        matrix_neg.append([obj.fast_of, obj.fast_off, obj.fast_dpf,
                           obj.of_off, obj.of_dpf, obj.off_dpf])

    fig = plt.figure(figsize=(10, 20))
    xticks = ['Fast_OF', 'Fast_OFF', 'Fast_DPF', 'OF_OFF', 'OF_DPF', 'OFF_DPF']
    yticks = [obj.name for obj in sig_list_neg]
    sns.heatmap(matrix_neg, vmin=-1, vmax=0, cmap='coolwarm',
                xticklabels=xticks, yticklabels=yticks)
    plt.title('Most significant Gene - Decrease')
    plt.savefig("Most significant Gene - Decrease")
    plt.close()

    fig = plt.figure(figsize=(10, 20))
    xticks = ['Fast_OF', 'Fast_OFF', 'Fast_DPF', 'OF_OFF', 'OF_DPF', 'OFF_DPF']
    yticks = [obj.name for obj in sig_list_pos]
    sns.heatmap(matrix_neg, vmin=0, vmax=1, cmap='coolwarm',
                xticklabels=xticks, yticklabels=yticks)
    plt.title('Most significant Gene - Increase')
    plt.savefig("Most significant Gene - Increase")
    plt.close()
