import random

#load KB tu file 
def Load_KB(file_name):
    f = open(file_name, "r")
    fact_list = f.readlines()
    f.close()

    #loai bo cac dau xuong dong cuoi moi cau
    delete_sentences = []
    for i in range(len(fact_list)):
        fact_list[i] = Eliminate_Spaces(fact_list[i]) #loai bo cac khoang trang
            
        #neu cau chi gom dau xuong dong, hoac la cau chu thich thi loai khoi KB
        if (fact_list[i] == '\n') or (fact_list[i][0] == '%') or (fact_list[i][:1] == "/*"):
            delete_sentences.append(fact_list[i])

        else:
            pos = fact_list[i].find('\n')
            if pos:
                fact_list[i] = fact_list[i][:pos]
        
        #loai bo dau cham cuoi cau de tinh toan ve sau
        if fact_list[i][-1] == '.':
            fact_list[i] = fact_list[i][:-1]

    for del_sen in delete_sentences:
        fact_list.remove(del_sen)
    return fact_list

#loai bo cac khoang trong du thua trong cau de de xu ly
def Eliminate_Spaces(sentence):
    return sentence.replace(' ', '')

#lay ra ten cua cac quan he
def Get_Relation_Name(question):
    return question[:question.find('(')]


#lay ra cac ki hieu hang trong vi tu
def Get_Constant_Symbols(predicate):
    #cac doi tuong nam sau cap dau ngoac ()
    const_sym_str = predicate[predicate.find('(') + 1:predicate.find(')')]
    constant_symbols = const_sym_str.split(',')
    return constant_symbols


#lay ra phan dinh nghia cua ham co ten tuong ung trong KB
def Get_Defination_By_Name(KB, predicate):
    known_event_names = ['parent', 'male', 'female', 'married', 'divorced'] #nhung vi tu da cho tu gia thuyet
    const_symbols = Get_Constant_Symbols(predicate)
    # print('predicate: ', predicate)
    # print('symbols: ', const_symbols)
    
    #neu khong phai la ham thi khong co phan dinh nghia
    if Get_Relation_Name(predicate) in known_event_names:
        return 'None'

    for sentence in KB:
        if Get_Relation_Name(sentence) == Get_Relation_Name(predicate):
            const_symbols_sentence = Get_Constant_Symbols(sentence)
            # print('predicate zzzzzzzz:', sentence)
            # print('symbols zzzzzzzzzz:', const_symbols_sentence)

            #loai bo su trung ten bien giua sentence va predicate
            for j in range(len(const_symbols_sentence)):
                if const_symbols_sentence[j] in const_symbols:
                    new_symbol = const_symbols_sentence[j]
                    while new_symbol in const_symbols:
                        new_symbol = new_symbol + str(random.randint(1, 10))
                    sentence = sentence.replace(const_symbols_sentence[j], new_symbol)
                    #print('new sentence: ', sentence)
            #thay the doi so tuong ung giua 2 vi tu
            for i in range(len(const_symbols)):
                sentence = sentence.replace(const_symbols_sentence[i], const_symbols[i])

            return sentence[sentence.find(":-") + 2:]
    return 'None'


#tach cac vi tu dinh nghia ham  thanh cac vi tu rieng biet
def Separate_Sentence(defination, separate_type):
    defination = Eliminate_Spaces(defination)
    if defination[-1] == '.':
        defination = defination[:-1]
    sub_predicates = defination.split(')'+separate_type)
    for i in range(len(sub_predicates)):
        if (sub_predicates[i][-1] != ')') and (i != len(sub_predicates) - 1) and (sub_predicates[i] != 'None'):
            sub_predicates[i] = sub_predicates[i] + ')' #bo sung dau ')' bi mat khi thuc hien ham split
    return sub_predicates


#tra ve vi tri xuat hien cua bien 
#neu khong ton tai bien thi tra ve -1
def Get_Valuable_Pos(predicate):
    predicate = Eliminate_Spaces(predicate)
    constant_syms = Get_Constant_Symbols(predicate)
    for i in range(len(constant_syms)):
        if (constant_syms[i][0] >= 'A') and (constant_syms[i][0] <= 'Z'): #ten bien luon bat dau bang chu cai viet hoa
            return i
    return -1


