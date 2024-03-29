
# Freeling tags to override and replace by other tags
TAGS = {'I': 'AQ0MS00', 'DP1MPP': 'AP0MP1P', 'AQVMP00':'AQ0MP00',
        'DP1MSP': 'AP0MS1P', 'DP1FPP': 'AP0FP1P', 'DP1FSP': 'AP0FS1P', 'AQVFS00': 'AQ0FS00'}

REPLACE_LEMMA_AND_TAG = {'ladra': {'lemma': 'ladrar', 'tag':'VMIP3S0'}, 'dió': {'lemma': 'dar', 'tag': 'VMIS3S0'},
                         'dios': {'lemma': 'dios', 'tag': 'NCMS000'},
                         'adiós': {'lemma': 'adiós', 'tag': 'NCMS000'},
                         'señor': {'lemma': 'señor', 'tag': 'NCMS000'},
                         }


DO_NOT_OVERRIDE = {'uf', 'je', 'ja', 'oh', 'todo_lo_contrario', 'ojalá'}

STEM_EQUALS_TAG = {'Z', 'W'}

'''
The MAL_TAGS maps the tags that come from Freeling morphophonological tagger and maps them to all names of
lexical rules in inflr.tdl that are necessary for covering learner constructions (where there is an agreement mismatch).
'''
# For now, we only implement gender mismatch. In the commented out mapping, the second tags are intended for number mismatch,
# which is not yet fully implemented in inflr.tdl and irtypes.tdl and srtypes.tdl and srules.tdl.
#MAL_TAGS = {'NCFS000':'NCFS000-MG, NCFS000-MN', 'NCMS000':'NCMS000-MG, NCMS000-MN', 'NCFP000':'NCFP000-MG, NCFP000-MN'}
MAL_TAGS = {'NCFS000':'NCFS000-MG', 'NCMS000':'NCMS000-MG', 'NCFP000':'NCFP000-MG', 'NCMP000':'NCMP000-MG',
            'NCFP00V':'NCFP00V-MG', 'NCMP00V':'NCMP00V-MG', 'NCFS00V':'NCFS00V-MG', 'NCMS00V':'NCMS00V-MG',
            'NCFP00A':'NCFP00A-MG', 'NCMP00A':'NCMP00A-MG', 'NCFS00A':'NCFS00A-MG', 'NCMS00A':'NCMS00A-MG',
            'NCFP00X':'NCFP00X-MG', 'NCMP00X':'NCMP00X-MG', 'NCFS00X':'NCFS00X-MG', 'NCMS00X':'NCMS00X-MG',
            'NCFP00D':'NCFP00D-MG', 'NCMP00D':'NCMP00D-MG', 'NCFS00D':'NCFS00D-MG', 'NCMS00D':'NCMS00D-MG',
            'AQ0MS00':'AQ0MS00-MG', 'AQ0FS00':'AQ0FS00-MG', 'AQ0MP00':'AQ0MP00-MG', 'AQ0FP00':'AQ0FP00-MG',
            'AQSMS00':'AQSMS00-MG', 'AQSMP00':'AQSMP00-MG', 'AQSFS00':'AQSFS00-MG', 'AQSFP00':'AQSFP00-MG',
            'AQDMS00':'AQDMS00-MG', 'AQDMP00':'AQDMP00-MG', 'AQDFS00':'AQDFS00-MG', 'AQDFP00':'AQDFP00-MG',
            'AQ0MSP':'AQ0MSP-MG', 'AQ0FSP':'AQ0FSP-MG', 'AQ0MPP':'AQ0MPP-MG', 'AQ0FPP':'AQ0FPP-MG',
            'VMP00SM':'VMP00SM-MG', 'VMP00SF':'VMP00SF-MG', 'VMP00PM':'VMP00PM-MG', 'VMP00PF':'VMP00PF-MG',}

