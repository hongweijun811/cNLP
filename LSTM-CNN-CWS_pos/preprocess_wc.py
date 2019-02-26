# -*- coding: utf-8 -*-
#


from __future__ import print_function

from collections import defaultdict

import codecs
import argparse
import os


NE_LEFT = u'['
NE_RIGHT = u']'
DIVIDER = u'/'
SPACE = u' '
UNK = u"unk"

WORD_S = u'0'
WORD_B = u'1'
WORD_M = u'2'
WORD_E = u'3'

Part_of_speech = ['a',
'ad',
'ag',
'al',
'an',
'b',
'begin',
'bg',
'bl',
'c',
'cc',
'd',
'dg',
'dl',
'e',
'end',
'f',
'g',
'gb',
'gbc',
'gc',
'gg',
'gi',
'gm',
'gp',
'h',
'i',
'j',
'k',
'l',
'm',
'mg',
'Mg',
'mq',
'n',
'na',
'nb',
'nba',
'nbc',
'nbp',
'nf',
'ng',
'nh',
'nhd',
'nhm',
'ni',
'nic',
'nis',
'nit',
'nl',
'nm',
'nmc',
'nn',
'nnd',
'nnt',
'nr',
'nr1',
'nr2',
'nrf',
'nrj',
'ns',
'nsf',
'nt',
'ntc',
'ntcb',
'ntcf',
'ntch',
'nth',
'nto',
'nts',
'ntu',
'nx',
'nz',
'o',
'p',
'pba',
'pbei',
'q',
'qg',
'qt',
'qv',
'R',
'r',
'rg',
'Rg',
'rr',
'ry',
'rys',
'ryt',
'ryv',
'rz',
'rzs',
'rzt',
'rzv',
's',
't',
'tg',
'u',
'ud',
'ude1',
'ude2',
'ude3',
'udeng',
'udh',
'ug',
'uguo',
'uj',
'ul',
'ule',
'ulian',
'uls',
'usuo',
'uv',
'uyy',
'uz',
'uzhe',
'uzhi',
'v',
'vd',
'vf',
'vg',
'vi',
'vl',
'vn',
'vshi',
'vx',
'vyou',
'w',
'wb',
'wd',
'wf',
'wh',
'wj',
'wky',
'wkz',
'wm',
'wn',
'wp',
'ws',
'wt',
'ww',
'wyy',
'wyz',
'x',
'xu',
'xx',
'y',
'yg',
'z',
'zg'
]


def clean_sentence(line_list):
  new_line_list = []

  new_line_tag_list = []

  for token in line_list:
    div_id = token.rfind(DIVIDER)
    
    if div_id < 1:
      # the div_id shouldn't be lower than 1
      # if it does, give up the word
      continue

    word = token[ : div_id]


    ###这里需要将
    tag = token[(div_id + 1) : ]
    index_tag = Part_of_speech.index(tag)


  #判断如果分的词含有 【 】 符号时，如何处理。 但是好像只能处理包含一个【 或 】 的情况，超过一个以上好像只能删去一个
    if word[0] == NE_LEFT and len(word) > 1:
      new_line_list.append(word[1 : ])
      #需要处理 【 时要将【词 分成【 和 词两个 分别记录词标注
      #new_line_list_cixing.append(word[])
      new_line_tag_list.append(index_tag)

    elif word[-1] == NE_RIGHT and len(word) > 1:
      div_id = word.rfind(DIVIDER)
      if div_id < 1:
        new_line_list.append(word[ : (len(word)-1)])
        ###这种情况不是只能时/n]这种吗  那录取的词岂不是为01 直接录取了/n 这个作为词吗
        new_line_tag_list.append(index_tag)
      else:
        new_line_list.append(word[ : div_id])
        temp_tag = word[div_id+2 -1]
        index_tag = Part_of_speech.index(temp_tag)
        new_line_tag_list.append(index_tag)
    # 需要处理 ]时要将  词 ] 分成 ]  和 词两个 分别记录词标注
    # new_line_list_cixing.append(word[div_id+1 :])

    else:
      new_line_list.append(word)
      new_line_tag_list.append(index_tag)
  return new_line_list,new_line_tag_list


def write_line(line_list2, outstream, sep = SPACE):
  line_list = [str(i) for i in line_list2]
  line = sep.join(line_list)
  outstream.write(line + u'\n')


def analyze_line(line_list, vob_dict):
  char_list = []
  label_list = []

  for word in line_list:
#    length = len(word)
#    if length == 1:
#      char_list.append(word)
#      label_list.append(WORD_S)
#      vob_dict[word] += 1


 #   else:
 #     for pos, char in enumerate(word):
 #       if pos == 0:
 #         label_list.append(WORD_B)
 #       elif pos == (length - 1):
 #         label_list.append(WORD_E)
 #       else:
 #         label_list.append(WORD_M)

