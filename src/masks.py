def get_mask_card_number(card_number: str) -> str:

    if len(card_number) != 16 or not card_number.isdigit():
        return "Некорректный номер карты"

    first_block = card_number[:4]
    second_block = f"{card_number[4:6]}**"
    third_block = "****"
    fourth_block = card_number[12:]

    return f"{first_block} {second_block} {third_block} {fourth_block}"


def get_mask_account(account_number: str) -> str:

    if len(account_number) < 4 or not account_number.isdigit():
        return "Некорректный номер счета"

    last_four = account_number[-4:]
    return f"**{last_four}"
