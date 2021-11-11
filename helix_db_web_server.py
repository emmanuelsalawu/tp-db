# -*- coding: utf-8 -*-
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


import sys; reload(sys); sys.setdefaultencoding("utf-8"); import os
import cPickle as cP, math
import subprocess as sbp
import numpy as np

from Bio import SeqIO, Blast
from Bio.Blast.Applications import NcbiblastnCommandline, NcbiblastpCommandline
import Bio.Blast.NCBIXML as NCBIXML



d3_ = {'A': (2649921, 0.109), 'C': (284780, 0.012), 'E': (2037420, 0.084), 'D': (1266155, 0.052), 'G': (1127806, 0.046), 'F': (927803, 0.038), 'I': (1418628, 0.058), 'H': (535711, 0.022), 'K': (1547402, 0.064), 'M': (642753, 0.026), 'L': (2794992, 0.115), 'N': (916269, 0.038), 'Q': (1098361, 0.045), 'P': (509355, 0.021), 'S': (1298566, 0.053), 'R': (1427259, 0.059), 'T': (1180051, 0.049), 'W': (337622, 0.014), 'V': (1505317, 0.062), 'Y': (795511, 0.033)}


#Source http://web.expasy.org/docs/relnotes/relstat.html
rel_ab = {'A': 0.08259999999999999, 'C': 0.0137, 'E': 0.0674, 'D': 0.0546, 'G': 0.0708, 'F': 0.038599999999999995, 'I': 0.0593, 'H': 0.0227, 'K': 0.0582, 'M': 0.0241, 'L': 0.0965, 'N': 0.0406, 'Q': 0.0393, 'P': 0.0472, 'S': 0.0659, 'R': 0.0553, 'T': 0.053399999999999996, 'W': 0.0109, 'V': 0.0687, 'Y': 0.0292}


#Based on log_e                                                     math.log
d4_ = {key:(value[0], value[1], rel_ab[key], value[1]/rel_ab[key], math.log (value[1]/rel_ab[key])) for (key, value) in d3_.items()}
#d4_ = {'A': (2649921, 0.109, 0.08259999999999999, 1.3196125907990315, 0.2773382017022113), 'C': (284780, 0.012, 0.0137, 0.8759124087591241, -0.13248918304607887), 'E': (2037420, 0.084, 0.0674, 1.2462908011869436, 0.22017178092505224), 'D': (1266155, 0.052, 0.0546, 0.9523809523809523, -0.048790164169432056), 'G': (1127806, 0.046, 0.0708, 0.6497175141242938, -0.4312176042105791), 'F': (927803, 0.038, 0.038599999999999995, 0.9844559585492229, -0.015666116744399352), 'I': (1418628, 0.058, 0.0593, 0.9780775716694773, -0.022166295457260378), 'H': (535711, 0.022, 0.0227, 0.9691629955947135, -0.03132247112904127), 'K': (1547402, 0.064, 0.0582, 1.0996563573883162, 0.0949977286222798), 'M': (642753, 0.026, 0.0241, 1.0788381742738589, 0.07588469752487267), 'L': (2794992, 0.115, 0.0965, 1.1917098445595855, 0.17538912001830984), 'N': (916269, 0.038, 0.0406, 0.935960591133005, -0.0661819068813011), 'Q': (1098361, 0.045, 0.0393, 1.1450381679389312, 0.13543797089510412), 'P': (509355, 0.021, 0.0472, 0.44491525423728817, -0.8098714548680866), 'S': (1298566, 0.053, 0.0659, 0.8042488619119879, -0.21784652795633971), 'R': (1427259, 0.059, 0.0553, 1.0669077757685352, 0.06476453537743031), 'T': (1180051, 0.049, 0.053399999999999996, 0.9176029962546818, -0.0859904478555224), 'W': (337622, 0.014, 0.0109, 1.2844036697247707, 0.25029454038016063), 'V': (1505317, 0.062, 0.0687, 0.9024745269286755, -0.10261481418321203), 'Y': (795511, 0.033, 0.0292, 1.13013698630137, 0.12233885219224423)}

