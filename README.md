## ImageMover &mdash; GUI для ускорения доразметки

### Предыстория
Идея создания этого скромного GUI возникла в процессе подготовки изображений для обучения нейронной сети ResNet152. В проекте, над которым я работал, на тот момент уже была обученная версия классификатора. Однако качество работы не совсем устраивало. При помощи некоторых скриптов удалось получить более 120.000 изображений. Каждая картинка прошла через тот самый классификатор, и большинство классов было предсказано верно, но, тем не менее, не все. Работать с таким большим количеством изображений напрямую из файлового менеджера было очень неудобно, отсюда и родилась идея написать специальный GUI. 

### Основная идея
Есть 3 папки с изображениями, каждая из них соответствует одному из трех классов. Большинство изображений изначально находится в нужной папке. Ошибок, однако, все равно достаточно много, поэтому нужно посмотреть весь датасет вручную. GUI ускоряет процесс переноса изображений в другие папки за счет того, что выводит на экран сразу 15 изображений. Также, GUI дает возможность отменить любое количество действий, вернувшись, таким образом, в любое предыдущее состояние. Помимо всего прочего, у данного интерфейса реализована возможность сохранения контрольной точки в отдельный файл.

### Функционал
При включении открывается стартовое окно, в которое нужно вписать пути до директорий с изображениями. Основная папка - папка, картинки которой нужно перебрать. После того, как все пути введены, нужно нажать кнопку "Начать". После этого, в окне появятся 15 изображений, расположенных в 3 ряда по 5 штук, сжатых до размера 224х224, а также кнопки: "class2", "Далее", "class3", "Отмена", "Сохранить". Кнопки "class2" и "class3" будут иметь названия папок, которые были указаны в начальном окне. Они отвечают за перенос выбранных изображений в папку. Чтобы выбрать одну или несколько картинок, достаточно просто на нее нажать. Беспокоится за то, что при переносе из-за возможного совпадения имен файлы перезапишутся, и произойдет потеря данных, не нужно. Перемещенным файлам будет дано новое название. Кнопка "Далее" оставляет изображения на месте. Кнопка "Отмена" отменяет предыдущее действие, ей можно пользоваться любое количество раз. В программе также предусмотрена возможность сохранения прогресса в pickle-файл. Для этого нужно нажать кнопку "Сохранить". Для того, чтобы загрузиться из pickle-файла, нужно нажать кнопку "Загрузить" в стартовом окне. 

P.S. Все картинки внутри папок должны иметь названия в формате "номер.jpg/.png/.jpeg".

![ImageMover](https://raw.githubusercontent.com/slarkslarkshark/ImageMover/547a7b5421e756bb875a2751d4714fb276a4eb1e/ImageMover.png)
