from get_reference_seq.get_reference import get_reference_allele

conv23ME_CHROM_INDEX = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5,
                    "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
                    "11": 11, "12": 12, "13": 13, "14": 14, "15": 15,
                    "16": 16, "17": 17, "18": 18, "19": 19, "20": 20,
                    "21": 21, "22": 22, "X": "X", "Y": "Y", "MT": "M",
                    }


def conv23andme_to_vcf(conv23Me_file):
    for conv23Me_line in conv23Me_file:
        conv23Me_fields = conv23Me_line.strip().split('\t')
        rsid = conv23Me_fields[0]
        chrom = conv23Me_CHROM_INDEX[conv23Me_fields[1]]
        pos = int(conv23Me_fields[2])
        genotype = conv23Me_fields[3]

        vcf_chrom = None
        vcf_pos = None
        vcf_id = None
        vcf_ref = None
        vcf_alt = None
        vcf_qual = '.'
        vcf_filter = '.'
        vcf_info = '.'
        vcf_format = 'GT'
        vcf_genome_data = None

        # set vcf_chrom, vcf_pos, and vcf_id
        vcf_chrom = chrom
        vcf_pos = pos
        if rsid.startswith('rs'):
            vcf_id = rsid
        else:
            vcf_id = '.'

        refallele = get_reference_allele('chr' + str(chrom), pos)
        vcf_ref = refallele

        # This is for extracting the ref/alt alleles
        split_genotype = self.genotype.split("")
        allele_list = []
        allele_list.append(refallele)
        for allele in split_genotype:
            if not allele in allele_list:
                allele_list.append(allele)
        alt_list = allele_list[1:]
        if alt_list:
            vcf_alt = ','.join(alt_list)
        else:
            vcf_alt = '.'

        vcf_genome_data = '/'.join([str(allele_list.index(x)) for
                                    x in split_genotype])
        # build the vcf line
        vcf_line ='\t'.join[vcf_chrom, vcf_pos,
                        vcf_id, vcf_ref, vcf_alt,
                        vcf_qual, vcf_filter, vcf_info, vcf_format, vcf_genome_data]
        yield vcf_line