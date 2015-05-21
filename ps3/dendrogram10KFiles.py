import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage 

def dendo():   
    ### 10 X 10 matrix of the jargon distance
    mat = [[ch_11,ch_12,ch_13,ch_14,ch_15,ch_16,ch_17,ch_18,ch_19,ch_110],
           [ch_21,ch_22,ch_23,ch_24,ch_25,ch_26,ch_27,ch_28,ch_29,ch_210],
           [ch_31,ch_32,ch_33,ch_34,ch_35,ch_36,ch_37,ch_38,ch_39,ch_310],
           [ch_41,ch_42,ch_43,ch_44,ch_45,ch_46,ch_47,ch_48,ch_49,ch_410],
           [ch_51,ch_52,ch_53,ch_54,ch_55,ch_56,ch_57,ch_58,ch_59,ch_510],
           [ch_61,ch_62,ch_63,ch_64,ch_65,ch_66,ch_67,ch_68,ch_69,ch_610],
           [ch_71,ch_72,ch_73,ch_74,ch_75,ch_76,ch_77,ch_78,ch_79,ch_710],
           [ch_81,ch_82,ch_83,ch_84,ch_85,ch_86,ch_87,ch_88,ch_89,ch_810],
           [ch_91,ch_92,ch_93,ch_94,ch_95,ch_96,ch_97,ch_98,ch_99,ch_910],
           [ch_101,ch_102,ch_103,ch_104,ch_105,ch_106,ch_107,ch_108,ch_109,ch_1010]]
            
    linkage_matrix = linkage(mat, 'average') ### UPGMA algorithm
    #print linkage_matrix
    
    plt.title("Jargon Distance Plot across various fields")
    plt.ylabel('jargon distance')
    dendrogram(linkage_matrix,
               labels=array(['Ecology and Evolution', 'Molecular and Cell Biology', 'Economics','Sociology',
                             'Probability and Statistics','Organizational and marketing','Law','Anthropology','Political Science','Education']),
               leaf_rotation=90)
    plt.tight_layout()
    plt.show()

dendo()