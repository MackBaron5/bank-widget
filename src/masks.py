import logging
import os

# Создаем папку logs, если её нет
os.makedirs("logs", exist_ok=True)

# 1. Создаем объект логера для модуля masks
logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)

# 2. Настраиваем file_handler для записи в файл с перезаписью ('w')
file_handler = logging.FileHandler(
    "logs/masks.log", mode="w", encoding="utf-8"
)
file_handler.setLevel(logging.DEBUG)

# 3. Настраиваем формат записи логов
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)

# 4. Добавляем хендлер к логеру
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер карты в формат XXXX XX** **** XXXX."""
    card_str = str(card_number).replace(" ", "")

    if not card_str.isdigit() or len(card_str) != 16:
        # Логирование ошибочного случая (уровень ERROR)
        logger.error(
            f"Ошибка маскирования: неверный формат "
            f"номера карты '{card_number}'"
        )
        return ""

    masked = f"{card_str[:4]} {card_str[4:6]}** **** {card_str[12:]}"
    # Логирование успешного случая (уровень INFO)
    logger.info("Успешно маскирован номер карты")
    return masked


def get_mask_account(account_number: str) -> str:
    """Маскирует номер счета в формат **XXXX."""
    acc_str = str(account_number).replace(" ", "")

    if not acc_str.isdigit() or len(acc_str) < 4:
        logger.error(
            f"Ошибка маскирования: неверный формат "
            f"номера счета '{account_number}'"
        )
        return ""

    masked = f"**{acc_str[-4:]}"
    logger.info("Успешно маскирован номер счета")
    return masked
