# Final-Project-
The project is owned by Xinyi(Cindy) Fu and will be used for University of Colorado Boulder MCDB department. The experiment data is confidential here so there is only one page of example data here. Please contact xifu0847@colorado.edu for any more detail about this tool

# Usage
The usage of this repository is pretty straight forward. An example command line is:

```sh
python driver.py --input_file=merged_gene_counts.txt --sample_num=30
```

Note that the input file is the one gathered from third party gene data analyzer and it should be in the pre-defined format. See merged_gene_counts.txt as an example input data.

The sample number is a parameter that defines how many gene does an user is interested in. It should be a number in range 1-50. Note that the program will be a bit slow with the increasing of sample_num.

# Example result:

## What will this project do?
- Parse the raw data into a defined format
- Filter out not fully expressed gene(the one with gene count under 200)
- Order the gene with gene_counts difference and find the most increased/decreased X genes. (X is the sample number from the input argument)
- Send query to NCBI database and fetch the gene summary for further study.
- Draw a heatmap which indicates the difference of interested genes.

## Output result:
The delivery can be divided into two parts: (1) Gene Summary (2) Heatmap

### Gene Summary

Gene summary is a spreadsheet that includes all interested gene summary filtered out from raw data.

The result of a URL query is available at: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gene&id=285&version=2.0&retmode=json

Some fields are filtered and saved in the spreadsheet with a name as xxx_xxx.xls. The example output is available in the repository.

### Heatmap

The goal of drawing a heatmap is makeing data visualized. The most "active" gene is obvious in the heatmap. Usually, there are output heatmap for a input data - Most X increased gene and Most X decreased gene.

An example output is:

- Most 20 increased gene:

![avatar](https://raw.githubusercontent.com/xifu0847/Final-Project-/master/Most%20significant%20Gene%20-%20Increase.png?token=AMLOEOH2CDUWBCCVVWZIKBC56MNTC)

- Most 20 decreased gene:

![avatar](https://raw.githubusercontent.com/xifu0847/Final-Project-/master/Most%20significant%20Gene%20-%20Decrease.png?token=AMLOEOEOWYS2J3HSB2AKYHK56MNXM)