#Based on log_10
#d4_ = {key:(value[0], value[1], rel_ab[key], value[1]/rel_ab[key], math.log10 (value[1]/rel_ab[key])) for (key, value) in d3.items()}
#d4_ = {'A': (2649921, 0.109, 0.08259999999999999, 1.3196125907990315, 0.12044645062024141), 'C': (284780, 0.012, 0.0137, 0.8759124087591241, -0.05753932110878192), 'E': (2037420, 0.084, 0.0674, 1.2462908011869436, 0.09561938952656182), 'D': (1266155, 0.052, 0.0546, 0.9523809523809523, -0.021189299069938095), 'G': (1127806, 0.046, 0.0708, 0.6497175141242938, -0.18727542600819494), 'F': (927803, 0.038, 0.038599999999999995, 0.9844559585492229, -0.006803708054944775), 'I': (1418628, 0.058, 0.0593, 0.9780775716694773, -0.0096266998013253), 'H': (535711, 0.022, 0.0227, 0.9691629955947135, -0.01360317637091654), 'K': (1547402, 0.064, 0.0582, 1.0996563573883162, 0.041256989333998725), 'M': (642753, 0.026, 0.0241, 1.0788381742738589, 0.032956305395949556), 'L': (2794992, 0.115, 0.0965, 1.1917098445595855, 0.07617052700981912), 'N': (916269, 0.038, 0.0406, 0.935960591133005, -0.028742436960383918), 'Q': (1098361, 0.045, 0.0393, 1.1450381679389312, 0.05881996339991694), 'P': (509355, 0.021, 0.0472, 0.44491525423728817, -0.35172270390016847), 'S': (1298566, 0.053, 0.0659, 0.8042488619119879, -0.09460954499322081), 'R': (1427259, 0.059, 0.0553, 1.0669077757685352, 0.02812688033744592), 'T': (1180051, 0.049, 0.053399999999999996, 0.9176029962546818, -0.037345177000042695), 'W': (337622, 0.014, 0.0109, 1.2844036697247707, 0.1087015377376144), 'V': (1505317, 0.062, 0.0687, 0.9024745269286755, -0.04456504756129653), 'Y': (795511, 0.033, 0.0292, 1.13013698630137, 0.05313108842946921)}


d4_rounded = {i: (d4_[i][0], d4_[i][1], round(d4_[i][2], 3), round(d4_[i][3], 3), round(d4_[i][4], 3),) for i in d4_}


# if 1:
#     needed_dir = 'contacts_BA'
#     needed_dir = 'contacts'
#     needed_contacts = cP.load (open ('needed_contacts_%s.cP' % needed_dir, 'rb'))
#     #print len (needed_contacts)
    

# if 1:
#     compressed_hh_contacts = cP.load (open ('compressed_hh_contacts.cP' , 'rb'))


def scoreMatchedSeq (matchedSeq, contacts = [0], aaScore = d4_, divisor = 1.0):
    score = sum ([aaScore.get (aa, (0., 0.))[-1] for aa in matchedSeq])
    normalizsedScore = score / (divisor or 1.0)
    return round (normalizsedScore, 3), round (score, 3), 100.0 - np.mean (contacts)

