## ImageMover &mdash; mini-GUI для ускорения доразметки


### Предыстория
Идея создания этого скромного GUI возникла в процессе подготовки изображений для обучения нейронной сети ResNet152. В проекте, над которым я работал, на тот момент уже была обученная мною версия классификатора. Однако качество работы не совсем устраивало. При помощи некоторых скриптов удалось получить более 120.000 изображений. Каждая картинка прошла через тот самый классификатор, и большинство классов было предсказано верно, но, тем не менее, не все. Работать с таким большим количеством изображений напрямую из файлового менеджера было очень неудобно, отсюда и родилась идея написать специальный GUI. 

### Основная идея
Нужно распределить 