#        char_list.append(char)
        char_list.append(word)
        vob_dict[word] += 1

  #assert len(char_list) == len(label_list)
  #return char_list, label_list
  return char_list


def generate_files(corpora, vob_path, char_file, train_word_file,
    train_label_file, eval_word_file, eval_label_file, eval_gold_file,
    test_file, gold_file, step, freq, max_len):

  inp = codecs.open(corpora, 'r', "utf-8")

  tr_wd_wr = codecs.open(train_word_file, 'w', "utf-8")
  tr_lb_wr = codecs.open(train_label_file, 'w', "utf-8")
  ev_wd_wr = codecs.open(eval_word_file, 'w', "utf-8")
  ev_lb_wr = codecs.open(eval_label_file, 'w', "utf-8")

  ev_gold_wr = codecs.open(eval_gold_file, 'w', "utf-8")
  test_wr = codecs.open(test_file, 'w', "utf-8")
  gold_wr = codecs.open(gold_file, 'w', "utf-8")

  dump_cnt = 0
  #统计每个词的词频，默认初始类型为int
  vob_dict = defaultdict(int)
  isEval = True

  with inp, tr_wd_wr, tr_lb_wr, ev_wd_wr, ev_lb_wr, ev_gold_wr, test_wr, gold_wr:
    for ind, line in enumerate(inp):
      line_list = line.strip().split()
      if len(line_list) > max_len:
        dump_cnt += 1
        continue

      #将/和词性等标志去掉，只保留字。
      cleaned_line,cleaned_tag_line = clean_sentence(line_list)
      if not cleaned_line:
        dump_cnt += 1
        continue

      #这里统计的原则十什么，返回了每个字的状态 B E S M
     # char_list, label_list = analyze_line(cleaned_line, vob_dict)
      char_list = analyze_line(cleaned_line, vob_dict)
      if ind % step == 0:
        if isEval:
          #分别记录了验证集里分开每个字的文件，每个字的状态文件，每个词的文件
#          write_line(char_list, ev_wd_wr)
#          write_line(label_list, ev_lb_wr)
#          write_line(cleaned_line, ev_gold_wr)

          write_line(cleaned_line, ev_wd_wr)
          write_line(cleaned_tag_line, ev_lb_wr)
          write_line(cleaned_line, ev_gold_wr)

          isEval = False
        else:
          #如果ind % setp成立 交替将改行的每个词文件，这里做测试集的文件
          write_line(cleaned_line, test_wr, sep = u'')
          write_line(cleaned_line, gold_wr)



          isEval = True
      else:
        #一个step相当于一个batchsize，大部分不为0的判断的读入的行 作为训练集，写入分开每个字的文件tr_wd_wr，和每个字的状态文件tr_lb_wr
        #write_line(char_list, tr_wd_wr)
        #write_line(label_list, tr_lb_wr)

        write_line(cleaned_line, tr_wd_wr)
        write_line(cleaned_tag_line, tr_lb_wr)

#统计文件中所有的分开的字，过滤掉小于词频的字，用UNK代替
  inp = codecs.open(corpora, 'r', "utf-8")
  ch_wr = codecs.open(char_file, 'w', "utf-8")
  with inp, ch_wr:
    for line in inp:
      line_list = line.strip().split()
      if len(line_list) > max_len:
        continue

      cleaned_line,cleaned_tag_line = clean_sentence(line_list)
      if not cleaned_line:
        continue
      char_list = []
      for phr in cleaned_line:
#        for ch in phr:
#          if vob_dict[ch] < freq:
          if vob_dict[phr] < freq:
            char_list.append(UNK)
          else:
#            char_list.append(ch)
            char_list.append(phr)

      write_line(char_list, ch_wr)

#将大于词频的字和第一个为UNK 写入文件中 过滤掉了小于词频的字和多余的UNK。
  word_cnt = 0
  with codecs.open(vob_path, 'w', "utf-8") as vob_wr:
    vob_wr.write(UNK + u'\n')
    for word, fq in vob_dict.items():
      if fq >= freq:
        vob_wr.write(word + u'\n')
        word_cnt += 1

  print("Finished, give up %d sentences." % dump_cnt)
  print("Select %d chars from the original %d chars" % (word_cnt, len(vob_dict)))


# used for people corpora
def people_main(args):
  corpora = args.all_corpora
  assert os.path.exists(corpora)

  total_line = 0
  # count the total number of lines
  with open(corpora, 'r', encoding='utf8') as inp:
    for line in inp:
      total_line += 1

  base = 2 * args.line_cnt
  #base = 1

  assert base < total_line
  step = total_line // base

  train_word_file = args.train_file_pre + ".txt"
  train_label_file = args.train_file_pre + ".lb"
  eval_word_file = args.eval_file_pre + ".txt"
  eval_label_file = args.eval_file_pre + ".lb"

  generate_files(corpora, args.vob_path, args.char_file,
      train_word_file, train_label_file, eval_word_file,
      eval_label_file, args.eval_gold_file, args.test_file,
      args.gold_file, step, args.word_freq, args.max_len)