#kiem tra xem co phai tat ca cac doi so trong vi tu deu la bien hay khong
def All_Is_Valuables(predicate):
    const_symbols = Get_Constant_Symbols(predicate)
    for const_symbol in const_symbols:
        if (const_symbol[0] < 'A') or (const_symbol[0] > 'Z'):
            return False
    return True


#kiem tra co phai tat ca cac do
def All_Are_Const_Syms(predicate):
    if Get_Valuable_Pos(predicate) != -1:
        return True
    return False


#lay ra cac su kien da duoc xac dinh trong KB
def Get_Known_Events(KB):
    known_event_names = ['parent', 'male', 'female', 'married', 'divorced'] #nhung vi tu da cho tu gia thuyet
    known_events = []
    for sentence in KB:
        if Get_Relation_Name(sentence) in known_event_names:
            known_events.append(sentence)
    return known_events


#tra ve tat ca cac event co ten tuong ung trong KB
def Get_Event_By_Name(known_events, predicate):
    event_name = Get_Relation_Name(predicate)
    list_events = []
    for event in known_events:
        if event_name == Get_Relation_Name(event):
            list_events.append(event)
    return list_events


#tra ve true neu day la mot bieu thuc dieu kien co chua '/='
def Have_Differential_Cond(predicate):
    if predicate.find(r'\=') != -1:
        return True
    return False


#kiem tra xem vi tu co con suy dien lui duoc nua hay khong
def Cannot_Backward_Chaining(KB, predicate):
    #neu co chua dieu kien thi khong suy dien duoc nua
    if Have_Differential_Cond(predicate):
        return True

    known_event_names = ['parent', 'male', 'female', 'married', 'divorced']
    #neu vi tu nam trong tap cac su kien da biet thi khong the suy dien duoc nua
    if Get_Relation_Name(predicate) in known_event_names:
        return True 
    return False


#tra ve gia tri tuong ung cua bien voi 1 vi tu da biet cac doi so
def Get_Compatible_Value(predicate1, predicate2):
    predicate1 = Eliminate_Spaces(predicate1)
    predicate2 = Eliminate_Spaces(predicate2)
    pos = Get_Valuable_Pos(predicate1)
    const_syms_1 = Get_Constant_Symbols(predicate1)
    const_syms_2 = Get_Constant_Symbols(predicate2)
    answer = ''
    result = []
                
    while pos != -1:
        answer = const_syms_1[pos] + ' ' + '=' + ' ' + const_syms_2[pos]
        result.append(answer)
        predicate1 = predicate1.replace(const_syms_1[pos], const_syms_2[pos])
        pos = Get_Valuable_Pos(predicate1)
    return result



#tim trong KB cac su kien phu hop
def Find_Matched_Events(known_events, predicate):
    predicate = Eliminate_Spaces(predicate) #xoa bo cac dau khoang trang trong cau hoi
    predicate_name = Get_Relation_Name(predicate)
    pos_valuable = Get_Valuable_Pos(predicate)
    const_syms = Get_Constant_Symbols(predicate)
    matched_events = []
    is_matched = False #danh dau su tuong thich giua 2 vi tu
    check = 0 #do vị trí của các vị từ được ta tổ chức thành các cụm trong KB (VD cụm parent, xong đến cụm male), do đó ta kiểm tra
                    #xem đã đến cụm match với predicate mà ta đưa vào hay chưa, nếu rồi thì không cần kiểm tra các dòng sự kiện bên dưới
                    #nó nữa 
                    #check = 0: chua xet den cum cac vi tu phu hop
                    #check = 1: dang xet den
                    #check = 2: da xet qua

    #neu tat ca doi so deu la bien thi lay ra tat ca cac event co cung ten voi predicate trong KB
    if All_Is_Valuables(predicate):
        matched_events = Get_Event_By_Name(known_events, predicate)
    else:
        for i in range(len(known_events)):
            if check == 2: 
                break
            
            is_matched = False
            if Get_Relation_Name(known_events[i]) == predicate_name:
                check = 1
                const_syms_event = Get_Constant_Symbols(known_events[i])
                #so sanh cac doi tuong hang trong 2 vi tu, neu gap vi tri cua bien thi khong xet
                for j in range(len(const_syms)):
                    if j != pos_valuable: 
                        if const_syms[j] != const_syms_event[j]: #neu co 1 doi tuong khong tuong thich thi day khong phai la su kien phu hop
                            break
                        else:
                            is_matched = True
                #neu cac doi tuong duoc xet het thi co nghia day la su kien phu hop
                if is_matched: 
                    matched_events.append(known_events[i])
                                    
            else:
                if check == 1:
                    check = 2

    return matched_events