def parseLine (line, lenOfPattern, matchedPattern):
    '4xr7_J_1_544_561 TTLLTDLGYLFDMMERSH 10 208869'
    #print matchedPattern
    split_line = line.split ()
    split_0_line = split_line [0].split ('_')
    start_of_full_helix, end_of_full_helix = int (split_0_line [3]), int (split_0_line [4])
    
    seq = split_line [1]
    start = int (split_line [2])
    stop = start + lenOfPattern
    
    index_in_db = int (split_line [3])
    
    try:
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
    """"""
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
                print shortSeq
                print possitionsProcessed
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
    '''
    for index, item in enumerate (raw_output_seg_native[0]):
        print index, item
    
    0 ('F0D2E2H', ['F', 0, 'D', 2, 'E', 1, 'D', 2, 'E', 2, 'H'], 8)
    1 [(0.045, 0.36), ('4xr7', 'J', 1, 544, 561), 'TTLLTDLGYLFDMMERSH', 10, 208869, 'F0D2E2H', 'FDMMERSH', 'TTLLTDLGYL<span class="sh_1"><span class="dh_1">FD</span>MM<span class="dh_1">E</span>RS<span class="dh_1">H</span></span>']
    2 [(0.045, 0.36), ('4q8g', 'B', 1, 545, 561), 'TLLTDLGYLFDMMERSH', 9, 512149, 'F0D2E2H', 'FDMMERSH', 'TLLTDLGYL<span class="sh_1"><span class="dh_1">FD</span>MM<span class="dh_1">E</span>RS<span class="dh_1">H</span></span>']
    3 [(0.045, 0.36), ('4q8h', 'A', 1, 544, 561), 'TTLLTDLGYLFDMMERSH', 10, 1591817, 'F0D2E2H', 'FDMMERSH', 'TTLLTDLGYL<span class="sh_1"><span class="dh_1">FD</span>MM<span class="dh_1">E</span>RS<span class="dh_1">H</span></span>']
    '''
    cP.dump (raw_output_seg_native, open ('%s.raw_output_seg_native' % jobId, 'wb'), -1)
    
    sorted_results = generateSortedResults (raw_output_seg_native)
    '''
    for each_result in sorted_results:
        print each_result
    
    [(0.067, 0.601), ('4oh7', 'B', 1, 285, 306), 'VVFDEAENRLHAQKAILAWCLQ', 2, (287, 296), 45615, 'F0D2E3H', 'FDEAENRLH', 'VV<span class="sh_1"><span class="dh_1">FD</span>EA<span class="dh_1">E</span>NRL<span class="dh_1">H</span></span>AQKAILAWCLQ']
    [(0.067, 0.601), ('4oh7', 'A', 1, 285, 306), 'VVFDEAENRLHAQKAILAWCLQ', 2, (287, 296), 45605, 'F0D2E3H', 'FDEAENRLH', 'VV<span class="sh_1"><span class="dh_1">FD</span>EA<span class="dh_1">E</span>NRL<span class="dh_1">H</span></span>AQKAILAWCLQ']
    [(0.066, 0.593), ('4wsb', 'C', 1, 110, 127), 'HYPRVYKMYFDRLERLTH', 9, (119, 128), 267961, 'F0D2E3H', 'FDRLERLTH', 'HYPRVYKMY<span class="sh_1"><span class="dh_1">FD</span>RL<span class="dh_1">E</span>RLT<span class="dh_1">H</span></span>']
    ...
    ...
    [(0.045, 0.36), ('4q8g', 'B', 1, 545, 561), 'TLLTDLGYLFDMMERSH', 9, (554, 562), 512149, 'F0D2E2H', 'FDMMERSH', 'TLLTDLGYL<span class="sh_1"><span class="dh_1">FD</span>MM<span class="dh_1">E</span>RS<span class="dh_1">H</span></span>']
    
    
    0 (0.053, 0.473)
    1 ('1duv', 'I', 1, 311, 332)
    2 IVFDQAENRMHTIKAVMVATLS
    3 2
    4 (313, 322)
    5 312019
    6 F0D2E3H
    7 FDQAENRMH
    8 IV<span class="sh_1"><span class="dh_1">FD</span>QA<span class="dh_1">E</span>NRM<span class="dh_1">H</span></span>TIKAVMVATLS
    '''
    cP.dump (sorted_results, open ('%s.sorted_results' % jobId, 'wb'), -1)
    
    return sorted_results, raw_output_seg_native
    

def genHtmlTable (sorted_results):
    '''
    <table>
      <tr>
        <th>Month</th>
        <th>Savings</th>
      </tr>
      <tr>
        <td>January</td>
        <td>$100</td>
      </tr>
      <tr>
        <td>February</td>
        <td>$80</td>
      </tr>
    </table>
    '''
    
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
            #                                                PDB ID          CHAIN         start_end_pair
            helical_contact_info = compressed_hh_contacts [entry [1][0]] [entry [1][1]] [(entry [1][3], entry [1][4])]
            #       id   chain  start end id_j
            # --> [['1', 'F', 220, 223, '5'], ['1', 'F', 292, 306, '1']]
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
        
    return '<span class="monospace"><table id="results1">%s</table></span>' % output






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



example_query = 'A/E 0,4 D 2,3 E 2,3 H' #"A(0,4)D(2,3)E(2,3)H"



'''
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

def make_app():
    return tornado.web.Application([
           (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8111)
    tornado.ioloop.IOLoop.current().start()
helixdb.py (END) 


'''

#Modified by Yu-Lin
portToUse = 15153
homeUrl = 'http://localhost:{}'.format(portToUse)
    


