import functools
import sys
from typing import Any, Callable, Optional, TypeVar, cast

# Типизация для сохранения сигнатуры оборачиваемых функций
F = TypeVar("F", bound=Callable[..., Any])


def log(filename: Optional[str] = None) -> Callable[[F], F]:
    """Декоратор, который логирует вызовы функций в файл или консоль."""

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                # Успешное выполнение функции
                result = func(*args, **kwargs)
                log_message = f"{func.__name__} ok\n"
                
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(log_message)
                else:
                    sys.stdout.write(log_message)
                    
                return result

            except Exception as e:
                # Обработка и логирование ошибки
                error_type = type(e).__name__
                log_message = f"{func.__name__} error: {error_type}. Inputs: {args}, {kwargs}\n"
                
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(log_message)
                else:
                    sys.stdout.write(log_message)
                
                raise e  # Пробрасываем ошибку дальше, чтобы не нарушать логику программы

        return cast(F, wrapper)

    return decorator
