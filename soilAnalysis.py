#coding=utf-8
import os
class SoilAnalysis(object):
    def __init__(self):
        self.soil_dict = {}
        self.out_list  = []
        self.bracket_list = ['[', ']', '(', ')']
        self.pre_bracket_list = ['[', '(']
        self.back_bracket_list = [']', ')']
        self.seq = '='
        self.stack = []

    def read_from_file(self,filename):
        # 文件是否存在
        #=号后面数字
        if not os.path.exists(filename):
            print filename,' not exists'
            raise IOError
        with open(filename,'r') as f:
            for line in f:
                if line.count(self.seq)>0:
                    lst = line.split('=')
                    value = lst[1].strip()
                    if self.is_float(value):
                        key, value = lst[0].strip(), float(value)
                        self.soil_dict.update({key : value})
                    else:
                        print key,'参数错误：',value
                        raise AttributeError
                else:
                    key = line.strip()
                    self.out_list.append(key)

    def get_output(self,infile):
        try:
            self.read_from_file(infile)
            out_dict = self.compute_soils(self.out_list)
        except (IOError,  AttributeError),e:
            print 'error',e
        with open('output.txt','w') as f:
            for key in self.out_list:
                if out_dict.has_key(key):
                    f.write(key+' = ' + str(out_dict[key]) + '\n')
                    print key+' = ' + str(out_dict[key])


    def get_next_elem(self,soil):
        # 添加异常,序列不正确
        # 判断括号
        # 判断是否数字，如果是就把数字读完
        # 判断是单元素，还是双元素
        si = 0
        while si < len(soil):
            newele = soil[si]
            if not self.is_bracket( newele ):
                if newele.isdigit() :
                    digit_list = [ newele ]
                    while (si+1)<len(soil) and soil[si+1].isdigit():
                        si = si + 1
                        digit_list.append(soil[si])
                    newele = ''.join(digit_list)
                else:
                    double_ele = soil[si:si+2]
                    if self.soil_dict.has_key(double_ele):
                        si = si + 1
                        newele = double_ele
                    if not self.soil_dict.has_key(newele):
                        print 'can not recgonize ',newele
                        raise Exception
            si = si + 1
            yield newele

    def compute_soil(self,soil):
        # 列表中只放括号和数字
        # 判断括号，前括号，压入前值，压入括号
        #           后括号，取出所有值合并，直到取出前括号，压入值
        # 最后判断是元素
        stack = []
        for elem in self.get_next_elem(soil):
            if self.is_pre_bracket(elem):
                stack.append(elem)
            if self.is_back_bracket(elem):
                merge_wei = 0
                top = stack.pop()
                while not self.is_pre_bracket(top):
                    merge_wei += top
                    top = stack.pop()
                stack.append( merge_wei )
            if elem.isdigit():
                size = len(stack)
                stack[size-1] = stack[size-1] * int(elem)
            if self.soil_dict.has_key(elem):
                stack.append( self.soil_dict[elem] )
        weight = 0
        while len(stack)>0:
            weight += stack.pop()
        return weight

    def compute_soils(self,out_list):
        out_dict = {}
        for key in out_list:
            try:
                out_dict[key] = self.compute_soil(key)
            except Exception,e:
                pass
        return out_dict

    def is_float(self,ele):
        if ele.isdigit():
            return True
        elif isinstance( eval(ele),float):
            return True
        else: 
            return False

    def is_bracket(self,ele):
        return True if self.bracket_list.count(ele) >0  else False

    def is_pre_bracket(self,ele):
        return True if self.pre_bracket_list.count(ele) >0  else False

    def is_back_bracket(self,ele):
        return True if self.back_bracket_list.count(ele) >0  else False


if __name__=='__main__':
    soli = SoilAnalysis()
    soli.get_output('input.txt')
