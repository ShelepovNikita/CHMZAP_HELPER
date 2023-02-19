
def transform_to_1c(message):
    valid_designation = ''
    for i in message:
        if i not in '.!@#$%^&*,()_=+:/?':
            valid_designation += i
    designation_split = valid_designation.split('-')
    designation_split[0] = (designation_split[0]
                            + ('x' * (7 - len(designation_split[0]))))
    designation_split[1] = (('0' * (7 - len(designation_split[1])))
                            + designation_split[1])
    designation = '-'.join(designation_split)
    return designation
