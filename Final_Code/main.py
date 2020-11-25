from source import Check_Question_True_False, Find_Answer, Load_KB, Get_Valuable_Pos

KB = Load_KB("cay_pha_he.pl")

#doc ra danh sach cac cau hoi
question_file = open("questions_2.txt")
lines = question_file.readlines()
question_file.close()
questions_list = [] #danh sach cac cau hoi
for line in lines:
    if line != '\n':
        #loai bo dau xuong dong cuoi moi cau hoi neu co
        if line[-1] == '\n':
            line = line[:-1]
        if '?- ' in line: #loai bo dau '?-' dau moi cau hoi neu co
            line = line[3:]
            questions_list.append(line)
        else:
            questions_list.append(line)

#in output ra file
output_file = open("output_2.txt", "w")

for question in questions_list:
    #truong hop khong co bien trong cau hoi, day la loai cau hoi tra ra ket qua True hoac False
    if Get_Valuable_Pos(question) == -1:
        answer = Check_Question_True_False(KB, question)
    #truong hop cau hoi ton tai bien, doi hoi phai dua ra cau tra loi
    else:
        answer = Find_Answer(KB, question)
    
    #ghi vao file output
    output_file.write('//Question: ')
    output_file.write(question)
    output_file.write('\n')
    output_file.write(str(answer))
    output_file.write('\n\n')

output_file.close()
    


