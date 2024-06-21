def rename(name) -> str:
    new_name = ""

    ALLOWED_CHAR = "!?^&-,()[]*$@%#:;'\"+=_ "

    if "u0026" in name:
        name = name.replace("\\", "").replace("u0026", "&")
    for i in range(len(name)):
        c = name[i]
        if not c.isalnum() and c not in ALLOWED_CHAR:
            new_name += ""
        else:
            new_name += name[i]

    return new_name