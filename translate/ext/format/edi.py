







# TODO refatorar for com enumerate(fild)...
#
RMV_SUBSTRIN = {
#    "[SPREAD": "]",
#    "[ARQUIVO1": "]",
#    "[CABECALHO]": "[/CABECALHO]",
#    "[/SPREAD]": "[/SPREAD]",
#    "[REGISTRO": "]",
    "| TAMANHO": "]",
}

TRANSLATE_STRING = {
    chr(34): chr(39),
    "trim": "RTRIM",
    "TRIM": "RTRIM",
    "Trim": "RTRIM",
    "[CAMPO NOME=|": "",
    "| TAMANHO": ",| TAMANHO",
}
TAGS = {"WHERE": "WHERE", "CAMPOS": "SELECT", "FROM": "FROM", "ORDEM": "ORDER BY"}
CHAR_PATEN = ("[", "]")
RMV_TAGG = ["CABECALHO"]

RMV_LINE_CONTENT = [
    "[SPREAD",
    "[/SPREAD]",
    "[ARQUIVO",
    "[/ARQUIVO",
    "[REGISTRO",
    "[/REGISTRO",
    "[EDI]",
    "[/EDI]",
]


def tags(tag):
    char_paten1, char_paten2 = CHAR_PATEN
    str_start = f"{char_paten1}{tag}{char_paten2}"
    str_end = f"{char_paten1}/{tag}{char_paten2}"
    return str_start, str_end


def translate_tag(script):

    for tag, command in TAGS.items():
        tag_start, tag_end = tags(tag)
        script = script.replace(tag_start, command)
        script = script.replace(tag_end, "")

    return script

def get_substring(script, str_start, str_end):
    try:
        index_start = script.index(str_start)
        index_end = script.index(str_end)
        index_end += len(str_end)
        content = script[index_start:index_end]

    except ValueError as e:
        print(f"Error: {str_start},{str_end}: {e}")
        content = ""

    return content

def rmv_substring(script):

    for str_start, str_end in RMV_SUBSTRIN.items():
        
        found = True
        while found:
            rmv_conten = get_substring(script=script,str_start=str_start,str_end=str_end)
            script = script.replace(rmv_conten, "")

            found =  True if rmv_conten != "" else False

    return script

def translate_string(script):

    for old, new in TRANSLATE_STRING.items():
        if script.find(old) >= 0:
            script = script.replace(old, new)

    return script


def get_tag(script, tag):
    try:
        tag_start, tag_end = tags(tag)

        index_start = script.index(tag_start)
        index_end = script.index(tag_end)
        index_end += len(tag_end)

        content_tag = script[index_start:index_end]

    except ValueError as e:
        content_tag = ""

    return content_tag


def rmv_tag(script, tag):

    rmv_tag = get_tag(script=script, tag=tag)
    script = script.replace(rmv_tag, "")

    return script


def get_content_tag(script, tag):

    str_start, str_end = tags(tag)
    content = get_tag(script, tag)
    content = content.replace(str_start, "").replace(str_end, "").strip()

    return content


def check_empty_tag(script, tag):
    return True if get_content_tag(script, tag) == "" else False


def rmv_tag_empty(script):
    for tag in TAGS:
        if check_empty_tag(script, tag):
            script = rmv_tag(script=script, tag=tag)
    return script


def rmv_tags(script):

    for tag in RMV_TAGG:
        rmv_content = get_tag(script, tag)
        script = script.replace(rmv_content, "")
    return script


def clean_script(list_script):
    list_remove = []

    for idx_scr in range(len(list_script)):
        for idx_rmv in range(len(RMV_LINE_CONTENT)):
            if list_script[idx_scr].find(RMV_LINE_CONTENT[idx_rmv]) >= 0:
                list_remove.append(idx_scr)

    try:
        list_remove.reverse()
        for idx in list_remove:
            del list_script[idx]

    except ValueError as err:
        print(f"content: {rmv}", f" Error: {err}")

    return list_script


###### - RUN
def to_sql(script):

    script_list = script.split(chr(13))
    script_list = clean_script(script_list)
    script = chr(13).join(script_list)

    script = rmv_tag_empty(script=script)
    script = translate_tag(script=script)
    script = rmv_tags(script=script)
    script = translate_string(script=script)
    script = rmv_substring(script=script)

    return script
'''
#Testes
content = "[CAMPO NOME=|'001'| TAMANHO=|5| ] \
            [CAMPO NOME=|'2'| TAMANHO=|2| ]\
"

print(
    to_sql(content)
) '''