#lay ra tat ca cac ten bien co trong tap nghiem
def Get_All_Variables(list_solution):
    variables = []
    if not list_solution:
        return set()
    
    for i in range(len(list_solution)):
        if type(list_solution[i] ) == tuple:
            list_solution[i] = list(list_solution[i])

    #truong hop tap nghiem chi co 1 bien
    if (type(list_solution[0]) != tuple) and (type(list_solution[0]) != list):
        for i in range(len(list_solution)):
            temp = list_solution[i].split()
            variables.append(temp[0])
    #truong hop tap nghiem co nhieu bien 
    else:
        for i in range(len(list_solution)):
            for j in range(len(list_solution[i])):
                temp = list_solution[i][j].split()
                variables.append(temp[0])
    return set(variables)


def Find_General_Solutions(list1, list2):
    variables1 = Get_All_Variables(list1)
    variables2 = Get_All_Variables(list2)
    intersect_vars = variables1.intersection(variables2)
    general_solutions = []

    if len(list1) == 0:
        general_solutions = list(list2)
    elif len(list2) == 0:
        general_solutions = list(list1)

    #truong hop co su trung ten bien giua 2 tap nghiem
    if intersect_vars:
        general_solutions = Find_Intersect_Values(list1, list2)
        return general_solutions
    #neu cac bien giua 2 list la khac nhau thi tien hanh hop gia tri cua nghiem
    else:
        for i in range(len(list1)):
            for j in range(len(list2)):
                if (type(list1[i]) != list) and (type(list2[j]) != list):
                    list3 = [list1[i], list2[j]]
                    general_solutions.append(list3)
                elif (type(list1[i]) == list) and (type(list2[j]) != list):
                    list3 = list1[i].append(list2[j])
                    general_solutions.append(list3)
                elif (type(list1[i]) != list) and (type(list2[j]) == list):
                    list3 = list(list2[j])
                    list3.append(list1[i])
                    general_solutions.append(list3)
                else:
                    list3 = set(list1[i]+list2[j])
                    general_solutions.append(list(list3))
        return general_solutions


#lay ra ten cua bien chua nghiem
def Get_Solution_Name(solution):
    temp = solution.split()
    return temp[0]   


#lay ra gia tri cua nghiem
def Get_Solution_Value(solution):
    temp = solution.split()
    return temp[-1]


#lay giao cua 2 tap hop
def Find_Intersect_Values(list1, list2):
    result = []
    if type(list1[0]) != list:
        for i in range(len(list1)):
            list1[i] = [list1[i]]
    
    if type(list2[0]) != list:
        for i in range(len(list2)):
            list2[i] = [list2[i]]

    for i in range(len(list1)):
        for j in range(len(list2)):
            # print('list1[i]: ', list1[i])
            # print('list2[j]: ', list2[j])
            # #truong hop 2 phan tu con co chieu dai bang nhau
            # if list1[i] == list2[j]: 
            #     result.append(list1[i])

            # #truong hop 2 phan tu con co so phan tu khac nhau
            # else:
            list3 = set()
            for x in range(len(list1[i])):
                intersect = True
                for y in range(len(list2[j])):
                    # print('list1[i][x]: ', list1[i][x])
                    # print('list2[j][y]: ', list2[j][y])
                    #intersect = True
                    if Get_Solution_Name(list2[j][y])==Get_Solution_Name(list1[i][x]):
                        #neu co su xung dot gia tri thi chung to khong co nghiem chung
                        if Get_Solution_Value(list2[j][y]) != Get_Solution_Value(list1[i][x]):
                            #print('khac nhau')
                            intersect = False
                            break
                        else:
                            #intersect = True 
                            list3 = set(list1[i]+list2[j])
                            #print('hop nghiem: ', list3)

                #neu co su mau thuan nghiem thi dung
                if intersect == False:
                    break
                # else:
                #     result.append(list(list3))
                #     print('result: ', result)
            if intersect == True:
                result.append(list(list3))
                #print('result: ', result)
                       
    return result


