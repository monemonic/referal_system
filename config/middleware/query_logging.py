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
            request_url = request.build_absolute_uri()
            remote_addr = request.META.get("REMOTE_ADDR", "Неизвестно")
            user = request.user if request.user.is_authenticated else "Аноним"

            if response.status_code >= 400:
                logger.error(
                    f"{date}, "
                    f"Запрос: {request.method} {request_url}, "
                    f"IP-адрес: {remote_addr}, "
                    f"Статус ответа: {response.status_code}, "
                    f"Пользователь: {user}, "
                    f"Параметры POST: {dict(request.POST)}"
                )
            else:
                total_time = end_time - start_time
                queries = len(connection.queries)
                logger.info(
                    f"{date}, "
                    f"Запрос: {request.method} {request_url}, "
                    f"Время выполнения: {total_time:.2f}s, "
                    f"SQL запросов: {queries}."
                )

                for query in connection.queries:
                    sql_snippet = (
                        query['sql'][:100] + "..." if len(query['sql']) > 100
                        else query['sql']
                    )
                    query_time = query['time']
                    logger.debug(
                        f"SQL: {sql_snippet} | "
                        f"Время: {query_time}с"
                    )

        return response
