import logging
from src.utils import read_excel_transactions
from src.views import generate_main_page

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("project.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

if __name__ == "__main__":
    logger = logging.getLogger("main")
    logger.info("Программа курсовой работы успешно запущена.")

    # Считываем транзакции из папки data
    transactions = read_excel_transactions("data/operations.xlsx")

    # Тестовый запуск генерации главной страницы
    result_json = generate_main_page("2026-10-20 14:30:00", transactions)
    print(result_json)