#loai bo tat ca phan tu rong trong tap nghiem tong 
def Reject_All_Empty_Element(list_solution):
    result = []
    for i in range(len(list_solution)):
        if len(list_solution[i]) != 0:
            result.append(list_solution[i])
    return result


#lay ra nghiem co ten bien tuong ung trong tap nghiem
def Get_Solution_By_Variable(solutions, variable_name):
    for i in range(len(solutions)):
        if Get_Solution_Name(solutions[i]) == variable_name:
            return solutions[i]
    return ''

#loai bo nhung nghiem khong thoa dieu kien
def Reject_Solution_By_Cond(solutions, condition):
    #xac dinh bien va trong bieu thuc dieu kien
    result = []
    vals = condition.split(r'\=')
    arg1 = vals[0]
    arg2 = vals[1]
    count_variable = 0 #cho biết số đối số là biến có trong điều kiện 

    #dem so bien co trong bieu thuc dieu kien
    if (vals[0][0] >= 'A') and (vals[0][0] <= 'Z'):
        count_variable += 1
    
    if (vals[1][0] >= 'A') and (vals[1][0] <= 'Z'):
        count_variable += 1

    #lay ra cac nghiem thoa dieu kien

    #truong hop co 1 bien va 1 hang
    if count_variable == 0:
        if arg1 != arg2:
            return solutions
        else:
            return []

    elif count_variable == 1:
        if (arg1[0] >= 'A') and (arg1[0] <= 'Z'):
            variable = arg1
            const_sym = arg2
        else:
            variable = arg2
            const_sym = arg1
        wrong_sol = variable + ' = ' + const_sym
        for i in range(len(solutions)):
            if wrong_sol not in solutions[i]:
                result.append(solutions[i])
    #truong hop co 2 bien
    elif count_variable == 2:
        sol1 = ''
        sol2 = ''
        for i in range(len(solutions)):
            sol1 = Get_Solution_By_Variable(solutions[i], arg1)
            sol2 = Get_Solution_By_Variable(solutions[i], arg2)

            # if (sol1 == '') and (sol2 == ''):
            #     result.append(solutions[i])

            if (sol1 != '') and (sol2 != ''):
                if Get_Solution_Value(sol1) != Get_Solution_Value(sol2):
                    result.append(solutions[i])

            else:
                result.append(solutions[i])
                
    return result

#lay ra gia tri cua doi so la hang duoc truyen vao trong cau hoi
def Get_Input_Const(question):
    const_syms = Get_Constant_Symbols(question)
    for const_sym in const_syms:
        if (const_sym[0] <= 'A') or (const_sym[0] >= 'Z'):
            return const_sym
    return ''

#lay ra ten bien duoc truyen vao trong cau hoi
def Get_Variable_Name(question):
    const_syms = Get_Constant_Symbols(question)
    for const_sym in const_syms:
        if (const_sym[0] >= 'A') and (const_sym[0] <= 'Z'):
            return const_sym
    return ''

#cho biet vi tri cua hang so duoc truyen vao trong cau hoi
def Get_Pos_Of_Const(question):
    const_syms = Get_Constant_Symbols(question)
    for i in range(len(const_syms)):
        if (const_syms[i][0] <= 'A') or (const_syms[i][0] >= 'Z'):
            return i
    return -1

#thay ten cho bien trong cau hoi de tranh trung lap ten bien trong KB
def Change_Var_Names(question):
    question = Eliminate_Spaces(question)
    const_syms = Get_Constant_Symbols(question)
    original_names = []
    for i in range(len(const_syms)):
        if (const_syms[i][0] >= 'A') and (const_syms[i][0] <= 'Z'):
            new_var_name = 'Q' + str(i)
            original_names.append([const_syms[i], new_var_name])
            #thay ten cho bien
            question = question.replace(const_syms[i], new_var_name)
    return [question, original_names]


