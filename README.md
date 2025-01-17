Задача 1.
Использовать Python 3.10 и asyncio.

Есть сервер и 2 клиента в разных процессах. Сервер слушает TCP порт, клиенты при запуске коннектятся к нему. Всё общение идёт только клиент-сервер и только через данное TCP соединение в виде сообщений ASCII текстом с переводом строки в конце сообщения одним байтом 0x0a.

Клиенты со случайными интервалами от 300 до 3000мс шлют на сервер сообщения в формате:
- порядковый номер запроса в десятичном виде (начинается с 0) в квадратных скобках;
- через пробел слово PING.

Сервер, получив запрос, с 10% вероятностью его игнорирует. В остальных случаях засекает случайный интервал от 100 до 1000 мс, после чего отвечает клиенту сообщением:
- в квадратных скобках порядковый номер ответа (начинается с 0), дробь и порядковый номер запроса, на который даётся ответ;
- через пробел слово PONG;
- через пробел, в круглых скобках порядковый номер клиента (по времени их подключения, начиная с 1).

Также раз в 5 секунд сервер шлёт всем подключенным клиентам:
- в квадратных скобках порядковый номер ответа;
- через пробел слово keepalive.

Все ответы сервера имеют сквозную нумерацию вне зависимости какое сообщение и какому клиенту отправляется.

Сервер должен вести лог-файл, в который сохранять строки со следующими значениями, разделёнными точкой с запятой:
- дата в формате ГГГГ-ММ-ДД;
- время получения запроса в формате ЧЧ:ММ:СС.ССС;
- текст запроса;
- время отправки ответа в таком же формате;
- текст ответа.
Для проигнорированных сообщений 2 последних параметра заменить на строку "(проигнорировано)".

Клиенты должны вести свои логи со строками в формате:
- дата;
- время отправки запроса;
- текст запроса;
- время получения ответа или таймаута;
- текст ответа или строку "(таймаут)".
Для сообщений keepalive атрибуты запроса в логе должны быть пустыми.

Сервер и 2 клиента необходимо запустить, прервать через 5 минут.
Предоставить исходный код и сохранённые логи.
Код будет анализироваться на читаемость, грамотность, адекватность. Логи на корректность работы и соблюдение требований.
Даётся максимум одна повторная попытка сдать задачу после работы над ошибками.