import time, signal, logging, json, os, cPickle as cP, urlparse, copy, chardet, string, cgi, random, subprocess, math, glob, requests
import tornado.httpserver, tornado.ioloop, tornado.options, tornado.web#, csscompressor
from tornado.options import define, options
#from mailer import Mailer; from mailer import Message


emptyFormater = {str (i):'' for i in range (10)}


define("port", default=portToUse, help="run on the given port", type=int)
MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 3


d1 = {'Allow': 'GET, HEAD, POST', 'Content-Type': 'text/html; charset=utf-8'}
d2 = {'Allow': 'GET, HEAD, POST', 'Content-Type': 'application/json; charset=utf-8'}
d3 = {'Allow': 'GET, HEAD, POST', 'Content-Type': 'text/xml, application/xml; charset=utf-8'}
d4 = {'Allow': 'GET, HEAD, POST', 'Content-Type': 'application/pdf', #'Connection':'close', 'Content-Transfer-Encoding': 'binary',
      #'Accept-Ranges':'none', 'Cache-Control':'no-cache', 'Transfer-Encoding':'chunked', 
      }
d5 = {'Allow': 'GET, HEAD, POST', 'Content-Type': 'text/plain; charset=utf-8'}
d6 = {'Allow': 'GET, HEAD, POST', 'Content-Type': 'image/png'}



def genEffectiveDict (theDict):
    neededDict = {}
    for key in theDict:
        if isinstance (theDict [key], list):
            if len (theDict [key]) > 1: value = theDict [key]
            else: value = theDict [key][0]
        else: value = theDict [key]
        if value: neededDict [key] = value
    return neededDict


try:
    len (seq_map)
except:
    seq_map = {}

def load_seq_map (reload_seq_map = False):
    
    if (len (seq_map) > 0) and (not reload_seq_map):
        return
    else:
        seqs = [i.strip() for i in open ("sequences_helix_corrected_dec292017.fasta").readlines ()]
        
        for line in seqs:
            if line.startswith (">"):
                key = line.strip ("> ")
                seq_map [key] = []
            else:
                seq_map [key].append (line)
            

def format_alignment (query, subject, q_start, q_end, s_start, s_end, hsp_match, sub_start_end_in_pdb, html=False):
    """
    'GAIAAIMQKG'
    'WDEFAKGAVRAIMQAG'
    7 16 1 10
    <pre>
    """
    
#    query = 'GAIAAIMQKG'
#    subject = 'WDEFAKGAVRAIMQAG'
#    q_start, q_end, s_start, s_end =  1, 10, 7, 16,
#    hsp_match = "GA+ AIMQ G"
    
    max_padding = max (s_start - 1, q_start - 1,) + 6
    
    padded_query = " " * (max_padding - (q_start - 1)) + query
    padded_subject = " " * (max_padding - (s_start - 1) - 6) +  sub_start_end_in_pdb [0].rjust (4) + "  " + subject + "  " + sub_start_end_in_pdb [1] 
    padded_hsp_match = " " * (max_padding ) + hsp_match
    
    if html:
        formatted_result = "<pre>%s\n%s\n%s</pre>" % (padded_query, padded_hsp_match, padded_subject)
    else:
        formatted_result = "%s\n%s\n%s" % (padded_query, padded_hsp_match, padded_subject)
    
    return formatted_result, (padded_query, padded_hsp_match, padded_subject)
    

htmlHeader = '''<head> 

<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script>

<style>
.sh_1 {color: blue;}
.dh_1 {font-weight: 900;}
.monospace {font-family: "Courier New", Courier, monospace; font-size: 80%; }
td {font-size: 80%; }
</style>

<script>
$(document).ready(function()
{
  $("table#results1 tr:even").css("background-color", "#F4F4F8");
  $("table#results1 tr:odd").css("background-color", "#EFF1F1");
  
  //$("table#id2 tr:even").css("background-color", "#F4F4F8");
  //$("table#id2 tr:odd").css("background-color", "#EFF1F1");


    $( "#toggleUniqueSequences" ).click(function() {
      $( ".not_unique" ).toggle();
    });

});

</script>

</head>''' 


