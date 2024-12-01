import logging
import time
from datetime import datetime

from django.db import connection

logger = logging.getLogger(__name__)


class QueryLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        end_time = time.time()

        if "http://testserver" not in request.build_absolute_uri():
            date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            if response.status_code >= 400:
                logger.error(
                    f"{date}, "
                    f"Запрос: {request.method} {
                        request.build_absolute_uri()
                    }, "
                    f"IP-адрес: {
                        request.META.get('REMOTE_ADDR', 'Неизвестно')
                    }, "
                    f"Статус ответа: {response.status_code}, "
                    f"Пользователь: {
                        request.user if request.user.is_authenticated
                        else 'Аноним'
                    }, "
                    f"Параметры POST: {dict(request.POST)}"
                )
            else:
                total_time = end_time - start_time
                queries = len(connection.queries)
                logger.info(
                    f"{date}, "
                    f"Запрос: {request.method} {
                        request.build_absolute_uri()
                    }, "
                    f"Время выполнения: {total_time:.2f}s, "
                    f"SQL запросов: {queries}."
                )

                for query in connection.queries:
                    logger.debug(
                        f"SQL: {query['sql'][:100]}... | Время: {
                            query['time']
                        }с"
                    )

        return response
