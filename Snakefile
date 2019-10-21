SIM_COUNT = 10

rule all:
    input:
        expand('exp_{n}/box_plot.png', n=range(SIM_COUNT))


rule create:
    output:
        expand('exp_{n}/para_dict.pickle', n=range(SIM_COUNT))
    shell:
        '''
        python create_paras.py {output}
        '''

rule simulate:
    input: 'exp_{n}/para_dict.pickle'
    output: 'exp_{n}/box_plot.png'
    shell:
        '''
        python run_selectivity.py {input} {output}
        '''
