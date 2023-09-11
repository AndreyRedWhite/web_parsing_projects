# vistaauction.com parsing project


In this project, data was collected from the website https://vistaauction.com/. The client required gathering all the lots that met his criteria (maximum values of MSRP and BID).

## Three functions were created in this project:

##### get_pagination: 
This function is responsible for finding the last page to set the pagination value. It returns the pagination number.

##### get_lot_time:
The time for each lot is dynamically loaded using JavaScript scripts. However, the project's page itself statically specifies the start and end times of the auction. Using these values and obtaining the current time considering the site's time zone, the time for each lot is calculated. This function takes the URL of the lot as an argument and returns a string with the lot's time.

##### parse_page:
The main function of the module. It receives the pagination value obtained from **get_pagination()** as input. Using the **requests** library, each page from the pagination is fetched. Then, each page is parsed using the **BeautifulSoup** library, and the necessary elements are searched for. Compliance with the conditions is checked, and the satisfying lots are recorded in the result.csv file.

## Russian translate

В данном проекте был реализован сбор данных с сайта https://vistaauction.com/. Заказчику требовалось собирать все лоты, удовлетворяющие его условиям (предельные значения MSRP и BID).

В проекте были созданы 3 функции:
##### get_pagination
Данная функция отвечает за поиск последней страницы для задания значения пагинации. Возвращает чилсо пагинации.

##### get_lot_time
Время каждого лота подгружается динамически с использованием js скриптов. Однако на самой странице проекта статично заданы время начала аукциона и время завершения. Используя эти значения и получая текущее время с учетом time-зоны сайта, высчитывается время для каждого лота. 
В качестве аргумента данная функция получает url лота, возвращает строку с временем лота.

##### parce_page
Основная функция модуля. На вход получает значение пагинации, полученное из **get_pagination()**.
С помощью библиотеки **requests** забирается каждая страница из пагинации. Далее каждая страница разбирается с помощью библиотеки **BeautifulSoup** и ищутся нужные элементы. Проверяется соответствие условиям и удовлетворяющие лоты записываются в файл result.csv.
