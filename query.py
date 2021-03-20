from __future__ import print_function

"""

Author:     Emmanuel Salawu 
Email:      dr.emmanuel.salawu@gmail.com 


   Copyright 2016 Emmanuel Salawu

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.


"""

import sys,os
import cPickle as cP, math
import subprocess as sbp
import numpy as np
import time
import argparse
# from Bio import SeqIO, Blast
# from Bio.Blast.Applications import NcbiblastnCommandline, NcbiblastpCommandline
# import Bio.Blast.NCBIXML as NCBIXML



d3_ = {'A': (2649921, 0.109), 'C': (284780, 0.012), 'E': (2037420, 0.084), 'D': (1266155, 0.052), 'G': (1127806, 0.046), 'F': (927803, 0.038), 'I': (1418628, 0.058), 'H': (535711, 0.022), 'K': (1547402, 0.064), 'M': (642753, 0.026), 'L': (2794992, 0.115), 'N': (916269, 0.038), 'Q': (1098361, 0.045), 'P': (509355, 0.021), 'S': (1298566, 0.053), 'R': (1427259, 0.059), 'T': (1180051, 0.049), 'W': (337622, 0.014), 'V': (1505317, 0.062), 'Y': (795511, 0.033)}


#Source http://web.expasy.org/docs/relnotes/relstat.html
rel_ab = {'A': 0.08259999999999999, 'C': 0.0137, 'E': 0.0674, 'D': 0.0546, 'G': 0.0708, 'F': 0.038599999999999995, 'I': 0.0593, 'H': 0.0227, 'K': 0.0582, 'M': 0.0241, 'L': 0.0965, 'N': 0.0406, 'Q': 0.0393, 'P': 0.0472, 'S': 0.0659, 'R': 0.0553, 'T': 0.053399999999999996, 'W': 0.0109, 'V': 0.0687, 'Y': 0.0292}


#Based on log_e                                                     math.log
d4_ = {key:(value[0], value[1], rel_ab[key], value[1]/rel_ab[key], math.log (value[1]/rel_ab[key])) for (key, value) in d3_.items()}


d4_rounded = {i: (d4_[i][0], d4_[i][1], round(d4_[i][2], 3), round(d4_[i][3], 3), round(d4_[i][4], 3),) for i in d4_}


needed_contacts = None
needed_dir = 'contacts'
compressed_hh_contacts = None



def scoreMatchedSeq (matchedSeq, contacts = [0], aaScore = d4_, divisor = 1.0):
    score = sum ([aaScore.get (aa, (0., 0.))[-1] for aa in matchedSeq])
    normalizsedScore = score / (divisor or 1.0)
    return round (normalizsedScore, 3), round (score, 3), 100.0 - np.mean (contacts)

def parseLine (line, lenOfPattern, matchedPattern):
    global needed_contacts
    #print matchedPattern
    split_line = line.split ()
    split_0_line = split_line [0].split ('_')
    start_of_full_helix, end_of_full_helix = int (split_0_line [3]), int (split_0_line [4])
    
    seq = split_line [1]
    start = int (split_line [2])
    stop = start + lenOfPattern
    
    index_in_db = int (split_line [3])
    
    try:
        if not needed_contacts:
            needed_contacts = cP.load (open ('needed_contacts_%s.cP' % needed_dir, 'rb'))
        contacts = needed_contacts [index_in_db][1] [start : stop]
    except:
        contacts = [0]
    
    start_in_pdb = start_of_full_helix + start
    stop_in_pdb = start_of_full_helix + stop
    
    matchedSeq = seq [start : stop]
    score = scoreMatchedSeq (matchedSeq, contacts)
    
    return [score, 
            (split_0_line [0], split_0_line [1], 1, #int (split_0_line [2]), 
             start_of_full_helix, end_of_full_helix, ), 
            split_line [1], start, (start_in_pdb, stop_in_pdb - 1),
            int (split_line [3]),
            matchedPattern, matchedSeq,
            highlight1 (split_line [1], start, stop, matchedPattern),
            #,        ,
            ]
    

def parseRawOutput (raw_output):
    raw_output_seg = [l for l in 
                        [[k for k in [j.strip() for j in i.splitlines()] if k] for i in 
                        raw_output.split ('>')] if l]
    return raw_output_seg

