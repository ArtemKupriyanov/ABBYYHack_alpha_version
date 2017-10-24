# utf-8


def get_employee_duties(input_text):
    """

    :param input_text: string with input text from photo
    :return: list with responsibilities
    """

    employ_variants = ['Работник обязан',
                       'Обязанности работника',
                       'Права и обязанности работника',
                       ]

    with open("employment_contract_sample.txt", "r", encoding='utf-8') as file:
        sample_doc = file.read().replace("_", "")

    start_pos = -1

    for variant in employ_variants:
        start_pos = sample_doc.find(variant)
        if start_pos != -1:
            break

    finish_pos = start_pos + 1
    while sample_doc[finish_pos] != "\n" or sample_doc[finish_pos + 1] != "\n":
        finish_pos += 1

    responsibilities = []
    current_index = start_pos
    temple_duty = ""

    while current_index < finish_pos and current_index < len(input_text):
        if sample_doc[current_index] != "\n":
            temple_duty += sample_doc[current_index]
        else:
            responsibilities.append(temple_duty)
            temple_duty = ""
        current_index += 1

    return responsibilities
