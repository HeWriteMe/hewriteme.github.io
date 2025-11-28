def format_label(label):
    if(label == 'hieronymous'):
        formatted_label = 'Hieronmyous Bosch'
    else:
        formatted_label = label.replace("-", " ").title()
    return formatted_label
