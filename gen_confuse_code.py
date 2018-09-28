# -*- coding: utf-8 -*-
import random
import os,shutil
import string,sys,json;
import time
import datetime
import hashlib 

reload(sys);
sys.setdefaultencoding("utf-8");

FILE_PATH = os.path.split(os.path.realpath(sys.argv[0]))[0];
DEAULT_DST_PATH = os.path.join(FILE_PATH, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'));

FUNCTION_BEGIN_WORDS = ['gen', 'get', 'set', 'check', 'change', 'fix', 'adjust', 'attack', 'treat', 'upgrade', 'update', 'load', 'init', 'draw', 'reload'];
FUNCTION_MIDDLE_WORDS = ['Big', 'Small', 'Old', 'New', 'Young', 'Short', 'Long', 'Wid', 'Huge', 'Test', 'Preview', 'Red', 'Green', 'Blue', 'Yellow', 'Gray', 'Quick', 'Slow', 'Good', 'Bad', 'Cude', 'Randge', 'Circle', 'Rect', 'Round', 'Lucky', 'Usefull', 'Select'];

COMMON_WORDS = ['Entity', 'Fruit', 'Enemy', 'Hero', 'Object', 'Computer', 'Animal', 'Vegetable', 'Money', 'Interface', "Listener", 'Code', 'Writeable', 'WithChannelObject', 'WithSkillObject', 'Food', 'Park']

VARIABLE_WORDS = [
                ('bool', 'cando'),
                ('bool', 'call'),
                ('bool', 'created'),
                ('int', 'count'),
                ('int', 'size'),
                ('int', 'type'),
                ('int', 'createcount'),
                ('float', 'time'),
                ('float', 'createtime'),
                ('float', 'updatetime'),
                ('float', 'delttime'),
                ('NSString*', 'name'),
                ('NSString*', 'nick'),
                ('NSString*', 'token'),
                ('NSString*', 'owner'),
                ('NSString*', 'describe')];

MANAGER_VARIABLE_WORDS = [
                ('bool', 'inited'),
                ('NSMutableArray*', 'items')];

_base_class_func_name_arr = []
_base_class_vars_name_arr = []

_pre_name = ''
def mkdir_if_noexist(path):
    if not os.path.exists(path):
        os.makedirs(path);

def mkdir_and_romove_old(path):
    if os.path.exists(path) == True:
       shutil.rmtree(path)

    os.makedirs(path) ;
    pass

def get_elements_by_random(array, count):
    new_array = []
    selected_map = []

    while len(new_array) < count:
        item = random.choice(array)
        if item not in new_array:
            new_array.append(item)
        
    return new_array

def get_type_flag(type):
    if type == 'int':
        return '%d'
    elif type == 'float':
        return '%f'
    elif type == 'double':
        return '%d'
    elif type == 'bool':
        return '%d'
    elif type == 'NSString':
        return '%@'   
    return '%@'

def get_type_random_value(type):
    if type == 'int':
        return '%d' % random.uniform(1, 10000)
    elif type == 'float':
        return '%ff' % random.random()
    elif type == 'double':
        return '%fd' % random.random()
    elif type == 'bool':
        if random.random() > 0.5:
            return 'true'
        else:
            return "false"
    elif type == 'NSString*':
        t1 = 'cflgjdpbtxwzrs'
        t2 = 'aeiou'
        str = ''
        length = random.uniform(3, 10)
        for x in xrange(1,int(length)):
            if x == 1 or x == 3 or x == 5:
                str = str + random.choice(t1)
            else:
                str = str + random.choice(t2)
        return '@\"' + str + '\"'
    elif type == 'NSMutableArray*':
        return '[NSMutableArray arrayWithCapacity:%d];' % random.uniform(1, 10)
    return '@\"' + 'semgilo' + '\"'

def upper_first_char(str):
    return str.title()

def write_variable_in_h(file, type, name):
    # print 'add a variable type = ' + type + ', name = ' + name
    file.write('\t%s _%s;\n' % (type, name))

def write_variables_in_h(file, variables):
    for var in variables:
        if var[0] != 'NSString*' and var[0] != 'NSMutableArray*':
            write_variable_in_h(file, var[0], var[1])

def write_property_in_h(file, type, name):
    # print 'add a property type = ' + type + ', name = ' + name
    file.write('@property (nullable, nonatomic, copy) %s %s;\n' % (type, name))

def write_propertys_in_h(file, variables):
    for var in variables:
        if var[0] == 'NSString*' or var[0] == 'NSMutableArray*':
            write_property_in_h(file, var[0], var[1])

def write_set_and_get_func_in_h(file, type, name):
    # print 'add a variable type = ' + type + ', name = ' + name
    file.write('- (void) set%s:(%s)%s;\n' % (upper_first_char(name), type, name))
    file.write('- (%s) get%s;\n' % (type, upper_first_char(name)))

def write_set_and_get_funcs_in_h(file, variables):
    # print 'add a variable type = ' + type + ', name = ' + name
    for var in variables:
        if var[0] != 'NSString*' and var[0] != 'NSMutableArray*':
            write_set_and_get_func_in_h(file, var[0], var[1])
            file.write("\n")

def write_set_and_get_func_in_m(file, type, name):
    # print 'add a variable type = ' + type + ', name = ' + name
    set_func_name = 'set%s' % upper_first_char(name)
    set_func_content = '\t_%s = %s;\n' % (name, name)
    write_func(file, set_func_name, 'void', [(type, name)], set_func_content)
    file.write("\n")
    get_func_name = 'get%s' % upper_first_char(name)
    get_func_content = '\treturn _%s;\n' % name
    write_func(file, get_func_name, type, [], get_func_content)

def write_set_and_get_funcs_in_m(file, variables):
    for var in variables:
        if var[0] != 'NSString*' and var[0] != 'NSMutableArray*':
            write_set_and_get_func_in_m(file, var[0], var[1])
            file.write("\n")


def write_property_in_m(file, type, name):
    file.write('@synthesize %s;\n' % name)

def write_propertys_in_m(file, variables):
    for var in variables:
        if var[0] == 'NSString*' or var[0] == "NSMutableArray*":
            write_property_in_m(file, var[0], var[1])

def write_func(file, name, return_type, args, content, isstatic=False):
    if isstatic:
        file.write('+ ')
    else:
        file.write('- ')

    file.write('(%s)' % return_type)
    file.write(name)
    for arg in args:
        file.write(':(%s)%s ' % (arg[0], arg[1]))
    file.write('\n')
    file.write('{\n')
    file.write(content)
    file.write('}\n')


def gen_pre_name():
    elements = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    return random.choice(elements) + random.choice(elements)
def gen_child_variables(element, ):
    pass

def gen_h_file(parent_dir, classname, variables, extend_classname=''):
    # print(parent_dir, classname, variables, extend_classname)
    path = os.path.join(parent_dir, classname + '.h')

    file = open(path, 'w');

    # info
    file.write("/*----------------------------------------------------\n")
    file.write(' %s.h\n'%(classname))
    file.write(' create time ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
    file.write("----------------------------------------------------*/\n")
 
    if extend_classname == '':
        # import
        file.write('#import <UIKit/UIKit.h>\n')

        # content
        file.write('@interface %s : UIViewController {\n' % classname)
        write_variables_in_h(file, variables)
        file.write('}\n')

        write_propertys_in_h(file, variables)

        file.write('- (NSString*) getInfo;\n')

        write_set_and_get_funcs_in_h(file, variables)
    else:
        # import
        file.write('#import \"%s.h\" \n' % extend_classname)
        
         # content
        file.write('@interface %s : %s {\n' % (classname, extend_classname))
        write_variables_in_h(file, variables)
        file.write('}\n')

        write_propertys_in_h(file, variables)
        file.write('- (NSString*) getInfo;\n')
        write_set_and_get_funcs_in_h(file, variables)

    file.write('\n\n@end')
    file.close()

def gen_m_file(parent_dir, classname, variables, extend_classname):
    path = os.path.join(parent_dir, classname + '.m')

    file = open(path, 'w');

    file.write('#import \"%s.h\" \n' % classname)

    file.write('@implementation %s \n\n' % classname)

    write_propertys_in_m(file, variables)

    # init function
    init_func_content = ''
    for var in variables:
        if var[0] == "NSString*":
            init_func_content = init_func_content + ('\tself.%s = %s;\n' % (var[1], get_type_random_value(var[0])))
        else:
            init_func_content = init_func_content + ('\t[self set%s:%s];\n' % (upper_first_char(var[1]), get_type_random_value(var[0])))
        
    init_func_content = init_func_content + '\treturn [super init];\n'
    write_func(file, 'init', 'id', [], init_func_content)

    # getInfo function
    info_func_content = '\tNSString* strInfo = nil;\n'
    if extend_classname != '':
        info_func_content = info_func_content + '\tNSString* strSuperInfo = [super getInfo];\n'

    format_content = ''
    format_args = ''
    index = 0
    for var in variables:
        format_content = format_content + var[1] + ' = ' + get_type_flag(var[0]) + ","
        if var[0] == 'NSString*':
            format_args = format_args + 'self.%s' % var[1]
        else:
            format_args = format_args + '[self get%s]' % upper_first_char(var[1])
        index = index + 1
        if index < len(variables):
            format_args = format_args + ','
    info_func_content = info_func_content + '\tstrInfo = [NSString stringWithFormat:@\"%s\", %s]; \n' % (format_content, format_args) 
    
    if extend_classname != '':
        info_func_content = info_func_content + '\tstrInfo = [NSString stringWithFormat:@\"%@%@\", strInfo, strSuperInfo]; \n'
    info_func_content = info_func_content + '\treturn strInfo;\n'

    write_func(file, 'getInfo', 'NSString*', [], info_func_content)

    write_set_and_get_funcs_in_m(file, variables)
    file.write('\n\n@end')
    file.close()

def gen_class(parent_dir, classname, extend_classname='', variables=[]):
    if len(variables) == 0:
        variables = get_elements_by_random(VARIABLE_WORDS, random.uniform(5, 10))
    gen_h_file(parent_dir, classname, variables, extend_classname)    
    gen_m_file(parent_dir, classname, variables, extend_classname)

def gen_manager_h_file(parent_dir, classname, variables, element_name, import_class_names):
    # print(parent_dir, classname, variables, extend_classname)
    path = os.path.join(parent_dir, classname + '.h')

    file = open(path, 'w');

    # info
    file.write("/*----------------------------------------------------\n")
    file.write(' %s.h\n'%(classname))
    file.write(' create time ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
    file.write("----------------------------------------------------*/\n")
 
    # import
    file.write('#import <UIKit/UIKit.h>\n')

    # content
    file.write('@interface %s : UIViewController {\n' % classname)
    write_variables_in_h(file, variables)
    file.write('}\n')

    write_propertys_in_h(file, variables)

    file.write('+ (id) sharedInstance;\n')

    file.write('- (void) create%sByName:(NSString*) name;\n' % element_name)
    file.write('\n')

    write_set_and_get_funcs_in_h(file, variables)
    
    file.write('\n\n@end')
    file.close()

def gen_manager_m_file(parent_dir, classname, variables, element_name, import_class_names):
    path = os.path.join(parent_dir, classname + '.m')

    file = open(path, 'w');

    file.write('#import \"%s.h\" \n' % classname)

    for cn in import_class_names:
        file.write('#import \"%s.h\" \n' % cn)

    file.write('@implementation %s \n\n' % classname)

    write_propertys_in_m(file, variables)


    # sharedInstance function
    file.write('static %s *instance = nil;\n' % classname)
    instance_func_content = ''
    instance_func_content = instance_func_content + '\tstatic dispatch_once_t once;\n'
    instance_func_content = instance_func_content + '\tdispatch_once(&once, ^{\n'
    instance_func_content = instance_func_content + '\t\tinstance = [[%s alloc] init];\n' % classname
    instance_func_content = instance_func_content + '\t});\n'
    instance_func_content = instance_func_content + '\treturn instance;\n'
    write_func(file, 'sharedInstance', classname + '*', [], instance_func_content, True)
    file.write('\n')

    # create function
    create_func_name = 'create%sByName' % element_name
    create_func_args = [('NSString*', 'name')]
    create_func_content = ''
    index = 0
    for cn in import_class_names:
        if index == 0:
            create_func_content = create_func_content + '\tif([name compare:@\"%s\"])\n' % cn
        else:
            create_func_content = create_func_content + '\telse if([name compare:@\"%s\"])\n' % cn

        create_func_content = create_func_content + '\t{\n'
        create_func_content = create_func_content + '\t\t%s *item = [[%s alloc] init];\n' % (cn, cn)
        create_func_content = create_func_content + '\t\tNSLog(@\"%@\", [item getInfo]);\n'
        create_func_content = create_func_content + '\t}\n'

        index = index + 1
    write_func(file, create_func_name, 'void', create_func_args, create_func_content)
    file.write('\n')

    # init function
    init_func_content = ''
    for var in variables:
        if var[0] == "NSString*" or var[0] == "NSMutableArray*":
            init_func_content = init_func_content + ('\tself.%s = %s;\n' % (var[1], get_type_random_value(var[0])))
        else:
            init_func_content = init_func_content + ('\t[self set%s:%s];\n' % (upper_first_char(var[1]), get_type_random_value(var[0])))
        
    init_func_content = init_func_content + '\treturn [super init];\n'
    write_func(file, 'init', 'id', [], init_func_content)

    write_set_and_get_funcs_in_m(file, variables)
    file.write('\n\n@end')
    file.close()


def gen_manager_class(parent_dir, classname, element_name, variables, import_class_names):
    # for i in xrange(0, len(variables)):
    #     var = variables[i]
    #     variables[i] = (var[0], )

    for var in MANAGER_VARIABLE_WORDS:
        variables.append(var)
    gen_manager_h_file(parent_dir, classname, variables, element_name, import_class_names)    
    gen_manager_m_file(parent_dir, classname, variables, element_name, import_class_names)

# CC
def gen_class_name(pre_name, modify_name, element_name):
    return pre_name + modify_name + element_name

def gen_fold_name():
	return random.choice(COMMON_WORDS)

def gen_element():
    
    pass

def gen_codes(dst_dir, fold_num = 5, class_num_per_dir = 10, delt_num = 3): 
    mkdir_and_romove_old(dst_dir);
    print 'output path : ' + dst_dir 
    fold_name_arr = get_elements_by_random(COMMON_WORDS, fold_num)

    all_class_info = {}
    for fold_name in fold_name_arr:
        print '-----generate element <' + fold_name + '>-----'
        element_name = fold_name
        fold_name = fold_name.lower() + 's'
        dir_path = os.path.join(dst_dir, fold_name)
        mkdir_and_romove_old(dir_path)

        

        # base class
        base_variables = get_elements_by_random(VARIABLE_WORDS, random.uniform(5, 10))
        base_classname = gen_class_name(_pre_name, 'Base', element_name)
        gen_class(dir_path, base_classname, '', base_variables)
        
        # files
        class_num = int(class_num_per_dir + random.uniform(-3, 3))
        sub_name_arr = get_elements_by_random(FUNCTION_MIDDLE_WORDS, class_num)
        import_class_names = []
        for y in xrange(0,class_num):
            classname = gen_class_name(_pre_name, sub_name_arr[y], element_name)
            import_class_names.append(classname)
            variables = get_elements_by_random(VARIABLE_WORDS, random.uniform(3, 10))
            for index in xrange(0,len(variables)):
                var = variables[index]
                variables[index] = (var[0], element_name.lower() + upper_first_char(var[1]))
            gen_class(dir_path, classname, base_classname, variables)

        all_class_info[element_name] = import_class_names
        
        # manager class
        manager_classname = gen_class_name(_pre_name, element_name, 'Manager')
        gen_manager_class(dir_path, manager_classname, element_name, base_variables, import_class_names)



    # readme file
    readme_file_path = os.path.join(dst_dir, "readme.txt")
    readme_file = open(readme_file_path, 'w')

    for x in xrange(1,10):   
        readme_file.write('-------------------- code %d ----------------------\n' % x)
        elements1 = get_elements_by_random(fold_name_arr, random.uniform(1, 4))
        
        import_content = ''
        operate_content = ''
        for name in elements1:
            manager_name = gen_class_name(_pre_name, name, 'Manager')
            import_content = import_content + '#import "%s.h"\n' % manager_name
            for y in xrange(1,int(random.uniform(3, 8))):
                operate_content = operate_content + '[[%s sharedInstance] create%sByName:@"%s"];\n' % (manager_name, name, random.choice(all_class_info[name]))
        
        readme_file.write(import_content)
        readme_file.write('\n')
        readme_file.write(operate_content)
        readme_file.write('\n\n')

    readme_file.close()


if __name__ == '__main__':
    _pre_name = gen_pre_name()
    gen_codes(DEAULT_DST_PATH, random.uniform(5, 10), 10, 3)