def Find_Answer(KB, question):
    final_answers = [] #chua ket qua tra ve
    stack = [] #stack chua cac tap goal
    known_events = Get_Known_Events(KB)

    #chuẩn hóa tên biến để không trùng với tên các biến trong KB, nhằm tránh sai sót 
    temp = Change_Var_Names(question)
    question = temp[0]
    original_names = temp[1]

    #Truong hop cau hoi khong the suy dien lui
    if Cannot_Backward_Chaining(KB, question):
        events = Find_Matched_Events(known_events, question)
        for event in events:
            final_answers.append(Get_Compatible_Value(question, event))
        return Get_Final_Answer(question, final_answers, original_names)

    #Truong hop can phai suy dien lui de tim ra cau tra loi
    defination = Get_Defination_By_Name(KB, question)
    
    sub_predicates = Separate_Sentence(defination, ';')
    for i in range(len(sub_predicates)):
        stack.append(Separate_Sentence(sub_predicates[i], ','))

    while stack:
        goal = stack.pop()
        # print("=================================")
        # print('goal: ', goal)
        count = 0 #dem xem co bao nhieu vi tu trong goal khong suy dien duoc nua

        for i in range(len(goal)):
            if Cannot_Backward_Chaining(KB, goal[i]) == False:
                new_elements = Separate_Sentence(Get_Defination_By_Name(KB, goal[i]), ';')
            
                if len(new_elements) > 1:
                    for element in new_elements:
                        goal[i] = element
                        stack.append(goal)
                    break
                else:
                    new_predicates = Separate_Sentence(Get_Defination_By_Name(KB, goal[i]), ',')

                    #loai bo goal[i] va them vao cac phan tu thay the
                    goal.pop(i)
                    goal.extend(new_predicates)
                    stack.append(goal)
                    break
            else:
                count += 1

        #neu tat ca cac vi tu trong goal deu khong suy dien duoc nua
        if count == len(goal):
            #tim loi giai cho tung vi tu trong goal
            general_answers = []
            check = False 
            
            for j in range(count):
                # print('GOAL[J]: ', goal[j])
                answers = []
                condition = ''
                if Have_Differential_Cond(goal[j]):
                    condition = goal[j]
                    #chuyen dieu kien ve cuoi de xet sau
                    if j != count - 1:
                        goal[j] = goal[count-1]
                        goal[count-1] = condition
                    else:
                        general_answers = Reject_Solution_By_Cond(general_answers, condition)
                else:
                    matched_events = Find_Matched_Events(known_events, goal[j])
                    if matched_events:
                        for event in matched_events:
                            if goal[j] != event:
                                answers.append(Get_Compatible_Value(goal[j], event)) 
                            else:
                                check = True #danh dau la menh de dung
                    else:
                        check = False

                    #neu menh de truoc do co cau tra loi hoac menh de duoc chung minh dung
                    if answers or (check == True):
                        if general_answers:
                            # print()
                            # print('ANSWER: ', answers)
                            # print('@len: ', len(answers))
                            # print()
                            general_answers = Find_General_Solutions(general_answers, answers)
                            general_answers = Reject_All_Empty_Element(general_answers)
                        else:
                            general_answers = answers
                    else:
                        general_answers = []
                        break
                # print()
                # print('GENERAL: ', general_answers)
                # print('@len: ', len(general_answers))
                # print()
            final_answers.extend(list(general_answers))

    return Get_Final_Answer(question, final_answers, original_names)
    

#dua ra ket qua hoan chinh cuoi cung (loc bo cac ket qua khong can thiet)
def Get_Final_Answer(question, answer, original_names):
    question = Eliminate_Spaces(question)
    const_syms = Get_Constant_Symbols(question)
    variables = []
    final_answer = []
    for const_sym in const_syms:
        if (const_sym[0] >= 'A') and (const_sym[0] <= 'Z'):
            variables.append(const_sym)

    if len(variables) < 2:
        for i in range(len(answer)):
            for j in range(len(answer[i])):
                if Get_Solution_Name(answer[i][j]) == variables[0]:
                    final_answer.append(answer[i][j])
        
        #lay lai ten cu cua bien
        for i in range(len(final_answer)):
            final_answer[i] = original_names[0][0] + ' = ' + Get_Solution_Value(final_answer[i])

    else:
        for i in range(len(answer)):
            sub_answer = []
            for var in variables:
                for j in range(len(answer[i])):
                    if Get_Solution_Name(answer[i][j]) == var:
                        sub_answer.append(answer[i][j])
            final_answer.append((sub_answer))
        
        #lay lai ten cu cho bien
        for i in range(len(original_names)):
            for x in range(len(final_answer)):
                for y in range(len(final_answer[x])):
                    if Get_Solution_Name(final_answer[x][y]) == original_names[i][1]:
                        final_answer[x][y] = original_names[i][0] + ' = ' + Get_Solution_Value(final_answer[x][y])
        
        #dua cac phan tu con thanh dang tuple
        for i in range(len(final_answer)):
            final_answer[i] = tuple(final_answer[i])
        
    return set(final_answer)