def parseKey (key):
    global split_key_list
    key_proper = ''
    split_key_1 = key.split ('_')
    
    split_key_list = []
    
    for index_1, item_1 in enumerate ( split_key_1 ):
        index_1p = index_1 - 1
        if item_1.isdigit():
            split_key_2 = [item_1]
        else:
            split_key_2 = list (item_1)
        for item_2 in split_key_2:
            try:
                split_key_list.append (int (item_2))
            except:
                split_key_list.append (item_2)
    
        if len (item_1) > 1:
            if not index_1: #len (split_key_list) < 6:
                start = 0
            else:
                if (split_key_list [(index_1p * 2) + 1] + split_key_list [(index_1p * 2) + 3]) < split_key_list [(index_1p * 2) + 5]:
                    start = 1
                else:
                    start = 3
            key_proper += item_1 [start :]
    return key_proper, split_key_list, effectiveLenOfKeyProper (key_proper)
    #E4D3E_5_D3E3H
    #04589   589
    #        1 3
    # 1 3  5  7 9 11
    


def parseRawOutputIntoNativeTypes (raw_output_seg):
    
    raw_output_seg_native = []
    for item in raw_output_seg:
        raw_output_seg_native.append ([])
        
        for lineId, line in enumerate (item):
            if lineId == 0:
                raw_output_seg_native [-1].append ( parseKey (line) )
            else:
                raw_output_seg_native [-1].append ( parseLine (line, 
                                                                raw_output_seg_native [-1][0][2],
                                                                raw_output_seg_native [-1][0][0] ) )
    
    return raw_output_seg_native



def effectiveLenOfKeyProper (key):
    'F0D2E2H'
    return sum ([int(i) if i.isdigit () else 1 for i in list (key)])


def simpleHighlight1 (seq, start, stop, tagBeg = '<span class="sh_1">', tagEnd = '</span>'):
    return seq [:start] + tagBeg + seq [start : stop] + tagEnd + seq [stop:]


def simpleHighlight2 (seq, start, stop, tagBeg = '<span class="sh_1">', tagEnd = '</span>'):
    return seq [:start] + tagBeg + seq [start : stop] + tagEnd + seq [stop:]


def breakSeq (seq, currentOffset=0, segLen=30):
    pos = 0
    lenSeq = len (seq)
    if (lenSeq + currentOffset) < segLen:
        return seq
    output = ''
    positions = range (-currentOffset, lenSeq, segLen) 
    #print positions 
    for index, pos in enumerate (positions [1:]):
        output += seq [max (0, positions [index]): pos] + '<br/>'
    output += seq [pos :]
    return output