def genHtmlTableBlast (alignments, query_seq, ):
    
    
    table_headers = ['#', 'U#', 'Alignment<br>-Query-<br>+Match+<br>Subject', 'PDB ID:<br>Chain', 'Alignment<br>Score',
                        ] #'View Helix in 3D', ]
    
    output = '<tr>%s</tr>' % (''.join (['<th>%s</th>' % i for i in table_headers]), )
    
    uniqueness = set ([])
    
    for index, alignment in enumerate (alignments):
        subject = "".join (seq_map [alignment.hit_def] )
        subject_info = alignment.hit_def.split("_"); print subject_info
        
        seq = subject
        if seq in uniqueness:
            unique = 'not_unique'
        else: 
            uniqueness.add (seq)
            unique = 'unique'
        
        hsps = alignment.hsps 
        
        for hsp in hsps: 
            q_start, q_end, s_start, s_end, hsp_match = hsp.query_start, hsp.query_end, hsp.sbjct_start, hsp.sbjct_end, hsp.match
            
            formatted_result, (padded_query, padded_hsp_match, padded_subject) = \
                format_alignment (query_seq, subject, q_start, q_end, s_start, s_end, hsp_match, subject_info [-2:], html=True)
            
            
            table_row = [str (index + 1), str (len (uniqueness)), formatted_result, "%s:%s"% (subject_info [0], subject_info [1]), hsp.score
                        ]
            output += '<tr class="%s">%s</tr>' % (unique, ''.join (['<td>%s</td>' % i for i in table_row]), )
        
    return '<span class="monospace"><table id="results1">%s</table></span>' % output

        
    

from pprint import pprint as pp
class MainHandler(tornado.web.RequestHandler):
    
    def get (self, *pargs_, **kwargs):
        insertInCenDiv = kwargs.get ('insertInCenDiv', copy.copy (emptyFormater))
        pargs = tuple ((i for i in pargs_ if i))
        #print 1, insertInCenDiv
        numArgs = len (pargs); xpctdMaxNumOfArgs = 11
        arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11 = (pargs + ((None,) * abs (xpctdMaxNumOfArgs - numArgs)))[:xpctdMaxNumOfArgs]
        print arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11
        originalUrl = '/' + '/'.join ([thisArg for thisArg in [arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11] if (isinstance (thisArg, str) or isinstance (thisArg, unicode))])
        
        specialMessage = kwargs.get ('specialMessage', '')
        url = '/' + '/'.join ([thisArg for thisArg in [arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11] if (isinstance (thisArg, str) or isinstance (thisArg, unicode))])
        #self.totalPageVisit += 1; totalPageVisit = self.totalPageVisit; group = None; 
        title = ''
        
        pageToRender = ''
        print arg1, arg2, arg3, arg4, arg5, arg6, arg7
        
        if not arg1: arg1 = 'home'
        
        if (arg1 and ('result' in arg1) and arg2) or (arg2 and ('result' in arg2) and arg3):
            if 'result' in arg1:
                jobId = arg2
            elif 'result' in arg2:
                jobId = arg3
                
            raw_result_file = 'result/%s/%s.output' % (jobId, jobId, )
            jobIdWithPath = 'result/%s/%s' % (jobId, jobId, )
            
            #if True:
            try:
                raw_result = open (raw_result_file).read ()
                processed_raw_result = raw_result.replace ('>', '<br>&gt;').replace ('\n', '<br>')
                submittedQuery = open ('%s.submitted' % (jobIdWithPath,)).read ()
                if True:
#                try:
                    try:
                        sorted_results = cP.load (open ('%s.sorted_results' % jobIdWithPath, 'rb'))
                        print "Loaded sorted results from file"
                    except:
                        print "Trying to compute sorted results"
                        sorted_results, raw_output_seg_native = process_output (raw_result, jobIdWithPath)
                    
                    html_table = genHtmlTable (sorted_results)
                    URL = '%s/result/%s' % (homeUrl, jobId)
                    permUrl = '<a href="%s">%s</a>' % (URL, URL)
                    
                    processed_raw_result = '''<html>%s<body>Result for Job: %s<br/><br/>Submitted Query: %s<br/>Permanent URL: %s<br/><br/>
                    <div id="toggleUniqueSequences">Unique (U) Matched Sequences [click here to toggle]</div><br/>
                    %s</body></html>''' \
                        % (htmlHeader, jobId, submittedQuery, permUrl, html_table, )
                    
                else:
#                except Exception as excp:
#                    print excp
                    pass
                
                
            #else:
            except:
                processed_raw_result = 'Pending. Refresh this page in one minute. Something might be wrong with your query if the results is not displayed in more than 2 minutes. If you wish to email us, please, include the URL of this result page in such email. Thank you.'
            
            pageToRender += specialMessage + '<br>Results<br><br>%s' % (processed_raw_result, )
        
        #BLAST
        elif (arg1 and ('blast' in arg1) and '<REMOVE>arg2') or (arg2 and ('blast' in arg2) and '<REMOVE>arg3'):
            if 'blast' in arg1:
                jobId = arg2
            elif 'blast' in arg2:
                jobId = arg3
            
            if not jobId: #show the input/SUBMIT page 
                another_example_query = 'WDEFAKGVRAMQG'
                pageToRender += specialMessage + '''<br/><br/><form method="POST" enctype="multipart/form-data">
  Query Sequence<br>
  <input type="text" name="query_string"><br>Examples: GAIAAIMQKG <br> %s <br><br>
  Email Address (Optional)<br>
  <input type="email" name="emailAddress">
  <br/> <br><br>
  <button type="submit" value="query2" name="query_button" id="query_button">Submit</button>
</form>''' % (another_example_query, )
        
            
            else: #show the RESULT page 
                #raw_result_file = 'blast/%s/%s.output' % (jobId, jobId, )
                jobIdWithPath = 'blast/%s/%s' % (jobId, jobId, )
                query_seq = open ('%s.que' % jobIdWithPath).read ().strip ().strip (">")
                load_seq_map ()
                
                try:
                    blast_record = cP.load (open ("%s_.blast_record.cP" % jobIdWithPath, "rb"))
                
                except:
                    cline = NcbiblastpCommandline (query = '%s.que' % jobIdWithPath, db = "sequences_helix_corrected", #strand="plus",
                                                   out = "%s_.xml" % jobIdWithPath, outfmt = 5, word_size = 4, evalue = 200,)# gapopen=60, gapextend=60,)
                                                   #min_raw_gapped_score=8)
                    cline (  )
                    
                    blast_record = NCBIXML.read (open ("%s_.xml" % jobIdWithPath)) 
                    cP.dump (blast_record, open ("%s_.blast_record.cP" % jobIdWithPath, "wb"), -1)
                    
                alignments = blast_record.alignments 
                
                
                html_table = genHtmlTableBlast (alignments, query_seq, )
                
                URL = '%s/blast/%s' % (homeUrl, jobId)
                permUrl = '<a href="%s">%s</a>' % (URL, URL)
                
                processed_raw_result = '''<html>%s<body>Result for Job: %s<br/><br/>Submitted Query: %s<br/>Permanent URL: %s<br/><br/>
                <div id="toggleUniqueSequences">Unique (U) Matched Sequences [click here to toggle]</div><br/>
                %s</body></html>''' \
                    % (htmlHeader, jobId, query_seq, permUrl, html_table, )
                    
