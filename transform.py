
letters_dict = {
    'A': 'А',
    'B': 'В',
    'C': 'С',
    'E': 'Е',
    'H': 'Н',
    'K': 'К',
    'M': 'М',
    'O': 'О',
    'P': 'Р',
    'T': 'Т',
    'X': 'Х'
}


def transform_to_1c(message):
    message = message.upper().strip()
    valid_designation = ''
    for i in message:
        if i not in '.!@#$%^&*,()_=+:/?':
            valid_designation += i
    designation_split = valid_designation.split('-')
    if len(designation_split) > 2:
        designation_split = eng_rus_letters(valid_designation.split('-'))
    designation_split[0] = (designation_split[0]
                            + ('х' * (7 - len(designation_split[0]))))
    designation_split[1] = (('0' * (7 - len(designation_split[1])))
                            + designation_split[1])
    designation = '-'.join(designation_split)
    return designation


def eng_rus_letters(transform_list):
    for i in range(2, len(transform_list)):
        x = list(transform_list[i])
        for j in range(len(x)):
            if x[j] in letters_dict.keys():
                x[j] = letters_dict[x[j]]
        transform_list[i] = ''.join(x)
    return transform_list