def detailedHighlightShortSeq (shortSeq, matchedPattern, tagBeg = '<span class="dh_1">', tagEnd = '</span>', start=0):
    '4xr7_J_1_544_561 TTLLTDLGYLFDMMERSH 10 208869'
    #global possitionsProcessed
    #print shortSeq
    #F0D2E2H        FDMMERSH
    #               01234567
    neededStr = ''
    aaAndNumbers = [int(i) if i.isdigit () else i for i in matchedPattern]
    #['F', 0, 'D', 2, 'E', 2, 'H']
    #<span >FD</span>MM<span >E</span>RS<span >H</span>
    possitionsProcessed = 0; numOfBrAdded = (start // 30) + 1
    for index, aaOrNum in enumerate (aaAndNumbers):
        #print possitionsProcessed
        if shortSeq and (index % 2):
            if ((start + possitionsProcessed) > 30 * numOfBrAdded):
                neededStr += '<br/>'
                numOfBrAdded += 1
            if (possitionsProcessed == 0) and shortSeq: 
                print (shortSeq)
                print (possitionsProcessed)
                neededStr += tagBeg + shortSeq [possitionsProcessed] + tagEnd 
#            elif ((start + possitionsProcessed) > 30 * numOfBrAdded):
#                neededStr += '<br/>'
#                numOfBrAdded += 1
            neededStr += shortSeq [possitionsProcessed + 1 : possitionsProcessed + 1 + aaOrNum]  
            neededStr += tagBeg + shortSeq [possitionsProcessed + 1 + aaOrNum] + tagEnd 
            possitionsProcessed += 1 + aaOrNum
#        if index % 2:
#            if aaOrNum:
#                neededStr += tagBeg + shortSeq [possitionsProcessed] + tagEnd 
#                neededStr += shortSeq [possitionsProcessed + 1 : possitionsProcessed + 1 + aaOrNum]  
#                neededStr += tagBeg + shortSeq [possitionsProcessed + 1 + aaOrNum] + tagEnd 
#                possitionsProcessed += 1 + aaOrNum
#            else:
#                neededStr += tagBeg + shortSeq [possitionsProcessed : possitionsProcessed + 2] + tagEnd 
#                possitionsProcessed += 2
    neededStr = neededStr.replace (tagEnd + tagBeg, '')
    return neededStr


def highlight1 (seq, start, stop, matchedPattern, 
                tagBegSimple = '<span class="sh_1">', tagEndSimple = '</span>', 
                tagBegDetailed = '<span class="dh_1">', tagEndDetailed = '</span>'):
    
    return breakSeq (seq [:start], currentOffset=0, segLen=30) + tagBegSimple + \
            detailedHighlightShortSeq (seq [start : stop], matchedPattern, tagBegDetailed, tagEndDetailed, start=start) \
            + tagEndSimple + breakSeq (seq [stop:], currentOffset=stop % 30, segLen=30)

def generateSortedResults (raw_output_seg_native):
    results = []
    for each_result in raw_output_seg_native:
        results.extend (each_result [1:])
    sorted_results = sorted (results, reverse=True)
    return sorted_results



def process_output (raw_output, jobId):
    #raw_output = sampleOutput
    raw_output_seg = parseRawOutput (raw_output)
    raw_output_seg_native = parseRawOutputIntoNativeTypes (raw_output_seg)

    cP.dump (raw_output_seg_native, open ('%s.raw_output_seg_native' % jobId, 'wb'), -1)
    
    sorted_results = generateSortedResults (raw_output_seg_native)

    cP.dump (sorted_results, open ('%s.sorted_results' % jobId, 'wb'), -1)
    
    return sorted_results, raw_output_seg_native
    

def genHtmlTable (sorted_results): 
    global compressed_hh_contacts
    table_headers = ['#', 'U#', 'Matched<br/>Sequence (MS)', 'Matched<br/>Pattern', 'Full Helix (FH)', 'PDB ID: Chain', 
                     ' &nbsp;&nbsp; Positions in PDB &nbsp;&nbsp; <br/>(MS), (FH)', 'Helical<br/>Propensity', 'Contact', 'Interacting<br>Partners',
                        ] #'View Helix in 3D', ]
    
    output = '<tr>%s</tr>' % (''.join (['<th>%s</th>' % i for i in table_headers]), )
    
    uniqueness = set ([])
    
    for index, entry in enumerate (sorted_results):
        seq = entry [7] # entry [2]
        if seq in uniqueness:
            unique = 'not_unique'
        else: 
            uniqueness.add (seq)
            unique = 'unique'
        
        contact_ = '%.3f' % (100.0 - entry [0][2],) if (entry [0][2] != 100.0) else ''
        
        helical_contact = ''
        try:
            if not compressed_hh_contacts:
                compressed_hh_contacts = cP.load (open ('compressed_hh_contacts.cP' , 'rb'))
            #                                                PDB ID          CHAIN         start_end_pair                
            helical_contact_info = compressed_hh_contacts [entry [1][0]] [entry [1][1]] [(entry [1][3], entry [1][4])]

            for hc_info in helical_contact_info:
                helical_contact += "%(pdbid)s:%(chain)s (%(start)s, %(end)s)</br>"  % \
                    {"pdbid": entry [1][0], "chain": hc_info [1], "start": hc_info [2], "end": hc_info [3]}
        except:
            pass
        
        table_row = [str (index + 1), str (len (uniqueness)), entry [7], entry [6], entry [8],
                     '%s:%s'% (entry [1][0], entry [1][1]), 
                     '%s, (%s, %s)' % (str (entry [4]), entry [1][3], entry [1][4], ),
                     '%.3f' % (entry [0][0],), contact_, helical_contact, # 'View Helix'
                    ]
        output += '<tr class="%s">%s</tr>' % (unique, ''.join (['<td>%s</td>' % i for i in table_row]), )
        table_css = '''    
.sh_1 {color: blue;}
.dh_1 {font-weight: 900;}
.monospace {font-family: "Courier New", Courier, monospace; font-size: 80%; }
td {font-size: 80%; }
tr:nth-child(2n) {
	background-color:#F4F4F8;
}

tr:nth-child(2n+1) {
	background-color:#EFF1F1;
}
        '''
    return '<style>%s</style><span class="monospace"><table id="results1">%s</table></span>' % (table_css,output)








def genViableNumbers (string):
    if string.find ('/') != -1:
        parts = string.split ('/')
        firstPart = parts [0]
        secPart = parts [1]
        firstPart = [int (i) for i in firstPart.split (',')]
        secPart = [int (i) for i in secPart.split (',')]
        if len (firstPart) > 1: 
            firstPart [1] = firstPart [1] + 1
            firstPart = range (*firstPart)
        if len (secPart) > 1: 
            secPart [1] = secPart [1] + 1
            secPart = range (*secPart)
        needed_numbers = firstPart + secPart
    else:
        firstPart = [int (i) for i in string.split (',')]
        if len (firstPart) > 1: 
            firstPart [1] = firstPart [1] + 1
            firstPart = range (*firstPart)
        needed_numbers = firstPart
    return needed_numbers

def genViableAlphabets (string):
    return string.split ('/')

def genSubQueries (list_of_lists): # [[A, D], [1, 2, 3], [E, f]]
    sub_queries = []
    for itemI in list_of_lists [0]:
        for itemJ in list_of_lists [1]:
            for itemK in list_of_lists [2]:
                sub_queries.append ('%s%s%s' % (itemI, itemJ, itemK))
    return sub_queries

def genViableQueries (needed_sub_queries): # [['A0S', 'A2S', 'A4S'], ['S2L', 'S3L'], ['A3A']]
    num_levels = len (needed_sub_queries)
    viable_queries = []
    for itemsL0 in needed_sub_queries [0]:
        if num_levels > 1:
            for itemsL1 in needed_sub_queries [1]:
                if num_levels > 2:
                    for itemsL2 in needed_sub_queries [2]:
                        if num_levels > 3:
                            for itemsL3 in needed_sub_queries [3]:
                                #viable_queries.append (itemsL0 + '_' + itemsL1 + '_' + itemsL2 + '_' + itemsL3)
                                viable_queries.append (itemsL0 + itemsL1 [1:] + '_' + str (1 + int (itemsL0 [1:-1]) + 1 + int (itemsL1 [1:-1])) + '_' + itemsL2 [:-1] + itemsL3)
                        else:
                            #viable_queries.append (itemsL0 + '_' + itemsL1 + '_' + itemsL2)
                            #viable_queries.append (itemsL0 + itemsL1 [1:-1] + itemsL2)
                            viable_queries.append (itemsL0 + itemsL1 [1:] + '_' + str (1 + int (itemsL0 [1:-1])) + '_' + itemsL1 [:-1] + itemsL2)
                else:
                    #viable_queries.append (itemsL0 + '_' + itemsL1)
                    viable_queries.append (itemsL0 + itemsL1 [1:])
        else:
            viable_queries.append (itemsL0)
    return viable_queries
        
        

def processQuery (query):
    query_list = query.split ()
    expanded_subset = []
    for index, subset in enumerate (query_list):
        if index % 2 == 0:
            expanded_subset.append (genViableAlphabets (subset))
        else:
            expanded_subset.append (genViableNumbers (subset))
    
    needed_sub_queries = []
    for index in range (0, len (expanded_subset) - 2, 2):
        needed_sub_queries.append (genSubQueries (expanded_subset [index : index + 3]))
    
    viable_queries = genViableQueries (needed_sub_queries)
    
    return viable_queries

def genFastaForQuery (viable_queries, outputFileName):
    fasta = ''
    for queryIndex, viable_query in enumerate (viable_queries):
        if queryIndex == 0:
            fasta += '>%s %s\n%s\n' % (viable_query.replace ('_', ' '), outputFileName, viable_query)
        else:
            fasta += '>%s\n%s\n' % (viable_query.replace ('_', ' '), viable_query)
    return fasta



def mainQueryDb (query, outputFileName = 'outputFileName'):
    
    with open ('%s.submitted' % (outputFileName,), 'w') as submittedQuery: 
        submittedQuery.write (query)
    
    viable_queries = processQuery (query)
    
    fasta_query = genFastaForQuery (viable_queries, outputFileName)
    
    with open ('query.fasta', 'w') as query_file: query_file.write (fasta_query)
    
    sbp.call ('cp query.fasta pending_jobs', shell=True)


def query(example_query,outputFileName):
    raw_result_file = '%s.output' % outputFileName
    while os.path.exists(raw_result_file):
        os.remove(raw_result_file)
    mainQueryDb(example_query,outputFileName = outputFileName)

    i = 0
    while not os.path.exists(raw_result_file):
        i +=1
        status = '.' * (i%4)
        print( 'running%-3s'% status, end='\r')
        sys.stdout.flush()
        time.sleep(0.3)
    raw_result = open (raw_result_file).read ()

    sorted_results, raw_output_seg_native = process_output(raw_result,outputFileName)

    html_table = genHtmlTable (sorted_results)

    with open('%s_table.html'%outputFileName,'w') as f:
        f.write(html_table)

    print('The output file is %s_table.html'%outputFileName)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--query', help='The query string of TP-DB')
    parser.add_argument('--output', help='The output prefix')
    args = parser.parse_args()
    query(args.query,args.output)


# from query import query
# query('asdfasdfasdf','sdfsdsa')
# query('asdfasdfasdf1','sdfsdsa1')
# query('asdfasdfasdf2','sdfsdsa2')
# query('asdfasdfasdf3','sdfsdsa3')