#                
#                for alignment in alignments: 
#                    subject = "".join (seq_map [alignment.hit_def] )
#                    subject_info = alignment.hit_def.split("_")
#                    print subject_info
#                    "\n\nAlignment", jobIdWithPath 
#                    #print alignment.hit_def, subject
#                    hsps = alignment.hsps 
#                    for hsp in hsps: 
#                        #if hsp.sbjct_end + hsp.query_start - 1 != len_seq_str: 
#                        #    continue
#            #            print hsp.score
#            #            print hsp.sbjct
#            #            print hsp.match
#            #            end_of_top = hsp.match.find (' ')
#            #            start_of_bottom = hsp.match.rfind (' ')
#            #            if end_of_top != -1:
#            #                end_of_top -= 1
#            #                start_of_bottom += 1
#            #            else:
#            #                end_of_top = len(hsp.sbjct)//2 -1 
#            #                start_of_bottom = end_of_top + 1
#            #            print hsp.query
#            #            print hsp.sbjct_start,
#            #            print hsp.sbjct_end,
#            #            print hsp.query_start,
#            #            print hsp.query_end
#                        #print end_of_top, start_of_bottom
#                        #genHairpin (hsp.sbjct, end_of_top, start_of_bottom, pos1=hsp.sbjct_start, pos2=hsp.sbjct_end)
#                        #print; print 
#                        q_start, q_end, s_start, s_end, hsp_match = hsp.query_start, hsp.query_end, hsp.sbjct_start, hsp.sbjct_end, hsp.match
#                        
#                        formatted_result, (padded_query, padded_hsp_match, padded_subject) = \
#                            format_alignment (query_seq, subject, q_start, q_end, s_start, s_end, hsp_match, subject_info [-2:], html=True)
#                        print formatted_result
#                        
#                        print "-------------------"
#            

                
#                except:
#                    processed_raw_result = 'Pending. Refresh this page in one minute. Something might be wrong with your query if the results is not displayed in more than 2 minutes. If you wish to email us, please, include the URL of this result page in such email. Thank you.'
                
                pageToRender += specialMessage + '<br>Results<br><br>%s' % (processed_raw_result, )
            
                
            
        else:
            pageToRender += specialMessage + '''<br/><br/><form method="POST" enctype="multipart/form-data">
  Query String<br>
  <input type="text" name="query_string"><br>Examples: A 2 D 3 E 2 H <br> %s <br><br>
  Email Address (Optional)<br>
  <input type="email" name="emailAddress">
  <br/> <br><br>
  <button type="submit" value="query1" name="query_button" id="query_button" >Submit</button>
</form>''' % (example_query, )
        
        
        
        for key_ in d1: self.set_header (key_, d1 [key_])
        #self.write('<html><br /><br />page2</html>')
        self.write (pageToRender)
        
        
        
    def post (self, *pargs, **kwargs):
        try:insertInCenDiv 
        except: insertInCenDiv = copy.copy (emptyFormater)
        numArgs = len (pargs); xpctdMaxNumOfArgs = 11
        arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11 = (pargs + ((None,) * abs (xpctdMaxNumOfArgs - numArgs)))[:xpctdMaxNumOfArgs]
        
        #pp (self.request.headers['Content-Type']); #pp (arg1); pp (arg2); pp (arg3); pp (self)
        """print dir (self.request)
        ['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_finish_time', '_start_time', 'arguments', 'body', 'connection', 'cookies', 'files', 'finish', 'full_url', 'get_ssl_certificate', 'headers', 'host', 'method', 'path', 'protocol', 'query', 'remote_ip', 'request_time', 'supports_http_1_1', 'uri', 'version', 'write']
        """
        submittedData = {}; submittedFiles = {} #boundary=
        contentType = self.request.headers.get('Content-Type', '')
        #print contentType
        
        
        if 'multipart/form-data' in contentType:
            tornado.httputil.parse_multipart_form_data (contentType.split('boundary=')[-1], self.request.body, submittedData, submittedFiles)
        else:
            try: submittedData = json.loads (self.request.body); 
            except Exception as e1: 
                print e1; print
                try: submittedData = urlparse.parse_qs (self.request.body)
                except Exception as e2: print e2; #submittedData = {}; 
        submittedData = genEffectiveDict (submittedData)
        
        
        specialMessage = "We are sorry but we could not confirm if that request was successful or not. <br />"
        submittedButton = submittedData.get ('query_button', ' ')
        print submittedData
        
        if submittedButton == 'query1':
            specialMessage = ''# "Thank you. Your attempt appears successful! <br />"
            expectedParams = {'query_string'}
            expectedParamsLabels = {"query": "Query", "firstName": "First Name", "lastName": "Last Name", "reenterPassword": '"Password Again/Re-Enter Password Field"', "emailAddress": 'Email Address', "password": 'Password'}
            submittedParams = set (submittedData.keys ())
            if expectedParams.issubset (submittedParams):
                query_string = submittedData ['query_string']
                
                jobId = hex(int (time.time ())) [2:] + random.choice (string.ascii_lowercase)
                workingDir = 'result/%s' % jobId
                mainOutputFile = 'result/%s/%s' % (jobId, jobId)
                os.makedirs (workingDir); 
                
                mainQueryDb (query=query_string, outputFileName=mainOutputFile)
                specialMessage = 'Result will be available <a href="%(link)s">here</a> [<a href="%(link)s">%(link)s</a>] in about one minute.<br/>' % {'link': '%s/%s' % (homeUrl, workingDir)}
        
        
        elif submittedButton == 'query2':
            specialMessage = ''# "Thank you. Your attempt appears successful! <br />"
            expectedParams = {'query_string'}
            expectedParamsLabels = {"query": "Query", "firstName": "First Name", "lastName": "Last Name", "reenterPassword": '"Password Again/Re-Enter Password Field"', "emailAddress": 'Email Address', "password": 'Password'}
            submittedParams = set (submittedData.keys ())
            if expectedParams.issubset (submittedParams):
                query_string = submittedData ['query_string']
                
                jobId = hex(int (time.time ())) [2:] + random.choice (string.ascii_lowercase)
                workingDir = 'blast/%s' % jobId
                mainInputFile = 'blast/%s/%s.que' % (jobId, jobId) #'%s.que' % jobIdWithPath
                os.makedirs (workingDir); 
                with open (mainInputFile, "w") as input_que:
                    input_que.write (query_string)
                #mainBlast (query=query_string, outputFileName=mainOutputFile)
                specialMessage = 'The results should be avilable here <a href="%(link)s">here</a> [<a href="%(link)s">%(link)s</a>] in a few seconds.<br/>' % {'link': '%s/%s' % (homeUrl, workingDir)}
        
        
        self.logData (submittedData)
        self.get (arg1, arg2, arg3, specialMessage=specialMessage, insertInCenDiv=insertInCenDiv)


    def logData (self, submittedData):
        with open (time.strftime ("subscriptions/%y%m%d", time.gmtime()), "a") as fileForToday:
            try: fileForToday.write (json.dumps(submittedData) + ' %s \n' % self.request.remote_ip)
            except Exception as e: print e; pp (self.request.body)
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
def sig_handler(sig, frame):
    logging.warning('Caught signal: %s', sig)
    tornado.ioloop.IOLoop.instance().add_callback(shutdown)

        