def analyze_write(inp, word_writer, label_writer,
    vob_dict = defaultdict(int)):
  with inp, word_writer, label_writer:
    for line in inp:
      line_list = line.strip().split()
      if len(line_list) < 1:
        continue

      char_list, label_list = analyze_line(line_list, vob_dict)
      write_line(char_list, word_writer)
      write_line(label_list, label_writer)


# used for icwb2 data
def icwb_main(args):
  corpora = args.all_corpora
  assert os.path.exists(corpora)
  gold_file = args.gold_file
  assert os.path.exists(gold_file)
  freq = args.word_freq

  train_word_file = args.train_file_pre + ".txt"
  train_label_file = args.train_file_pre + ".lb"
  eval_word_file = args.eval_file_pre + ".txt"
  eval_label_file = args.eval_file_pre + ".lb"

  train_inp = codecs.open(corpora, 'r', "utf-8")
  gold_inp = codecs.open(gold_file, 'r', "utf-8")

  ch_wr = codecs.open(args.char_file, 'w', "utf-8")
  tr_wd_wr = codecs.open(train_word_file, 'w', "utf-8")
  tr_lb_wr = codecs.open(train_label_file, 'w', "utf-8")
  ev_wd_wr = codecs.open(eval_word_file, 'w', "utf-8")
  ev_lb_wr = codecs.open(eval_label_file, 'w', "utf-8")

  vob_dict = defaultdict(int)
  analyze_write(train_inp, tr_wd_wr, tr_lb_wr, vob_dict)
  analyze_write(gold_inp, ev_wd_wr, ev_lb_wr)

  train_inp = codecs.open(corpora, 'r', "utf-8")
  with train_inp, ch_wr:
    for line in train_inp:
      phrases = line.strip().split()
      char_list = []
      for phr in phrases:
        for ch in phr:
          if vob_dict[ch] < freq:
            char_list.append(UNK)
          else:
            char_list.append(ch)

      write_line(char_list, ch_wr)

  word_cnt = 0
  with codecs.open(args.vob_path, 'w', "utf-8") as vob_wr:
    vob_wr.write(UNK + u'\r\n')
    for word, fq in vob_dict.items():
      if fq >= freq:
        vob_wr.write(word + u'\r\n')
        word_cnt += 1

  print("Finished, handling icwb2 data.")
  print("Select %d chars from the original %d chars" % (word_cnt, len(vob_dict)))


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.register("type", "bool", lambda v: v.lower() == "true")

  # input
  parser.add_argument(
    "--all_corpora",
    type = str,
    default = "./data/people2014All.txt",
    help = "all the corpora")

  # output
  parser.add_argument(
    "--vob_path",
    type = str,
    default = "./data/cws-v2-data/vocab.txt",
    help = "vocabulary's path")

  parser.add_argument(
    "--char_file",
    type = str,
    default = "./data/cws-v2-data/chars.txt",
    help = "the file used for word2vec pretraining")

  parser.add_argument(
    "--train_file_pre",
    type = str,
    default = "./data/cws-v2-data/train",
    help = "training file's prefix")

  parser.add_argument(
    "--eval_file_pre",
    type = str,
    default = "./data/cws-v2-data/eval",
    help = "eval file's prefix")

  parser.add_argument(
    "--eval_gold_file",
    type = str,
    default = "./data/cws-v2-data/eval_gold.txt",
    help = """gold file, used for the evaluation during training, \
      only generated for the 'people' corpus""")

  parser.add_argument(
    "--test_file",
    type = str,
    default = "./data/cws-v2-data/test.txt",
    help = "test file, raw sentences")

  parser.add_argument(
    "--gold_file",
    type = str,
    default = "./data/cws-v2-data/gold.txt",
    help = "gold file, segmented sentences")

  # parameters
  parser.add_argument(
    "--word_freq",
    type = int,
    default = 3,
    help = "word frequency")

  parser.add_argument(
    "--line_cnt",
    type = int,
    default = 8000,
    help = "the number of lines in eval or test file")

  # NOTE: It is the max length of word sequence, not char.
  parser.add_argument(
    "--max_len",
    type = int,
    default = 120,
    help = "deprecate the sentences longer than <max_len>")

  parser.add_argument(
    "--is_people",
    type = "bool",
    default = True,
    help = "Whether it is handling with People corpora")

  args = parser.parse_args()
  if args.is_people:
    people_main(args)
  else:
    icwb_main(args)
