import json
import os
import statistics
import time
import urllib.request
import xlwt


class Gene:
    '''
    A class to store Gene information and annotation
    '''
    def __init__(self, name):
        self.uid = None
        self.description = None
        self.name = name
        self.organ = None
        self.summary = None

        # Data
        self.fast = None
        self.of = None
        self.off = None
        self.dpf = None

        # Data difference
        self.fast_of = 0
        self.fast_off = 0
        self.fast_dpf = 0
        self.of_off = 0
        self.of_dpf = 0
        self.off_dpf = 0

        # For drawing heatmap
        self.total_diff = 0


def parse_input(input_file):
    '''
    Read input data, parse the gene name for further query
    '''
    if not os.path.exists(input_file):
        raise FileNotFoundError('Input file not found')

    header = []
    # gene = [Gene1, Gene2, ...]
    gene = []
    with open(input_file) as f:
        for line in f:
            if len(header) == 0:
                header = line.rstrip('\n').split('\t')
                continue
            # ['ABC', 'NA', 123, 1234, 3425, ...]
            temp = line.rstrip('\n').split('\t')

            fast = (int(temp[2]) + int(temp[6])) / 2
            of = (int(temp[3]) + int(temp[8])) / 2
            off = (int(temp[5]) + int(temp[7])) / 2
            dpf = (int(temp[4]) + int(temp[9])) / 2

            # filt out < 200 data
            if statistics.mean([fast, of, off, dpf]) < 200:
                continue
            # temp[0] = 'gene name ABC'
            gene_obj = Gene(temp[0])
            gene_obj.fast = fast
            gene_obj.of = of
            gene_obj.off = off
            gene_obj.dpf = dpf

            gene_obj.fast_of = (gene_obj.of - gene_obj.fast) / gene_obj.fast
            gene_obj.fast_off = (gene_obj.off - gene_obj.fast) / gene_obj.fast
            gene_obj.fast_dpf = (gene_obj.dpf - gene_obj.fast) / gene_obj.fast
            gene_obj.of_off = (gene_obj.off - gene_obj.of) / gene_obj.of
            gene_obj.of_dpf = (gene_obj.dpf - gene_obj.of) / gene_obj.of
            gene_obj.off_dpf = (gene_obj.dpf - gene_obj.off) / gene_obj.off
            gene_obj.total_diff = gene_obj.fast_of + gene_obj.fast_off + (
                gene_obj.fast_dpf + gene_obj.of_off + gene_obj.of_dpf) + (
                gene_obj.off_dpf)
            gene.append(gene_obj)

    return header, gene


# Gene.name
def NCBI_url(gene_name):
    URL_name = ('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
                'esearch.fcgi?db=gene&term=')
    URL_info = ('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
                'esummary.fcgi?db=gene&id=')
    URL_suffix = '&retmode=json'

    uid = None
    name = gene_name
    description = None
    summary = None
    organ = None

    response = urllib.request.urlopen(URL_name + gene_name + URL_suffix)
    result = response.read()
    json_res = json.loads(result)
    # json_res['esearchresult']['retmax']
    uid_string = json_res['esearchresult']['idlist']
    uid_list = [int(x) for x in uid_string]

    if len(uid_list) == 0:
        return uid, name, description, summary, organ

    uid_list.sort()
    uid = uid_list[0]

    response = urllib.request.urlopen(URL_info + str(uid) + URL_suffix)
    result = response.read()
    json_res = json.loads(result)
    description = json_res['result'][str(uid)]['description']
    summary = json_res['result'][str(uid)]['summary']
    organ = json_res['result'][str(uid)]['organism']['scientificname']

    if summary == '':
        summary = 'No Summary available :('
    time.sleep(0.33)

    return uid, name, description, summary, organ


def write_data(neg_list, pos_list, name1, name2, env):
    annotation_file = xlwt.Workbook()
    sheet = annotation_file.add_sheet(name1 + " v.s. " + name2 + " POS",
                                      cell_overwrite_ok=True)
    sheet.write(0, 0, "UID")
    sheet.write(0, 1, "Name")
    sheet.write(0, 2, "Description")
    sheet.write(0, 3, "Summary")
    sheet.write(0, 4, "Organism")
    sheet.write(0, 5, "Difference")
    for i in range(len(pos_list)):
        uid, name, description, summary, organ = NCBI_url(pos_list[i].name)
        sheet.write(i + 1, 0, uid)
        sheet.write(i + 1, 1, name)
        sheet.write(i + 1, 2, description)
        sheet.write(i + 1, 3, summary)
        sheet.write(i + 1, 4, organ)
        diff = get_diff(pos_list[i], env)
        sheet.write(i + 1, 5, diff)

    sheet = annotation_file.add_sheet(name1 + " v.s. " + name2 + " NEG",
                                      cell_overwrite_ok=True)
    sheet.write(0, 0, "UID")
    sheet.write(0, 1, "Name")
    sheet.write(0, 2, "Description")
    sheet.write(0, 3, "Summary")
    sheet.write(0, 4, "Organism")
    for i in range(len(neg_list)):
        uid, name, description, summary, organ = NCBI_url(neg_list[i].name)
        sheet.write(i + 1, 0, uid)
        sheet.write(i + 1, 1, name)
        sheet.write(i + 1, 2, description)
        sheet.write(i + 1, 3, summary)
        sheet.write(i + 1, 4, organ)
        diff = get_diff(neg_list[i], env)
        sheet.write(i + 1, 5, diff)

    annotation_file.save(name1 + "_" + name2 + ' significant genes.xls')


def get_diff(gene, env):
    if env == 0:
        return gene.fast_of
    elif env == 1:
        return gene.fast_off
    elif env == 2:
        return gene.fast_dpf
    elif env == 3:
        return gene.of_off
    elif env == 4:
        return gene.of_dpf
    elif env == 5:
        return gene.off_dpf
    return -1
