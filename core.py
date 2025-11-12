text = "=IF(AND(A1<=1,A1>0),FLOOR(B1),IF(A1<=2,FLOOR(B2),0))"
target = """=
IF(
    AND(
        A1<=1,
        A1>0
    )
    ,
    FLOOR(
        B1
    )
    ,
    IF(
        A1<=2,
        FLOOR(
            B2
        )
        ,
        0
    )
)"""


def format_excel_formula(formula):
    """
    将单行 Excel 公式格式化为多行缩进格式

    Args:
        formula: 单行 Excel 公式字符串，例如 '=IF(AND(B6<=-1.5%,B6>-4%),FLOOR(0.5*B4,100),0)'

    Returns:
        格式化后的多行字符串
    """
    if not formula:
        return ""

    # 移除首尾空格
    formula = formula.strip()

    # 如果以等号开头，单独处理等号
    result = []
    if formula.startswith("="):
        result.append("=")
        formula = formula[1:].strip()

    indent_level = 0
    indent_size = 4
    i = 0
    current_token = []

    while i < len(formula):
        char = formula[i]

        if char == "(":
            # 左括号：输出函数名和左括号，换行，增加缩进
            token = "".join(current_token).strip()
            if token:
                result.append(" " * indent_level + token + "(")
            else:
                result.append(" " * indent_level + "(")
            current_token = []
            indent_level += indent_size
            i += 1
        elif char == ")":
            # 右括号：先输出当前token（如果有），减少缩进，换行，输出右括号
            if current_token:
                token = "".join(current_token).strip()
                if token:
                    result.append(" " * indent_level + token)
                current_token = []
            indent_level -= indent_size
            result.append(" " * indent_level + ")")
            i += 1
        elif char == ",":
            # 逗号：输出当前token和逗号，换行
            token = "".join(current_token).strip()
            if token:
                result.append(" " * indent_level + token + ",")
            else:
                result.append(" " * indent_level + ",")
            current_token = []
            i += 1
        else:
            # 其他字符：添加到当前token
            current_token.append(char)
            i += 1

    # 处理最后剩余的内容
    if current_token:
        token = "".join(current_token).strip()
        if token:
            result.append(" " * indent_level + token)

    return "\n".join(result)


# 测试
if __name__ == "__main__":
    formatted = format_excel_formula(text)
    print("原始公式:")
    print(text)
    print("\n格式化后:")
    print(formatted)
    print("\n目标格式:")
    print(target)
    print("\n是否匹配:", formatted == target)
