## CryptoFluctuationDetector
### Ефремов Егор Сергеевич
Это тестовое задание на позицию **Python-разработчик (Junior)**

 1. Для того чтобы определить собственные движения цены фьючерса
		ETHUSDT, я использовал метод регрессинного анализа. 
 2. Данные брал с api сайта binance. 
 3. Сначала взял данные с промежутком в одну неделю. Осознал, что
	    получается слишком неточный результат, поэтому решил взять
	    промежуток в один день.
 4. Занёс все значения в Excel и с помощью встроенной функции
	    "Регрессия" во вкладке Анализ данных получил зависимость ETHUSDT от
	    BTCUSDT.
 5. Построил диаграмму и добавил линию тренда.

## Пример вывода в консоль

![Пример вывода в консоль](https://github.com/EfremovEgor/CryptoFluctuationDetector/blob/main/images/output.png?raw=true)