def Check_Question_True_False(KB, question):
    final_answer = True
    stack = [] #stack chua cac tap goal
    known_events = Get_Known_Events(KB)
    question = Eliminate_Spaces(question)

    #loai bo dau cham cuoi cau hoi
    if question[-1] == '.':
        question = question[:-1]


    #Truong hop cau hoi khong the suy dien lui
    if Cannot_Backward_Chaining(KB, question):
        if question in known_events:
            return True
        else:
            return False 

    #Truong hop can phai suy dien lui de tim ra cau tra loi
    defination = Get_Defination_By_Name(KB, question)
    
    sub_predicates = Separate_Sentence(defination, ';')
    for i in range(len(sub_predicates)):
        stack.append(Separate_Sentence(sub_predicates[i], ','))
    # print('stack: ', stack)
    while stack:
        goal = stack.pop()
        count = 0 #dem xem co bao nhieu vi tu trong goal khong suy dien duoc nua

        for i in range(len(goal)):
            if Cannot_Backward_Chaining(KB, goal[i]) == False:
                new_elements = Separate_Sentence(Get_Defination_By_Name(KB, goal[i]), ';')
            
                if len(new_elements) > 1:
                    for element in new_elements:
                        goal[i] = element
                        stack.append(goal)
                    break
                else:
                    new_predicates = Separate_Sentence(Get_Defination_By_Name(KB, goal[i]), ',')

                    #loai bo goal[i] va them vao cac phan tu thay the
                    goal.pop(i)
                    goal.extend(new_predicates)
                    stack.append(goal)
                    break
            else:
                count += 1

        #neu tat ca cac vi tu trong goal deu khong suy dien duoc nua
        # print('GOAL: ', goal)
        if count == len(goal):
            general_answers = []
            answers = []
            check = True
            #duyet qua tat ca cac vi tu trong goal, neu co vi tu nao khong nam trong su kien da biet thi cau tra loi la False
            for j in range(len(goal)):
                # print('=======================================')  
                # print('goal[j]: ', goal[j])
                if Have_Differential_Cond(goal[j]):
                    condition = goal[j]
                    #chuyen dieu kien ve cuoi de xet sau
                    if j != count - 1:
                        goal[j] = goal[count-1]
                        goal[count-1] = condition
                    else:
                        temp = Reject_Solution_By_Cond(general_answers, condition)
                    if temp:
                        final_answer = True
                    else:
                        final_answer = False
                        break
                else:
                    
                    if goal[j] not in known_events:
                        check = False 
                        #neu day la mot vi tu khong co bien
                        if Get_Valuable_Pos(goal[j]) == -1:
                            final_answer = False
                            break
                        #neu day la vi tu co chua bien thi tim xem bien co gia tri nao phu hop khong
                        else:
                            answers = list(Find_Answer(KB, goal[j]))
                            # print()
                            # print('ANSWER: ', answers)
                            # print()
                            #neu khong tim duoc gia tri cua bien thi vi tu la sai
                            if len(answers) == 0:
                                final_answer = False
                                break
                            else:
                                general_answers = Find_General_Solutions(answers, general_answers)
                        # print()
                        # print('GENERAL: ', general_answers)
                        # print()
                    else:
                        final_answer = True
            if (len(general_answers) == 0) and (check == False):
                final_answer = False
            #neu co 1 tap ket luan  goal trong stack la dung thi menh de duoc chung minh
            if final_answer == True:
                break
    return final_answer


