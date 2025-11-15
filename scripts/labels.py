def format_label(label):
    if(label == 'dreams'):
        formatted_label = 'Dreamz'
    else:
        formatted_label = label.replace("-", " ").title()
    return formatted_label
