#|
Check paths created from execution of
  (WITH-CHECK-PATH-LIST-COLLECTION "~/Documents/grammars/srg/lkb/c.lsp" (PARSE-SENTENCES "~/Documents/grammars/srg/lkb/an07-50.txt" T))
with grammar SRG1007 on 3-4-2023 (11:43:48)
|#
(CL:IN-PACKAGE #:LKB)
(DEFPARAMETER *CHECK-PATHS*
  '(((SYNSEM LOCAL CAT VAL COMPS) . 1436541)
    ((SYNSEM LOCAL CAT HEAD) . 832823)
    ((SYNSEM LOCAL CAT HEAD LSYNSEM) . 590746)
    (NIL . 422469)
    ((SYNSEM LOCAL CAT VAL CLTS) . 343526)
    ((SYNSEM LOCAL CAT HEAD MOD) . 246142)
    ((SYNSEM LOCAL CAT VAL CLTS FIRST LOCAL CAT HEAD CASE) . 182648)
    ((SYNSEM LOCAL CAT VAL SUBJ) . 147490)
    ((SYNSEM NON-LOCAL SLASH LAST) . 102091)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST LOCAL CAT HEAD) . 80443)
    ((SYNSEM NON-LOCAL SLASH) . 64012)
    ((SYNSEM LOCAL CAT HEAD VFORM) . 54475)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST) . 47740)
    ((SYNSEM) . 42199)
    ((SYNSEM NON-LOCAL SLASH LIST) . 39373)
    ((SYNSEM LOCAL COORD-STRAT) . 34592)
    ((SYNSEM LOCAL CAT MC) . 32853)
    ((SYNSEM LOCAL CAT HEAD KEYS KEY) . 29408)
    ((SYNSEM SLSHD) . 26339)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST LOCAL CAT HEAD KEYS KEY) . 22022)
    ((SYNSEM NON-LOCAL REL) . 21100)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD) . 13042)
    ((SYNSEM LOCAL CAT VAL COMPS REST) . 12703)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST NON-LOCAL SLASH LIST) . 11014)
    ((SYNSEM LOCAL CAT VAL CLTS REST) . 9906)
    ((SYNSEM PUNCT RPUNCT) . 9020)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST LOCAL CAT MC) . 7364)
    ((SYNSEM LOCAL CAT HEAD MOD FIRST LOCAL CAT HEAD) . 7333)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT HEAD LSYNSEM) . 6929)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST OPT) . 6390)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST NON-LOCAL SLASH LAST) . 6079)
    ((SYNSEM NON-LOCAL QUE) . 6069)
    ((SYNSEM LOCAL CAT VAL SPR) . 5400)
    ((SYNSEM NON-LOCAL QUE LAST) . 4547)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST LOCAL) . 4152)
    ((SYNSEM LOCAL CONT HOOK INDEX) . 3863)
    ((SYNSEM LOCAL STR HEADED) . 3449)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST LOCAL CAT HEAD) . 3054)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST NON-LOCAL SLASH LAST) . 3000)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD) . 2899)
    ((SYNSEM LOCAL COORD-REL PRED) . 2748)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST NON-LOCAL SLASH LAST FIRST) . 2516)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST LOCAL COORD) . 2332)
    ((SYNSEM LOCAL CONT HOOK INDEX SORT) . 2194)
    ((SYNSEM LOCAL CAT HEAD TAM MOOD) . 2002)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS FIRST MODIFIED) . 1899)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST NON-LOCAL SLASH LIST) . 1833)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD KEYS KEY) . 1788)
    ((SYNSEM MODIFIED) . 1667)
    ((SYNSEM LOCAL CAT HEAD CLIT) . 1596)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST LOCAL CAT VAL SPR) . 1550)
    ((SYNSEM LOCAL CONT HOOK XARG) . 1281)
    ((SYNSEM LOCAL AGR PNG PN) . 1261)
    ((SYNSEM LOCAL CAT HEAD MOD FIRST LOCAL) . 1224)
    ((SYNSEM LOCAL COORD) . 1129)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST LOCAL) . 1074)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD KEYS ALT2KEY) . 966)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST LOCAL CAT VAL COMPS) . 900)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT HEAD) . 884)
    ((SYNSEM LOCAL CAT HEAD VOICE) . 727)
    ((SYNSEM LOCAL CAT POSTHEAD) . 711)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST NON-LOCAL SLASH LAST FIRST CAT HEAD) . 696)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS FIRST LOCAL CAT HEAD LSYNSEM) . 647)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT VAL SUBJ) . 613)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST LOCAL CONT HOOK INDEX) . 575)
    ((SYNSEM LOCAL CAT VAL CLTS REST FIRST LOCAL CAT HEAD CASE) . 540)
    ((SYNSEM LOCAL AGR SF) . 518)
    ((SYNSEM LOCAL AGR) . 504)
    ((INFLECTED) . 492)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST) . 469)
    ((SYNSEM LOCAL CAT HEAD MOD FIRST LOCAL CAT VAL SPR) . 463)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST LOCAL CONT HOOK XARG) . 455)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT POSTHEAD) . 443)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST NON-LOCAL SLASH) . 440)
    ((SYNSEM LOCAL CAT VAL SPR FIRST OPT) . 427)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL SUBJ FIRST NON-LOCAL SLASH LAST FIRST CAT VAL SUBJ) . 426)
    ((SYNSEM NON-LOCAL REL LAST) . 409)
    ((SYNSEM LOCAL CAT HEAD PRD) . 405)
    ((SYNSEM LOCAL CONT HOOK INDEX E TENSE) . 342)
    ((SYNSEM LOCAL CAT VAL CLTS FIRST LOCAL AGR SORT) . 338)
    ((SYNSEM LOCAL CAT HEAD LEFT) . 304)
    ((SYNSEM LOCAL AGR E TENSE) . 304)
    ((SYNSEM LOCAL CONT HOOK INDEX PRONTYPE) . 302)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST LOCAL CAT HEAD MOD FIRST LOCAL CAT HEAD) . 298)
    ((SYNSEM NON-LOCAL QUE LIST) . 295)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS FIRST LOCAL STR HEADED) . 292)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CONT HOOK INDEX E TENSE) . 291)
    ((SYNSEM LOCAL CAT VAL CLTS FIRST LOCAL AGR PNG PN) . 244)
    ((ALTS IMPERS) . 240)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST NON-LOCAL SLASH LAST FIRST CONT HOOK INDEX E TENSE) . 228)
    ((SYNSEM LOCAL CAT VAL COMPS REST FIRST LOCAL) . 228)
    ((SYNSEM LOCAL CONT HOOK INDEX SF) . 221)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST LOCAL AGR) . 218)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST LOCAL CONT HOOK INDEX SORT) . 216)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT VAL SPR) . 207)
    ((SYNSEM LOCAL CAT HEAD KEYS) . 191)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST LOCAL CONT HOOK INDEX) . 186)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST LOCAL CONT HOOK INDEX E TENSE) . 183)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT VAL CLTS FIRST LOCAL AGR PRONTYPE) . 157)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL CLTS FIRST LOCAL AGR PRONTYPE) . 153)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CONT HOOK INDEX SORT) . 151)
    ((SYNSEM LOCAL CAT HEAD LSYNSEM LOCAL CAT VAL COMPS REST) . 149)
    ((SYNSEM LOCAL CAT HEAD MOD FIRST LOCAL CAT HEAD KEYS KEY) . 148)
    ((SYNSEM LOCAL CAT VAL COMPS REST FIRST LOCAL CAT MC) . 145)
    ((SYNSEM PUNCT LPUNCT) . 143)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL SUBJ FIRST MODIFIED) . 138)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CONT HOOK XARG SORT) . 134)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST LOCAL CAT HEAD VFORM) . 134)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST LOCAL AGR PNG PN) . 133)
    ((SYNSEM LOCAL CAT HEAD INV) . 133)
    ((SYNSEM LOCAL CAT HEAD TAM TENSE) . 130)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST LOCAL CONT HOOK XARG SORT) . 127)
    ((SYNSEM LOCAL CAT HEAD KEYS ALTKEY) . 124)
    ((SYNSEM LOCAL CAT VAL COMPS REST FIRST LOCAL CONT HOOK XARG) . 114)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT HEAD KEYS ALT2KEY) . 112)
    ((ALTS RFX) . 111)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS REST FIRST) . 111)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST NON-LOCAL SLASH LAST FIRST) . 107)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST NON-LOCAL SLASH LIST FIRST) . 105)
    ((ALTS RCP) . 104)
    ((SYNSEM LKEYS KEYREL) . 101)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST OPT) . 92)
    ((SYNSEM LOCAL CAT VAL SPEC) . 86)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST NON-LOCAL SLASH LAST FIRST CAT HEAD MOD FIRST LOCAL CAT POSTHEAD) . 82)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST NON-LOCAL REL LIST) . 81)
    ((SYNSEM LOCAL AGR DIVISIBLE) . 75)
    ((SYNSEM LOCAL CAT HEAD PUNCT-MK) . 73)
    ((SYNSEM LOCAL CAT HEAD LSYNSEM LOCAL CAT VAL COMPS FIRST LOCAL CAT HEAD LSYNSEM) . 72)
    ((C-CONT HOOK XARG SORT) . 72)
    ((SYNSEM LOCAL CONT RELS LIST FIRST PRED) . 70)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT VAL CLTS) . 70)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL SUBJ FIRST LOCAL CAT HEAD LSYNSEM) . 67)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST NON-LOCAL SLASH LAST FIRST CAT HEAD MOD FIRST LOCAL CAT HEAD LSYNSEM) . 67)
    ((SYNSEM LOCAL CONT HOOK INDEX PNG PN) . 64)
    ((SYNSEM LOCAL CAT VAL COMPS REST FIRST NON-LOCAL SLASH LAST) . 64)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS REST FIRST LOCAL CONT HOOK XARG SORT) . 62)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL SUBJ FIRST NON-LOCAL SLASH LIST) . 59)
    ((SYNSEM LKEYS ALTKEYREL PRED) . 57)
    ((SYNSEM LOCAL CONT HOOK XARG PNG PN) . 56)
    ((SYNSEM LOCAL CAT VAL SPEC FIRST LOCAL CAT HEAD) . 54)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS FIRST NON-LOCAL SLASH LIST FIRST CAT HEAD KEYS KEY) . 52)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CONT HOOK XARG DEF) . 52)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST LOCAL CAT HEAD KEYS ALT2KEY) . 52)
    ((SYNSEM LKEYS KEYREL PRED) . 51)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST LOCAL CAT HEAD KEYS ALTKEY) . 48)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST COORD) . 47)
    ((SYNSEM LOCAL CAT VAL CLTS REST FIRST LOCAL AGR PRONTYPE) . 47)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS FIRST LOCAL CAT VAL SPEC) . 44)
    ((SYNSEM LOCAL CONT RELS LIST FIRST) . 44)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS FIRST LOCAL CONT HOOK INDEX) . 43)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST LOCAL CAT VAL SPR) . 42)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT HEAD CASE) . 42)
    ((SYNSEM NON-LOCAL REL LIST) . 42)
    ((SYNSEM LOCAL CAT HEAD LSYNSEM LOCAL CAT VAL COMPS) . 40)
    ((SYNSEM LOCAL CAT HEAD CASE) . 38)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL SUBJ FIRST LOCAL CONT HOOK INDEX SORT) . 38)
    ((SYNSEM LOCAL CAT HEAD MOD FIRST LOCAL AGR SORT) . 37)
    ((SYNSEM LOCAL COORD-REL R-INDEX SF) . 37)
    ((SYNSEM LOCAL CONT RELS LIST FIRST ARG2) . 35)
    ((SYNSEM LOCAL CAT VAL SPR FIRST LOCAL CAT HEAD KEYS KEY) . 35)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS FIRST LOCAL CONT HOOK XARG SORT) . 33)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS FIRST OPT) . 32)
    ((SYNSEM LOCAL CAT VAL SPEC FIRST LOCAL CAT HEAD KEYS ALTKEY) . 31)
    ((SYNSEM LOCAL CAT HEAD MOD FIRST LOCAL AGR) . 28)
    ((SYNSEM LOCAL CAT VAL COMPS REST FIRST LOCAL CONT HOOK INDEX E TENSE) . 28)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST NON-LOCAL REL) . 28)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST NON-LOCAL SLASH LAST FIRST CAT HEAD MOD FIRST LOCAL CAT MC) . 26)
    ((SYNSEM LOCAL CAT HEAD LSYNSEM LOCAL CAT VAL COMPS FIRST NON-LOCAL SLASH LIST) . 25)
    ((SYNSEM LOCAL AGR PRONTYPE) . 25)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL SUBJ FIRST NON-LOCAL SLASH LAST FIRST) . 25)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS FIRST LOCAL CAT VAL SUBJ FIRST LOCAL CAT HEAD VFORM) . 24)
    ((SYNSEM LOCAL CAT VAL SPR FIRST LOCAL CONT HOOK XARG) . 24)
    ((SYNSEM LOCAL CONT HOOK INDEX E MOOD) . 24)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST NON-LOCAL SLASH LAST FIRST CAT HEAD KEYS ALT2KEY) . 23)
    ((ALTS PASS) . 23)
    ((SYNSEM LOCAL CAT VAL COMPS REST FIRST LOCAL CONT HOOK XARG SORT) . 22)
    ((SYNSEM LOCAL CAT HEAD KEYS ALT2KEY) . 22)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST LOCAL CAT VAL SPR FIRST NON-LOCAL REL) . 21)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL SPR FIRST LOCAL AGR PNG GEN) . 21)
    ((SYNSEM LOCAL CAT HEAD MOD FIRST LOCAL CONT HOOK INDEX PNG PN) . 20)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST NON-LOCAL SLASH LAST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL SUBJ FIRST LOCAL AGR PNG PN) . 20)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS REST FIRST SLSHD) . 20)
    ((SYNSEM LOCAL CAT HEAD AUX) . 20)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST NON-LOCAL SLASH LAST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS REST FIRST LKEYS) . 19)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST LOCAL CONT HOOK XARG SORT) . 19)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS FIRST LOCAL CAT HEAD MOD FIRST LOCAL) . 19)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS FIRST SLSHD) . 18)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CONT HOOK INDEX SF) . 18)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD CASE) . 18)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT VAL COMPS) . 18)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS FIRST LOCAL AGR) . 17)
    ((SYNSEM LOCAL STR HEADING) . 17)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST NON-LOCAL SLASH LAST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS FIRST LOCAL CAT VAL SUBJ FIRST LOCAL AGR PNG PN) . 16)
    ((SYNSEM LOCAL CAT LASTNMOD) . 16)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST LOCAL CAT HEAD VFORM) . 16)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST NON-LOCAL SLASH LAST FIRST CAT HEAD MOD FIRST LOCAL CAT HEAD CLIT) . 15)
    ((SYNSEM LOCAL AGR SORT) . 15)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS) . 15)
    ((SYNSEM LOCAL CAT VAL CLTS REST REST) . 14)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS FIRST LOCAL CAT MC) . 14)
    ((SYNSEM LOCAL CONT HOOK XARG PNG GEN) . 14)
    ((C-CONT HOOK XARG DIVISIBLE) . 13)
    ((SYNSEM LOCAL CONT RELS LIST REST FIRST PRED) . 12)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS FIRST NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL SUBJ) . 12)
    ((SYNSEM LOCAL CAT HEAD LSYNSEM LOCAL CAT VAL COMPS FIRST LOCAL CAT VAL SUBJ FIRST NON-LOCAL SLASH LAST FIRST CONT HOOK INDEX E TENSE) . 12)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST NON-LOCAL SLASH LAST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS FIRST MODIFIED) . 12)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CONT HOOK XARG PNG PN) . 12)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS REST FIRST LOCAL STR HEADED) . 12)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL SUBJ FIRST LOCAL AGR PNG PN) . 11)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL SUBJ FIRST) . 11)
    ((SYNSEM LOCAL CAT VAL CLTS FIRST LOCAL CONT HOOK INDEX PRONTYPE) . 11)
    ((SYNSEM LOCAL CONT RELS LIST FIRST ARG0) . 10)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CONT HOOK XARG) . 10)
    ((SYNSEM LOCAL CAT VAL CLTS FIRST OPT) . 10)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST LOCAL CONT HOOK INDEX PRONTYPE) . 9)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST NON-LOCAL SLASH LAST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS REST FIRST) . 9)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CONT HOOK INDEX PNG PN) . 9)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL SUBJ FIRST LOCAL CONT HOOK XARG) . 9)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST AGR PNG PN) . 8)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL SPR FIRST LOCAL CONT) . 8)
    ((SYNSEM NON-LOCAL REL LIST FIRST INDEX SORT) . 8)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST NON-LOCAL SLASH LAST FIRST CONT HOOK XARG PNG PN) . 8)
    ((SYNSEM LOCAL COORD-REL L-INDEX) . 8)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS FIRST LOCAL CONT HOOK INDEX DIVISIBLE) . 8)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL SUBJ FIRST PUNCT RPUNCT) . 8)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CONT HOOK INDEX) . 8)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS REST FIRST NON-LOCAL SLASH) . 8)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST NON-LOCAL REL LIST) . 8)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST NON-LOCAL SLASH LAST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL SUBJ FIRST LOCAL) . 7)
    ((SYNSEM LOCAL CAT VAL SPR FIRST NON-LOCAL QUE) . 7)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST NON-LOCAL SLASH LAST FIRST CONT HOOK INDEX PNG PN) . 7)
    ((SYNSEM LOCAL CAT VAL CLTS REST FIRST LOCAL AGR PNG PN) . 7)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST NON-LOCAL SLASH LAST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS FIRST LIGHT) . 6)
    ((SYNSEM LOCAL CAT HEAD LSYNSEM LOCAL CAT VAL COMPS FIRST MODIFIED) . 6)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST LOCAL CAT HEAD MOD FIRST LOCAL) . 6)
    ((SYNSEM LOCAL AGR PNG GEN) . 6)
    ((SYNSEM LOCAL CAT VAL SPR FIRST NON-LOCAL REL) . 6)
    ((SYNSEM LOCAL CAT VAL COMPS REST FIRST LOCAL CAT HEAD TAM MOOD) . 6)
    ((SYNSEM LOCAL CAT HEAD MOD FIRST LOCAL CAT HEAD KEYS) . 6)
    ((SYNSEM LOCAL CAT HEAD MOD FIRST PUNCT RPUNCT) . 6)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST NON-LOCAL SLASH LAST FIRST CAT HEAD KEYS KEY) . 6)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST NON-LOCAL SLASH LAST FIRST CAT HEAD KEYS KEY) . 6)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CONT HOOK INDEX SF) . 6)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST LOCAL CAT HEAD CASE) . 6)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS FIRST) . 6)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT MC) . 6)
    ((SYNSEM LOCAL CAT HEAD LSYNSEM LOCAL CAT VAL COMPS FIRST LOCAL CAT VAL SUBJ) . 5)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL SPR FIRST NON-LOCAL REL LIST) . 5)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST LOCAL CONT HOOK XARG PNG PN) . 5)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS FIRST LOCAL CAT HEAD MOD FIRST LOCAL AGR) . 5)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD VFORM) . 5)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST NON-LOCAL SLASH LAST FIRST CAT HEAD CASE) . 5)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST LOCAL AGR SORT) . 4)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST NON-LOCAL SLASH LAST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS REST FIRST NON-LOCAL SLASH) . 4)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL SPR FIRST OPT) . 4)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST NON-LOCAL SLASH LAST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS FIRST LKEYS KEYREL ARG1 SORT) . 4)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST NON-LOCAL SLASH LAST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS FIRST LKEYS) . 4)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST NON-LOCAL SLASH LAST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS FIRST LOCAL CONT HOOK INDEX PNG PN) . 4)
    ((SYNSEM LOCAL CAT HEAD MOD FIRST LOCAL CONT HOOK INDEX PRONTYPE) . 4)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL SPR FIRST LOCAL CAT HEAD) . 4)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS FIRST NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL SUBJ FIRST LOCAL CONT HOOK INDEX SORT) . 4)
    ((STEM TO) . 4)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST NON-LOCAL SLASH LAST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS FIRST) . 4)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST NON-LOCAL SLASH LAST FIRST CAT HEAD PRD) . 4)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST LOCAL CAT HEAD PRD) . 4)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS FIRST LOCAL CONT HOOK INDEX SORT) . 4)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS FIRST NON-LOCAL REL LIST) . 4)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST) . 4)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST NON-LOCAL SLASH LAST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS FIRST LOCAL CAT HEAD KEYS KEY) . 3)
    ((SYNSEM LOCAL CAT VAL COMPS REST FIRST LOCAL CAT HEAD KEYS KEY) . 3)
    ((SYNSEM NON-LOCAL QUE LIST FIRST) . 3)
    ((SYNSEM NON-LOCAL REL LIST FIRST INDEX PRONTYPE) . 3)
    ((SYNSEM LOCAL CAT VAL SPR FIRST) . 3)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS FIRST NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL CLTS FIRST LOCAL AGR PRONTYPE) . 3)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS FIRST LOCAL CAT HEAD KEYS ALT2KEY) . 3)
    ((SYNSEM LOCAL CAT VAL CLTS REST FIRST LOCAL AGR SORT) . 3)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS FIRST NON-LOCAL SLASH) . 3)
    ((SYNSEM LOCAL CAT HEAD MOD FIRST LOCAL CAT HEAD PRD) . 2)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST LOCAL AGR) . 2)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS FIRST LOCAL CAT VAL SUBJ FIRST LOCAL CONT HOOK XARG PNG PN) . 2)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL SPR FIRST LOCAL CONT HOOK XARG SF) . 2)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS FIRST LOCAL CAT HEAD MOD FIRST LOCAL CONT) . 2)
    ((SYNSEM LOCAL CAT VAL SPR FIRST NON-LOCAL SLASH LIST) . 2)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST NON-LOCAL SLASH LAST FIRST CONT HOOK XARG SORT) . 2)
    ((SYNSEM LOCAL CAT VAL SPR FIRST LOCAL AGR) . 2)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST NON-LOCAL SLASH LAST FIRST CONT HOOK INDEX SORT) . 2)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST LOCAL AGR PNG PN) . 2)
    ((SYNSEM LOCAL CONT RELS LIST FIRST ARG1 PNG PN) . 2)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST NON-LOCAL SLASH LAST FIRST CAT VAL CLTS) . 2)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS FIRST LOCAL AGR PNG PN) . 2)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST NON-LOCAL QUE LIST) . 2)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS REST FIRST PUNCT RPUNCT) . 2)
    ((SYNSEM LOCAL CAT VAL CLTS FIRST NON-LOCAL SLASH LIST) . 2)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT HEAD INV) . 2)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CONT HOOK XARG) . 2)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD KEYS) . 2)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT VAL SUBJ FIRST LOCAL) . 1)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST NON-LOCAL SLASH LIST FIRST CAT HEAD CASE) . 1)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST NON-LOCAL SLASH LAST FIRST AGR) . 1)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CONT HOOK INDEX PNG PN) . 1)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL SUBJ FIRST LOCAL CAT VAL SUBJ FIRST LOCAL) . 1)
    ((SYNSEM LOCAL CAT VAL COMPS REST FIRST LOCAL CAT HEAD CASE) . 1)
    ((ARG-ST REST) . 1)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST NON-LOCAL SLASH LAST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL CLTS FIRST LOCAL AGR SORT) . 1)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST NON-LOCAL SLASH LAST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL CLTS FIRST LOCAL AGR PNG PN) . 1)
    ((SYNSEM LOCAL CAT VAL SUBJ FIRST NON-LOCAL SLASH LAST FIRST CONT HOOK INDEX) . 1)
    ((SYNSEM LOCAL CAT VAL CLTS REST FIRST NON-LOCAL REL LIST) . 1)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CONT HOOK INDEX SORT) . 1)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL SUBJ FIRST LOCAL CAT VAL SPEC) . 1)
    ((SYNSEM LOCAL CAT VAL COMPS FIRST LOCAL CAT HEAD MOD) . 1)
    ((SYNSEM NON-LOCAL SLASH LIST FIRST CAT HEAD MOD FIRST LOCAL CAT VAL COMPS FIRST LOCAL CAT VAL CLTS REST) . 1)))