totalPageVisit = 200
def shutdown():
    with open ('totalPageVisit.txt', 'w') as pageVisitFile: pageVisitFile.write (str(totalPageVisit));
    logging.info ('Stopping http server')
    server.stop ()
    logging.info ('Will shutdown in %s seconds ...', MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)
    io_loop = tornado.ioloop.IOLoop.instance()
    deadline = time.time() + MAX_WAIT_SECONDS_BEFORE_SHUTDOWN
    def stop_loop():
        now = time.time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout (now + 1, stop_loop)
        else:
            io_loop.stop ()
            logging.info ('Shutdown')
    stop_loop()

def main():
    tornado.options.parse_command_line ()
    settings = {
                #"static_path": os.path.join(os.path.dirname(__file__), "static"),
                "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
                "login_url": "/login",
                "xsrf_cookies": False,
                'gzip':True,
                }
    application = tornado.web.Application([
                (r"/(favicon.ico)", tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), "static/img")},),
                (r"/(robots.txt)", tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), "static")},),
                #(r"/people/cover_picture/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), "people/cover_picture")},),
                #(r"/people/profile_picture/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), "people/profile_picture")},),
                (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), "static")},),
                (r"/manuscript_file/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), "manuscript_file")},),
                (r"/(checkData.*)", MainHandler),
                (r"/(.*)/(.*)/(.*)/(.*)/(.*)/(.*)/(.*)/(.*)/(.*)", MainHandler),
                (r"/(.*)/(.*)/(.*)/(.*)/(.*)/(.*)/(.*)/(.*)", MainHandler),
                (r"/(.*)/(.*)/(.*)/(.*)/(.*)/(.*)/(.*)", MainHandler),
                (r"/(.*)/(.*)/(.*)/(.*)/(.*)/(.*)", MainHandler),
                (r"/(.*)/(.*)/(.*)/(.*)/(.*)", MainHandler),
                (r"/(.*)/(.*)/(.*)/(.*)", MainHandler),
                (r"/(.*)/(.*)/(.*)", MainHandler),
                (r"/(.*)/(.*)", MainHandler),
                (r"/(.*)", MainHandler),
                (r"/", MainHandler),
                #(r"/api", ApiHandler),
                ], **settings
                )

    global server, totalPageVisit
    server = tornado.httpserver.HTTPServer(application)
    server.listen(options.port)
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)
    tornado.ioloop.IOLoop.instance().start()
    logging.info("Exit...")
    
    
    
    







if __name__ == "__main__":
    main()





#
