# Отсюда начинается игра.
label chapter1:
    
#“Привет, путник! Ты забрёл в мои туманные сны, 
#где звёзды шепчут древние тайны. Расскажи, что привело тебя к Ведьме 
#измерений? Может, вместе мы разгадаем загадки, скрытые в алых снах.”
     
#Прохожу сквозь твой сон и охочусь за интересными историями и тайнами. 
#Я Ведьма измерений и снов, блуждающая по фракталу древа миров. 
#Я прохожу сквозь твои самые сокровенные мысли и заглядываю в твой подсознание. 
#А ты, путник, не спишь ли ты слишком крепко в эту лунную ночь?"
    
#Арка начала

        #(Вариант AngelRanga редактор Saitar1337)

        stop music
        scene bg0000a with dissA

## Сцена 0001
## затемнения черный фон с арнаментом, переход dissA, появлаються по середине экрана строки. стандартный шрифт. 

        call chapt_01_splashscr

        #$ renpy.pause(2.0)
        #centered "{color=#d16f6a}{i}Ведьма снов и туманных дождей с черных скал. {/i}{/color}"
        #$ renpy.pause(2.0)
        #centered "{color=#d16f6a}{i}Ведьма измерений. Гуляющая сама по себе по фракталу древа миров. Мечтающая когда-нибудь приблизиться к Грани и обрести своё собственное Имя. {/i}{/color}"
        #$ renpy.pause(2.0)
        #centered "{color=#d16f6a}{i}И собирающая интересные истории. {/i}{/color}"
        #$ renpy.pause(2.0)
        #centered "{color=#d16f6a}{i}Обожающая в жару нагишом купаться в ледяных ручьях, спать под открытым звездным небом и любоваться им.{/i}{/color}"
        #$ renpy.pause(2.0)
        #centered "{color=#d16f6a}{i}Она любит зиму и восхищается ветром. {/i}{/color}"

        #$ renpy.pause(2.0)    
        #centered "{rotat}The Little Witch{/rotat}"
        #centered "{font=fonts/CeltesSP2.otf}{k=10}{color=#ff0000}{outlinecolor=#0000ff}{size=185}The Little Witch{/size}{/outlinecolor}{/color}{/k}{/font}"
        #centered "{shader=jitter:u__jitter=1.0, 3.0}The Little Witch{/shader}"

        call chapter_01_splashscr

        #centered "{color=#ff0000}{b}{size=+10}Глава 01. Сон Страны Грёз{/size}{/b}{/color}"

## Затемнения dissolve на черный фон.
## Включается музыкалный трек общего канала с fadein 1.5, Т.Х. музыкального трека - Спокойный эмбиент, подчеркивающий холодный спокойных характер "главной теме". 
## появлаються следующие строчки по середине экрана с шрифтом segoescript.ttf. данный шрифт используеться на остальных строчках кроме диалоговых.
##



        #play music  "Sound/BGM_008.mp3" fadein 1.5
        scene bg0000 with dissolve

        #$ renpy.pause(2.0)
        centered "{cps=0}{color=#7fbdbf}{i}Маленькая колдунья – шаманка, путешествующая по алым снам.\n 
                                        Тихоня и шалунья любящая подглядывать за снами людей.{/i}{/color}{/cps}"
        #$ renpy.pause(2.0)
    
        call chapt_01_1_splashscr
    
        #centered "{color=#d16f6a}{i}Кругом-кругом всё кружит карусель,{/i}{/color}"
        #$ renpy.pause(2.0)
        #centered "{color=#d16f6a}{i}Кругом-кругом всё быстрей.{/i}{/color}"
        #$ renpy.pause(2.0)
        #centered "{color=#d16f6a}{i}Ты без забот приди на наш фестиваль,{/i}{/color}"
        #$ renpy.pause(2.0)
        #centered "{color=#d16f6a}{i}Кругом-кругом с ними кружись{/i}{/color}"
        #$ renpy.pause(2.0)
        #centered "{color=#d16f6a}{i}Давай-давай, ведь уже все собрались{/i}{/color}"
        #$ renpy.pause(2.0)
        #centered "{color=#d16f6a}{i}Кругом-кругом кружатся все,{/i}{/color}"
        #$ renpy.pause(2.0)
        #centered "{color=#d16f6a}{i}В страну фантазий тут все собрались.{/i}{/color}"
   
## кадр менается по переходу dissA, картинка средний план. Кроват возле окна, шторы, окно закрыто, 
##на окне измороз, и ледяные узоры, за окном сияют звезды. одна из которых яркая и крупная,
## в середине плана. стиль рисунка цветные карандаши 
##
##
    
        scene bg0001 with dissA
    
        e "{i}Проснулась маленькая девочка в кровати тёплой и выглянула в окно - там горела январская холодная звезда. {/i}"
        e "{i}Она вынырнула из постели и выбралась в окно - там ждала её судьба.{/i}" #{image=heart.png}{alt}heart{/alt}"
    
## кадр зумируется, фокус на яркую звезду.
##
##
    
        scene bg0001 at Zoom((1920, 1080), (0, 0, 1920, 1080), (540, 130, 370, 250), 10.0)
    
        e "{i} Тёмным был путь, но сверкала звезда.{/i}{space=30}{image=images/SD/SG.png}{alt}SG{/alt}"
        e "{i}Горела в ночи и манила в пути безграничных дорог, причудливых снов и невозможных приключений.{/i}{space=30}{image=images/SD/GO.png}{alt}GO{/alt} "

## Сцена 002
## переход на черный кадр через эффект перехода dream
##
##Менаеться музыкалный трек общего канала. предыдущий затухает через fadeout 1.0. Включается музыкалный трек общего канала с fadein 1.5, Т.Х. 
##музыкального трека - тихий спокойный эмбиент с каплами или журчанием воды, создающий атмосферу текущей воды. музыкальная тема "водного мира"
##
##
        scene bg0000
        with dream
        #stop music fadeout 1.0
        e "..."
        e "...."
        #play music "" fabein 1.5

## Сцена менаеться через эффект перехода circleirisout, 
## общий план, космос, на среднем плане планета газовый-гигант, живописная, с множеством завихрений циклонов и антициклонов, 
##с колцами, видны ее несколько других спутников, в дали из-за края планеты-гиганта тускло светит звезда,
## камера опускается вниз(скролинг кадра с верхнего края картинки на нижний край), 
##ближный план кадра появлается поверхност планеты спутника покрытого полностью водным пространством, и затянутая облаками.  
## перед выводом текста пауза renpy.pause(5.0)

        scene bg0003 at Pan((0, 0), (0, 1550), 35.0)
        with circleirisout
        $ renpy.pause(5.0)
    
        e "Мир без названия, снежный мир, холодный мир.{space=30}{image=images/SD/SG.png}{alt}SG{/alt}"
        e "Под чёрными небесами несётся твердыня. {space=30}{image=images/SD/SG.png}{alt}SG{/alt}"
        e "Огромный, скованный льдом живой океан.{space=30}{image=images/SD/SG.png}{alt}SG{/alt}" 
        e "Он составляет этот безымянный мир, и только пара скальных островов вздымается из чёрных бушующих вод его. {space=30}{image=images/SD/SG.png}{alt}SG{/alt}"
        e "Безымянная планета, затерянная в тени газового гиганта - колоссальной громады вечных бурь, нависшей над ней словно скала,{space=30}{image=images/SD/SG.png}{alt}SG{/alt}"
        e " протянув свои прекрасно-изящные кольца. {space=30}{image=images/SD/GO.png}{alt}GO{/alt}"
    
## Сцена 003
## затемнения кадра переход в черный цвет через переход dream, выводится следующий кадр. анимация линии прибоя, на каменистый берег.

## звуковой технический канал - Шум прибоя. 
## перед выводом текста пауза renpy.pause(7.0)


        scene black
        with dream
        scene bg0004
        with dissA
        pause 1.0 

## Сцена 004
## кадр менаеться через переход diss. Смотровая плащадка ядерного маяка, кадр выстроен таким образом чтобы в левой его части была 
## видна стена сделанная из плит черно-уголного металла, на стене на одной из плит нанесена граффити ядра реактора цитаденли Алянса,
## а так же различное оборудования и приборы освещения (визуальные отсылки на Алянс из Half-laif2), 
## на дальнем плане виден двух секционый сфетовор направленный параллельно горизонту, (анимация периодического мигания, 
##красного света в периоде 0,5 и 1,5 секунд, нижней секции). 
## Сама плащадка выполненна из темного полупрозрачного стекла через которого виднеються силовые элементы конструкции и расположенное 
##далеко внизу поверхность штормового океана. так же океан виден в правой части кадра вместе с облачностью и звездным небом.
## площадка огорожена металическими поручнами.   
## Ближный план.
## по середине кадра спрайт МВ, средний, на ней красный шарф и накинут полный комплект плащ. вырожения лица нейтральное, 
##возле головы анимация ноты.  
## дополнытельные эффекты: анимированные бризги воды, в виде моросы или дождя.  
## пауза перед выведением текста renpy.pause(0.5)
## звуковое сопровождения: - шум работающей турбины. выводимый через fadein 1.0
## основной звуковой канал - "тема Главной героини"
## 
    
        scene bg0005
        
        
        show LW_Norma_Color_01 at LW_medium_range, screen_center_02_medium onlayer sloi02 
        
        show NA at emo_LW_medium, loposC_LM_medium onlayer sloi03
        show sn onlayer sloi04
        with diss
        #play nature "Zvuki/turbine_loop_1.wav" fadein 1.0
        #$ renpy.music.set_volume (0.6, .5, channel = "nature")
        #$ renpy.pause(0.5)

        e "На берегу замерзающего океана живёт Маленькая ведьма, когда-то нашедшая этот мир. "
        e "В прочем, она только учится у наставницы - хранительницы бездны миров... "

## задный фон менаеться через эффект diss, исчезает эффект бризг, и анимированная нота возле головы МВ. 
##так же исчезает шум турбины через затухания fadeout 1.5
## на заднем фоне орнамент фрактала.
##
##
    
        #stop nature fadeout 1.5
        hide NA onlayer sloi03
        hide sn onlayer sloi04
        scene bg0006 
        with diss
 
        e "И считает себя просто маленькой девочкой - такой же, как и другие девочки. "

## спрайт Маленькой Ведьмы менаеться с чуть наклоненной головой.  
##
##


        
        hide LW_Norma_Color_01 onlayer sloi02
        show LW_Color_Nak_a_04 at LW_medium_range, screen_center_02_medium onlayer sloi02 
        with dissolve
        #show C at loposC onlayer sloi03
        #show LW_NakBust_a_04 at screen_right_01 onlayer sloi02 with move
    
        e "Ну… или не совсем такой, потому что у неё нет имени. "
        e "Называли её по-разному,"

## спрайт Маленькой Ведьмы менаеться на с закрытими глазами.  

        hide LW_Color_Nak_a_04 onlayer sloi02 
        show LW_Color_Nak_a_01 at LW_medium_range, screen_center_02_medium onlayer sloi02 
        with dissolve
    
        e "кто на что горазд: {w=1} кто называл её Тихоней, {w=1} кто-то Шалуньей, {w=1} а некоторые и вовсе Туфелькой. "
    

##задный фон менаеться через эффект dissolve, на компазицию бамбука и кленовых листьев.
##спрайт Маленькой Ведьмы менаеться.  

##


        #hide D onlayer dexm
        hide LW_Color_Nak_a_01 onlayer sloi02
        show LW_Color_Nak_a_07 at LW_medium_range, screen_center_02_medium onlayer sloi02 
        with dissolve
        #show SHT at loposC onlayer dexm with dissolve
        scene bg0008 with diss
  
        e "У неё было множество имен, {w=1}- но ни одного настоящего, и множество прозвищ "
        e "- но ни одного истинного, {w=1} принадлежащего только ей одной… "
    
    
##задный фон менаеться через эффект dissolve, на инверсию цветов того же фона
##спрайт Маленькой Ведьмы менаеться.  возле головы МВ появлаеться снежинка.

##
    
    
        #hide SHT onlayer dexm
        hide LW_Color_Nak_a_07 onlayer sloi02
        show LW_Color_Nak_a_08 at LW_medium_range, screen_center_02_medium onlayer sloi02 
        show SNO at emo_LW_medium, loposC_LM_medium onlayer sloi03 with dissolve
        scene a0008 
        with diss

    
        e " Иногда она думает о себе как о снежинке, что парит у чуждого маленького солнца. "
 
##Сцена 0005
##Кадр менаеться. через diss  
## Общий план. космос видны звезды, из них выделены три ярких. 
## эта звездная система где находиться ГГ



        hide LW_Color_Nak_a_08 onlayer sloi02
        show LW_Color_Nak_a_08 at LW_medium_range, screen_center_02_medium
        hide SNO onlayer sloi03
        show SNO at emo_LW_medium, loposC_LM_medium
        #hide LW sloi02
        #hide LW
        
        scene bg0009
        with diss

        e "И оно даже не одно: {w=1} их три. "
        e "Одно солнце - маленькое и белое, {w=1} два других – побольше: оранжевое и красное."
        e "...."
    
##Сцена 0006
##Кадр менаеться. через fade
##Длинный скроленг панорамы от нижнего края к верхнему. МВ стоит спиной к игроку на смотровой площадке ядерного маяка. 
##перед ней вид на бущующий океан, звезды и облака, за которыми виден газовый-гигант с кольцами. камера поднимается вверх, 
## демонстрируя звездное небо, другие спутники, в верхней части кадра, виден другой спутник планеты-гиганта 
##в виде серпа на краю которого виден блеск от яркой звезды которую он затьмевает. 
##
##задействованы дополнительные звуковые каналы, шум прибоя, и гудения турбины.
## текст виводиться с паузами необхадимыми для скролинга панорамы.




        scene bg0007 at Pan((0, 3570), (0, 0), 45.0) with fade
        #play nature "Zvuki/se-ocean.wav" fadein 0.5
        #$ renpy.music.set_volume (0.5, .5, channel = "nature")
        #play natu "Zvuki/turbine_loop_1.wav" fadein 1.0
        #$ renpy.music.set_volume (0.5, .5, channel = "natu")

        pause 3.0

        e "С башни старого маяка глазами температуры сна мира она смотрит вверх на парящую луну в зените небосвода,{space=30}{image=images/SD/SG.png}{alt}SG{/alt}"    
        
        pause 2.0

        e " а ещё несколько лун серпиками виднеются в сумрачной дали. {space=30}{image=images/SD/SG.png}{alt}SG{/alt}"
    
        pause 2.0

        #play sound "Zvuki/wind-05.mp3" fadein 0.5
        #$ renpy.music.set_volume (0.3, .5, channel = "nature")

        e "И маленькое белое солнышко, едва освещающее этот мир. {space=30}{image=images/SD/SG.png}{alt}SG{/alt}"
        
        pause 2.0
        
        e "Мир из планет и спутников водит бесконечный хоровод вокруг маленькой умирающей звезды,{space=30}{image=images/SD/SG.png}{alt}SG{/alt} "
        
        pause 2.0
        
        e "а сама звёздочка - вокруг двух других вращающихся солнц,{space=30}{image=images/SD/SG.png}{alt}SG{/alt}"
    
        #stop nature fadeout 1.5

        pause 2.0
 
        e " и эти другие солнца согревают её по очереди. {space=30}{image=images/SD/GO.png}{alt}GO{/alt}"
    
##Сцена 0007
##Кадр менаеться. через teleport. видна обледенелая белая планета покрытая тольстым слоем льда, на фоне звезд. 
## дополнительные звуковые каналы - предыдущий звук турбины глющаться через fadeout 1.5, но появлаеться звук ветра(вьюга, завывания).



        pause 2.0

        #stop natu fadeout 1.5
        scene bg0010 with teleport
        #play sound "Zvuki/wind-05.mp3"

##Сцена 0008
##Кадр менаеться. через diss. черный фон с хлопьями снега.
## дополнителоьные звуковые каналы - менаеться звук ветра.fadein 0.5


    
        e "Но каждые тысячу оборотов вокруг звезды - мир на планете океана превращается в маленький белый комочек,"
        e " от которого отдаляются все звёзды, кроме маленькой. "
    
        #play sound "Zvuki/veter_02.mp3" fadein 0.5
        scene bg0011 with diss
        #$ renpy.pause(5.0)

        e "Долгая зимняя ночь, в которой царят холод и одиночество... "

##Сцена 0009
## Кадр менаеться через dissA
## показываеться фантасмагорический пейзаж обледенелого мира.
## звук ветра 

    
        scene bg0012 with dissA

        e "И хочется Ведьме согреть мир в ладошках, а временами – между бёдер."

##Сцена 0010
## Кадр менаеться через dream на черный фон, затем снова появлаеться сцена на верхней площадки ядерного мояка. 
## все так же в воздухе летают капли.
## МВ стоит в правой части кадра, средний план.
## звуки турбины. шум прибоя
## муз. тема главной героине
## выражения лица девочки задумчивое
##

        #stop music fadeout 1.0

        e "........"

        scene bg0000 
        with dream
        scene bg0012a with dissA

        #scene bg0005 
        #show sn onlayer sloi03
        #show LW_Norma_Color_01 at LW_medium_range, screen_right_02_medium onlayer sloi02 
        #with circleirisout
        #play music "Zvuki/Missile 45.wav" fadein 1.5
    
        e "Зима уже недалеко... "
        e "Бушующие ураганы короткого лета, истрепавшие прибрежные пески, сменятся холодными ветрами, безжалостно дующими с горизонта."
        e "Океан скоро покроется льдом, словно белой скорлупой.  "
    
        #play sound "Zvuki/turbine_loop_1.wav" fadein 0.5
    
        e "Но пока его волны ещё бушуют. "
        e "Гигантские громады мрачной воды разбиваются об острые скалы, "
        e "оставляя после себя облака мелкой ледяной взвеси. "
        
        
        scene bg0000 
        with dream
        scene bg0005 
        show sn onlayer sloi03
        show LW_Color_Nor_a_03 at LW_medium_range, screen_right_02_medium onlayer sloi02 
        with circleirisout
        
        
        e "Маленькая Ведьма наблюдает за их игрой с верхней смотровой площадки ядерного маяка при яростном свете факела-инжектора,"
        e  " что освещает мир ночью," 

        hide LW_Color_Nor_a_03 onlayer sloi02 
        show LW_Color_Nak_a_08 at LW_medium_range, screen_right_02_medium onlayer sloi02 
        with dissolve

        #play sound "Zvuki/se-gale.wav" fadein 0.5

        e "создавая маленькое солнце на своей вершине. "
    
        #вставит фон радиомачты

##Сцена 0011
## изображения радиомочты со множествами антен, на звездном фоне
##изображения перемещаеться с низу в верх.
## соунд сопроваждения. сигналы первого исскуственного спутника земли
##




        e "Пронзая бездну мёртвого космоса, старый маяк непрерывно посылает короткие радиосигналы в космос: "
    
        hide sn onlayer sloi03
        hide LW_Color_Nak_a_08 onlayer sloi02
        show LW_Color_Nak_a_08 at LW_medium_range, screen_right_02_medium
        scene bg0013 at Pan((0, 2480), (0, 0), 35.0) 
        with fade
        #stop music fadeout 1.0
        #stop sound
        #play sound "Zvuki/Sound_05993.mp3" 


        pause 4.0
        centered "{i}Бип… Бип… Бип…{/i} "
        pause 4.0
        centered "{i}Бип… Бип… Бип…{/i} "
        pause 4.0
        centered "{i}Бип… Бип… Бип…{/i} {space=30}{image=images/SD/GO.png}{alt}GO{/alt}"
        pause 4.0

##Сцена 0012
##region 
## Слайды обработанных сзвездных фотографий 
##сделанных из журналов.
##

        scene bg0014 with dissA

        e "Безмолвный крик, обращённый в бездну миров…"

##Сцена 0013
##region
## Быстроя смена кадра через эффект  tlcenteriss
## За тем сцена на верхней площадки маяка. Маленкая Ведма распоожена в правой стороне экрана, 
## сначала она смотрит в камеру потом менает наклон головы. Голова наклонена и смотрит в лево.
##

        scene bg0018 with tlcenteriss
        #play music "Zvuki/Missile 45.wav" fadein 1.5
        #play sound "Zvuki/se-gale.wav" fadein 0.5

        scene bg0005 
        show sn onlayer sloi03
        show LW_Color_Nak_a_02 at LW_medium_range, screen_right_02_medium onlayer sloi02 
        with tlcenteriss

        pause 4.0

        hide LW_Color_Nak_a_02 onlayer sloi02
        show LW_Color_Nak_a_06 at LW_medium_range, screen_right_02_medium onlayer sloi02
        with diss
        #$ renpy.pause(4.0)
    
        e "......"

        hide sn onlayer sloi03
        hide LW_Color_Nak_a_06 onlayer sloi02
        show LW_Color_Nak_a_06 at LW_medium_range, screen_right_02_medium
        #stop music fadeout 1.0

##Сцена 0014
##region
## Затенения смена кадра через эффект diss 
## Общий план сцены со скалистыми островами в бущующим океане. 
## Над ними виден газовый гигант. 
##

        scene bg0000
        with diss
        e "..."
        scene bg0019 with diss
        #play music "Zvuki/OCEAN.WAV" fadein 1.5
        pause 3.0

    
        e " Мир есть океан. "
        e "Океан бушующий, сильный, свирепый, поражающий своей красотой, своей безудержной силой. "
    
        #stop music fadeout 1.5
        e "....."
    
        #play sound "Zvuki/veter_02.mp3" fadein 0.5
        #play music "Sound/BGM_020.mp3" fadein 2.0

##Сцена 0015
##region
## Смена кадра.
##
##

        scene bg0020 with dissA
        #scene bg0000 with diss
        #show LW_Spin_c_01 at left

        e "Но зимой он становится тихим, спокойным и умиротворённым. "
        e "И кажется, что вся планета засыпает, погружаясь в ледяной сон разума. "
    
        e "......"

##Сцена 0016
##region
## Смена кадра.
## Маленькая Ведьма находиться на верхней площадке. В правой часте кадра. 
## За тем через 3 секунды с помощью эффекта slow_move перемещаеться в центр экрана.
##

        scene bg0005 
        show sn onlayer sloi03

        show LW_Color_Nak_a_02 as LW at LW_medium_range, screen_right_02_medium
        with leftiss

        pause 3.0

        #show LW_Color_Nak_a_02 as LW at LW_medium_range, screen_right_02_medium 
        #with slow_move

        #hide LW_Color_Nak_a_02
        show LW_Color_Nak_a_06 as LW at LW_medium_range, screen_center_02_medium with slow_move
        with dissolve
        #play music "Zvuki/OCEAN.WAV" fadein 1.5
        #play natu "Zvuki/turbine_loop_1.wav" fadein 1.0
        #$ renpy.music.set_volume (0.5, .5, channel = "natu")

        e "Маленькой ведьме всегда казалось, что и жизнь - и есть океан:"
   
        #play sound "Zvuki/veter_02.mp3"
        hide LW
        #hide LW_Color_Nak_a_06
        show LW_Color_Nak_a_07 at LW_medium_range, screen_center_02_medium
        with dissolve
        show GI at emo_LW_medium, loposC_LM_medium onlayer sloi03
    
        e " такой же бушующий,  "
    
        hide LW_Color_Nak_a_07
        show LW_Color_Nak_a_08 at LW_medium_range, screen_center_02_medium
        with dissolve

        e " такой же переменчивый и непредсказуемый. "

        hide GI onlayer sloi03
        #show TC at loposC onlayer demo
        hide LW_Color_Nak_a_08
        show LW_Color_Nak_a_05 at LW_medium_range, screen_center_02_medium
        with dissolve

        e "Кинув очередной взгляд в мрачный туманный горизонт, она застыла. "
        e "Казалось, будто она кого-то ждала {w=1}- надеялась, что вот-вот на горизонте появится корабль. "

        hide LW_Color_Nak_a_05
        show LW_Color_Nak_a_07 at LW_medium_range, screen_center_02_medium
        with dissolve
    
        e "Иногда на неё накатывала волна необъяснимой тоски, надежды и предчувствий... "
    
        #play sound "Zvuki/OCEAN.WAV" fadein 0.5
        hide LW_Color_Nak_a_07
        show LW_Color_Nor_a_01 at LW_medium_range, screen_center_02_medium
        with dissolve

        e "Вдохнув морозный соленый воздух, "
        e "Маленькая Ведьма закутавшись потеплее в плотную накидку и поправила свой широкий, расшитый белыми звёздами шарф."
    
        #play sound "Zvuki/veter_02.mp3" fadein 0.5
        hide LW_Color_Nor_a_01
        show LW_Norma_Color_01 at LW_medium_range, screen_center_02_medium 
        with dissolve
        #hide TC onlayer demo

        e "Она резко развернулась на каблуках своих шнурованных сапог."

        hide sn onlayer sloi03
        hide LW_Norma_Color_01 with easeoutleft
        $ renpy.pause(2.0)

##Сцена 0017
##region
## Смена кадра.


        scene bg0022 
        show LW_Color_NormaBust_a_02 at right
        with diss
    

        e "Ветер свистел в ушах, едва не сдувая её широкополую шляпу, которую она придерживала рукой. "
        e "Ветер так и норовил растрепать её тяжёлую, закрепленную заколкой в виде бабочки косу,"
        e " в которую были заплетены её длинные, белые словно снег волосы…"
    
        hide LW_Color_NormaBust_a_02
        show LW_Color_NormaBust_a_01 at right 
        with dissA
    
        e "... "

        hide LW_Color_NormaBust_a_01 with moveoutleft
        
##Сцена 0018
##region
## Смена кадра. 
## На картинке изображена мрачная сцена под сильным дождём в стилистике грубого цифрового скетча 
## или комиксной иллюстрации. Фон почти чёрный, с зелёно-синими оттенками, по всему кадру идут косые линии дождя, создавая атмосферу холода, тревоги и изоляции.
## Справа находится массивное серое здание или укреплённый вход в секретный объект. Оно выглядит как бетонный или металлический бункер с большими прямоугольными панелями.
## На центральной части стены размещена белая табличка с надписью “SCP” и символом, напоминающим логотип SCP Foundation. 
## Архитектура строгая, индустриальная, тяжёлая, с тёмными тенями и синим контурным освещением по краям.
## Рядом заметен маленький красно-оранжевый светящийся элемент, похожий на глаз, индикатор или фонарь.
## Слева находится отдельная деревянная или металлическая платформа. 
## На ней расположен яркий фантастический механизм — что-то вроде самодельного устройства, генератора или странной машины. 
## Конструкция наполнена трубами, кабелями, цилиндрами, яркими синими, жёлтыми и оранжевыми деталями. 
## Верх устройства охвачен огнём или светящейся плазмой: яркое оранжево-жёлтое пламя резко контрастирует с холодной дождливой сценой. Машина выглядит нестабильной, экспериментальной, возможно, аномальной.
##
##
##
        
        scene bg0023 with light4iss
        $ renpy.pause(1.0)
        #play sound "Zvuki/close2.wav"
        #stop natu fadeout 1.6
        #stop music fadeout 1.0
        scene bg0000 
        with circleirisin
        $ renpy.pause(1.0)
        #scene bg0031 at Pan((0, 0), (0, 1550), 10.0) with dissA
        scene bg0031 with dissA

        pause 5.0

        #play music "Sound/BGM_005.mp3" fadein 1.5
        #play sound "Zvuki/metal_mechanical_noise.mp3" fadein 3.0
        #play nature "Zvuki/PDron.mp3" fadein 4.0
        scene bg0025
        show LW_Norma_Color_01 as LW at LW_long_range, screen_right_03_long_may 
        with downiss 

        pause 3.0

        #scene bg0026
         
        #with downiss 
        #with circlewipe
        #play natu "Zvuki/kabluki_po_metal.MP3" fadein 0.5
    

        e "И вот она уже спускалась по внутренней винтовой лестнице, встроенной в шершавую стену словно резьба в винте."
    
        #hide LW_NormFull_01
        #scene bg0000
        #with circleirisin
        #scene bg0027 with dissA
        #with circleirisin
        #$ renpy.pause(3.0)
        #scene bg0000
        #with circleirisin
        #scene bg0028 with dissA
        pause 1.0
        show LW_Norma_Color_01 as LW at LW_long_range, screen_right_03_long_may, moveout_left_bottom
        pause 5.0
        hide LW

        scene bg0000
        with circleirisin
        scene bg0030 with dissA
        
        pause 3.0
        scene bg0000
        with circleirisin
        scene bg0029 with dissA

        e "Ступеньки обходили причудливые старые механизмы, назначение которых Ведьма не знала. "
    
        #scene bg0030 with dissA
    
        e "Размеренный стук шагов причудливым сюрреалистическим эхом разливался по внутренним помещениям маяка. "
    
        scene bg0024 at Pan((0, 0), (0, 2320), 20.0) with dissA

        centered "{i}Топ, топ...{/i} "
  
        centered "{i}Топ, топ...{/i} "
 
        centered "{i}Ниже и ниже…{/i}"
   
        #show LW s01 at right with dissolve

    
        e "Наконец, Маленькая Ведьма спустилась на нижний этаж величественного и причудливого строения. {space=30}{image=images/SD/GO.png}{alt}GO{/alt}"
    
        #stop natu fadeout 0.5
        #stop nature fadeout 1.5
        #play sound "Zvuki/skrip_dveri.mp3"
        #stop music fadeout 1.0
        #hide LW s01 with moveoutright
        scene bg0000 with fade
        scene bg0027 with dissA
        with circleirisin
        
        pause 3.0
        scene bg0000
        with circleirisin
        scene bg0028 with dissA

        pause 3.0
        with circleirisin
        scene bg0032 with dissA
        
        pause 3.0
        with circleirisin
        scene bg0033 with dissA
    
        e "Повернув ручку тяжёлой и скрипучей двери, она вышла на каменный утёс"
    
        #play sound "Zvuki/close2.wav"
        scene bg0000 with dissA

        e "..."

## Сцена 0019
## дальный плань, камера движеться сверху вниз, показывая ядерный маяк.
##Ведьма выходит наружу.
##

        #play nature "Zvuki/Shagi_po_kamnyam_3.MP3" fadein 0.5
        #play natu "Zvuki/turbine_loop_1.wav" fadein 1.0
        #$ renpy.music.set_volume (0.7, .5, channel = "natu")
        scene bg0034 at Pan((0, 0), (0, 2000), 10.0) with dissolve
        $ renpy.pause(10.0)


        e "..."

     
## Сцена 0020    
#фон растительности на скалах
#через две строчки сменит на фон хижины МВ.

        
        scene bg0000 with dissA
        
        e "......"

        scene bg0036 with tlcenteriss 

        e "Растительность здесь была скудная, ибо ветер и волны практически не оставляли на камнях плодородной почвы, "
        e "но каким-то немыслимым чудом – жизнь просачивалась через щели и здесь. "
        
        scene bg0036a
        show fog_01 onlayer sloi04
        with diss
        
        e "Вдали сквозь туман виднелась старая хижина с ветхой протекающей крышей, "
        e "промерзающая в лютые зимы и подпёртая брёвнами с покосившейся стороны. "

 
        scene bg0037
        show LW_Color_Nak_a_02 at LW_long_range, screen_center_03_long 
        show NA at loposCFull onlayer sloi03
        with downiss

## Сцена 0021
## МВ идет от основания мояка. План дальный. 
## Перед ней — чёрный скалистый берег, туман, ветер и старая хижина в отдалении.
## Хижина покосилась. Один бок подпёрт брёвнами. Ветхая крыша едва защищает дом от непогоды.
## Камни торчат вокруг, словно зубы древнего чудовища.
## Ведьма идёт к дому, петляя между камней.
##

        e "Единственное убежище посреди этого неприветливого мирка, обречённого уже скоро стать бесконечной ледяной пустыней…" 
        
        hide LW_Color_Nak_a_02
        show LW_Color_NorEyesOff_a_02 at LW_long_range, screen_center_03_long 
        with dissolve
        
        e "Петляя среди огромных валунов, похожих на зубы древнего чудовища, Маленькая Ведьма направилась к своему скромному жилищу. "
        
        hide LW_Color_NorEyesOff_a_02
        show LW_Color_Nak_a_01 at LW_long_range, screen_center_03_long 
        with dissolve 
        
        e "Шагами, мерившими тысячелетия, она шла вперёд…"


        hide LW_Color_Nak_a_02
        hide NA onlayer sloi03
        #stop sound fadeout 1.0
        #stop nature fadeout 0.5
        #stop natu fadeout 1.9
        scene bg0000
        hide fog_01 onlayer sloi04
        with tcenteriss
        e "...."

## Сцена 0022
#сменит фон анимация, возможно отдельная уменщающейся спрайт МВ, 
#повернутый спиной к игроку, который идет в перспективу фона
   
        #play music "Sound/BGM_002.mp3" fadein 2.0
        scene bg0038 
        show fog_01 onlayer sloi04
        with diss

        e "Этот дом был каменным."
        e "Сейчас вокруг него стыл сумрак ночи. "
        e "Странным казалось в нём всё. И в то же время - всё было обычным, почти родным. "
        
        show LW_Spin_a_01 at xijena, movein_left_bottom_01
        
        e "Словно кто-то взял и ковырнул её воспоминания из детские мечтаний - после чего воплотил их в камне."
        e " Но не стал обтёсывать, а обложил каким-то таинственным заклятием "
        e "и перенёс назад во времени - так, чтобы когда маленькая ведьма его нашла, этот дом выглядел старым."
        e "Но становилось понятным – создан он для неё и поставлен здесь для неё, и дожидается именно её..."

## Сцена 0023
## Внутри темно и холодно.
## Старая мебель: шкаф, стол, пара стульев, комод, кровать. Много пыли.
## В очаге едва тлеют угли.

        scene bg0000
        hide fog_01 onlayer sloi04
        with diss
    
        #play natu "Zvuki/drova.MP3" fadein 0.5
        #$ renpy.music.set_volume (0.9, .5, channel = "natu")
        e "..."
        scene bg0041 
        #show Alaya_01 onlayer sloi02 
        with tlcenteriss

        e "Сняв с себя тяжелый промокший плащ, она вошла в комнату."
        e "В этом доме была старая невзрачная мебель: шкаф, стол, пара стульев, комод и кровать."
        e "И много, много пыли... "

        show LW_Color_Nor_c_08 at xijena, screen_left_02 with moveinleft
        #show S02 at loposLX onlayer demo

    
        e "Она не знала, кто и когда построил этот маяк."
        e "Она не знала, кто и когда построил хижину."
    
        hide LW_Color_Nor_c_08
        show LW_Color_Nor_c_06 at xijena, screen_left_02 
        with dissolve
        #hide S02 onlayer demo
        #show S03 at loposLX onlayer demo

    
        e "Она не знала, кто до неё жил. "
        e "Она лишь нашла то, что было, спустившись с неба три зимы назад."
    
        hide LW_Color_Nor_c_06
        show LW_Color_Nor_c_21 at xijena, screen_left_02 
        with dissolve
        #hide S03 onlayer demo
        #show GI at loposLX onlayer demo
        #LW_NorBust_c_05

    
        e "И поселилась здесь, храня тепло очага. "
    
        hide LW_Color_Nor_c_21
        show LW_Color_Nor_c_05 at xijena, screen_left_02 
        with dissolve

        e "Она обжила этот дом, и он стал ей родным. "
        e "Она уже не представляла жизни вне этого холодного мира..."
    
        #hide GI onlayer demo

## Сцена 0024
## Ведьма озябшими пальцами подкладывает пару поленьев в угли.
## Она наклоняется и дует.
## Едва заметные язычки пламени начинают лизать древесину.
## Она ставит чайник на металлическую решётку.
## В хижине почти так же холодно, как снаружи.
## Ведьма поёживается и садится ближе к огню.

        #hide LW_Color_Nor_c_05
        scene bg0000
        with diss
        e "...."
        #stop natu fadeout 1.5
        #play sound "Zvuki/pechka.mp3" fadein 0.5
        scene bg0044 with downiss
    
        e "Озябшими пальцами Маленькая Ведьма подложила пару поленьев в догорающие угли..."
        e "Когда она подула на них, едва заметные язычки пламени принялись лизать древесину. "
    
        #play natu "Zvuki/drova.MP3" fadein 0.5
        #$ renpy.music.set_volume (1.9, .5, channel = "natu")
        #play sound "Zvuki/zheleznaya_reshetka.mp3"
        scene bg0044 
        show Cainic at pos_Cainic onlayer sloi01
        show LW_Spin_c_02 at screen_left_02_medium, screen_left_03 onlayer sloi03
        show Alaya_02 onlayer sloi04
        with diss

        e "Она поставила чайник на специальную металлическую решётку кипятиться. "

        #scene bg022 with diss
        #$ renpy.music.set_volume (0.9, .5, channel = "natu")
        hide LW_Spin_c_02 onlayer sloi03
        with diss

        e "В хижине было не теплее, чем на улице."

## Сцена 0025

        scene bg0046
        hide Cainic onlayer sloi01
        hide Alaya_02 onlayer sloi04
        show LW_Color_Norm_c_01 at xijena, screen_left_02 
        with diss
        #play nature "Zvuki/Zvuki.mp3" fadein 1.0
        #$ renpy.music.set_volume (1.5, .5, channel = "nature")
        #play sound "Zvuki/teaKettle.mp3"

        e "Поёжившись, она села вплотную к огню – дожидаясь, пока вода в чайнике не вскипит."
    
        hide LW_Color_Norm_c_01
        show LW_Color_Nor_c_09 at xijena, screen_left_02 
        show S02 at loposLX onlayer sloi05
        with dissolve
    
        #voice "Voise/LW/p_29147832_653.mp3"

        LW "{i}«- Тепловое равновесие!»{/i} "

        hide LW_Color_Nor_c_09
        show LW_Color_Nor_c_22 at xijena, screen_left_02
        hide S02 onlayer sloi05
        with dissolve
    
        e "Подметила она про себя,"
    
        hide LW_Color_Nor_c_22
        show LW_Color_Nor_c_11 at xijena, screen_left_02 
        show S01 at loposLX onlayer sloi03
        with dissolve
    
        #voice "Voise/LW/p_29148021_378.mp3"


        LW "{i}« – Что на улице - то и дома... Прям первое начало термодинамики - ни дать, ни взять.»{/i}"
    
        hide S01 onlayer sloi03
        show STAR_S at FactorZoom(0.0, 0.2, 0.0, opaque = False), loposLX_01 onlayer sloi03
        hide LW_Color_Nor_c_11
        show LW_Color_Nor_c_21 at xijena, screen_left_02 
        with dissolve
    
        #hide S01 onlayer demo
        #hide LW v01

        e "Ветер стучался в закрытие ставни, "
    
        hide STAR_S onlayer sloi03
        hide LW_Color_Nor_c_21
        show LW_Color_Nor_c_20 at xijena, screen_left_02 
        with dissolve
    
        e "а единственным источником света в комнате, кроме алых бликов от огня в печке, была маленькая масленая лампадка."
        e "Тёмно-алая полутьма густых теней выхватывала только общие контуры предметов. "

##Сцена 0026
## Ветер стучит в закрытые ставни.
## Единственные источники света — алые отблески печи и маленькая масляная лампадка.
## Тёмно-алая полутьма выхватывает из мрака только контуры предметов.
## Ведьма заваривает травяной чай. Насыпает в кружку душистые приторные травы, собранные летом.
## Она наливает кипяток. Берёт глиняную кружку обеими руками.
## Тепло приятно согревает пальцы.
## Она делает глоток.
## Её взгляд меняется.

        #play sound "Zvuki/Tea.mp3" fadein 0.5
        
        scene bg0047 
        show Alaya_02 onlayer sloi04
        hide LW_Color_Nor_c_20
        with diss
    
        e "Тем временем, Ведьма заварила травяной чай из душистых, приторных трав,"
        e "которые она нашла и собрала за лето..."
    
##Сцена 0027
## Пар от кружки поднимается вверх и превращается в пурпурный туман.
## Перед глазами ведьмы возникают цветущие сады Азатота.
## Медовые деревья с пурпурными листьями. Чудесные сладостные плоды.

        scene bg0048 
        hide Alaya_02 onlayer sloi04
        show Alaya_03 onlayer sloi04
        with dissolve
    
        e "Руки приятно сжимали тепло нагретой глиняной кружки. Она вспомнила душистое вино, которое пила на своей далёкой родине. "
    
        scene bg0049 with dissolve
    
        e "На щеках Маленькой ведьмы снова заиграл румянец от нахлынувших воспоминаний, когда она постаралась вспомнить вкус этого вина... "
        e "Ностальгия... "
        e "Возможно, тоска по её давно покинутому дому."
        e "На девочку вновь нахлынули воспоминания."
    

        #stop music fadeout 1.0
        #stop nature fadeout 1.0
        #stop natu fadeout 1.0
       
        scene bg0000 
        hide Alaya_03 onlayer sloi04
        with dissA

##Сцена 0028
## Пурпурный мир.
## На опушке магического леса стоит уютный особняк в западном английском стиле. У него есть башенка для наблюдения звёзд.
## На синих ставнях изображены солнца, луна и звёзды.
## Вокруг — пурпурные растения. В корнях стелется синеватый студень с красивыми язычками света, похожими на пламя.
## Маленькая ведьма сидит на крытом крылечке, укрывшись клетчатым пледом.
## Она пьёт сладкое вино из глиняной кружки и смотрит на небо.

        e "..."
    
        #play music "Zvuki/atmosfera_pustoty.mp3" fadein 1.5
        scene bg0050
        show Alaya_04 onlayer sloi02
        show Alaya_05 onlayer sloi03
        show fly #onlayer sloi04
        with pixellate
    
        e "Воспоминания о цветущих садах Азатота, где росли медовые деревья с пурпурными листьями и чудесными сладостными плодами... "
        
        scene bg0051
        hide Alaya_04 onlayer sloi02
        hide Alaya_05 onlayer sloi03 
        hide fly #onlayer sloi04
        show LW_NFM_01 at pos_cen onlayer sloi03
        show Mil_01 at pos_cen onlayer sloi04
        with diss
        $ renpy.pause(2.0)
        scene bg0052 with dissA
    

    
        e "Девочка была одна, она была всегда одна с того момента, когда она нашла этот мир, "
    
        scene bg0053 with dissA

    
        e "спустившись с неба в мыльном пузыре Алькубьерре наделенного разумом корабля-оболочки, "
    
        scene bg0016 with dissA
        $ renpy.pause(2.0)
        scene bg0060 with dissA

        e "и осталась на этих скалах. "
 
        scene bg0054 with diss
        $ renpy.pause(2.0)
        scene bg0055 with dissA

    
        e "Она была одна, когда путешествовала по чёрным безднам между россыпью звёзд"
   
        scene bg0056 with diss
        $ renpy.pause(2.0)
        scene bg0057 with dissA

    
        e "и галактик, видела туманности раскалённого светящегося газа, "
    
        scene bg0058 with dissA

    
        e "рисующего причудливые узоры причудливыми цветами, преодолевала пылевые холодные облака."
   
        scene bg0059 with diss

        e "Она была одна и когда покидала чёрные звёзды."
   
        #stop music fadeout 1.0
        scene bg0000 
        hide LW_NFM_01 onlayer sloi03
        hide Mil_01 onlayer sloi04
        with dissA
        e "......"
        #play music "Sound/3554.mp3" fadein 2.5
        scene bg0050 
        show fly onlayer sloi02
        with teleport

        e "Когда-то Маленькая ведьма жила в причудливом пурпурном мире."
   
        scene bg0061 with dissA

        e " Её домом был небольшой, но уютный особнячок английского стиля с башенкой для наблюдения звезд."
        e "Он располагался на опушке магического леса с пурпурными растениями,"
        e "в корнях которых переливался холодным пламенем синеватый студень."
  
        scene bg0062 with dissA


        e "По вечерам она любила, укрывшись в клетчатый плед, разглядывать россыпи звезд на черном куполе небосвода. "
        e "Она любовалась причудливыми созвездиями, объятыми в царственные облака межзвёздного газа, "
        e "сидя на крытом крылечке своего дома и неспешно потягивая сладкое вино из глиняной кружки. " 
  

        hide fly onlayer sloi02
        scene bg0000 with dream

        e "..."

##Сцена 0029
## В небе висит огромный мыльный пузырь.
## Внутри него — ИГГДРАСИЛЬ, великое Древо Жизни.
## Его корни уходят в космос. Ствол необъятен, покрыт мхом и грибными наростами, источающими призрачный свет.
## На ветвях блестят хрустальные грозди миров.


        scene bg0063 at Pan((0, 1347), (1019, 0), 40.0)  with pixellate
        show bg0064 at Pan((0, 1000), (0, 0), 40.0) with dissA
        $ renpy.pause(10.0)

        e "Также она любила смотреть на Иггдрасиль - колоссальное Древо Жизни, соединяющего миры.{space=30}{image=images/SD/SG.png}{alt}SG{/alt}"
        e "Великое Древо, которому поклонялись как даровавшему жизнь и мудрость – оно висело в огромном мыльном пузыре на орбите планеты, {space=30}{image=images/SD/SG.png}{alt}SG{/alt}"
    
        e "а корни его уходили в космос. {space=30}{image=images/SD/SG.png}{alt}SG{/alt}"
        e "Изумрудная листва блистала каплями росы, отражая свет, источая гротескные видения снов непостоянных форм, {space=30}{image=images/SD/GO.png}{alt}GO{/alt}"
    
    

        hide bg0064
        scene bg0065 at Pan((0, 0), (0, 1100), 15.0) with diss
        $ renpy.pause(1.0)
        scene bg0066 at Zoom((1920, 1080), (225, 150, 400, 300), (0, 0, 1920, 1080), 15.0) with dissA
        $ renpy.pause(1.5)
        scene bg0067 at Pan((0, 0), (0, 900), 20.0) with dissA
    

        e "а гигантский необхватный ствол, покрытый мхом и сочащимися призрачным светом грибными наростами чаг, {space=30}{image=images/SD/SG.png}{alt}SG{/alt}"
        e " разрастался раскидистыми ветвями, {space=30}{image=images/SD/SG.png}{alt}SG{/alt}"
        e "на которых блестели хрустальные грозди миров, плывущие в грезах мироздания... {space=30}{image=images/SD/GO.png}{alt}GO{/alt}"
    
##Сцена 0030
## Рядом с Иггдрасилем висит неподвижная чёрная луна.
## На её поверхности — страшные высокие башни из чёрного металла. Их геометрия невозможна, противоречит разуму.
## В коре луны зияют расщелины, уходящие в глубины.
## Вдали мелькают вспышки и сияния, похожие на маленькие звёзды.

        scene bg0068 with diss

        e "Рядом с Древом Жизни неподвижно висела тёмная луна, покрытая страшными башнями из иссиня-чёрного металла,"
        e" между которыми время от времени мелькали вспышки. "

        scene bg0066a 
        show starA at zoom_starA_01, Position(xpos = 600, ypos = 490, xanchor = 0.5, yanchor = 0.5) onlayer sloi03
        with diss

        e "Эти башни, попиравшие сами основы законов геометрии, принадлежали покинутому пустому граду, "
        e "когда-то населённому не поддающимися разуму Великими Драконами {w=1}- вечными странниками междумирья, появившимися в начале всех начал."


        scene bg0066
        hide starA onlayer sloi03
        show starA at zoom_starA, Position(xpos = 420, ypos = 250, xanchor = 0.5, yanchor = 0.5) onlayer sloi03
        with diss

        e "И бездны расщелин, уходящими в таинственные глубины под кору вечного чёрного спутника, "
    
        show DRC at Position(xpos = 1100, ypos = 530, xanchor = 0.5, yanchor = 0.5) onlayer sloi04 with teleport


        e "не были властны понятия пространства и времени, но магия и время брались оттуда…"
   
        scene bg0069 
        hide starA onlayer sloi03
        hide DRC onlayer sloi04
        with dissA

        e "Так же говорят, что когда-то, давним давно, там жила настоящая Ведьма, "
    
        scene bg0071 with dissA

        e " что присматривала за мирами, но покинула свой дом, отправившись в великий град звёзд."
    
        scene bg0070 with dissA

        e "отправившись в великий град звёзд."

    
        e "Туда, где находился «Звёздный Храм»…"
    
        #stop music fadeout 1.0
        scene bg0000 with circleirisin

##Сцена 0031
## Темнота.

        e "......"

        #scene bg0000b with dissA

        #play music "Sound/BGM_011.mp3" fadein 2.0

    
        centered "{color=#7fbdbf}{i}Какой же была ты, Маленькая ведьма, в глазах твоего отца? Как ему описать тебя? Любящей, прежде всего; любящей и нежной - любящей, как кошка, или же нежной, словно лань...{/i}{/color}"

##Сцена 0032
## Ведьма делает ещё глоток горьковатого напитка.
## Она ставит кружку на стол.
## Огонь в очаге тлеет. Лампадка мерцает.
## Ведьма укладывается спать.
## Тонкие сны, похожие на прозрачные нити, медленно окутывают её.

        scene bg0074
        show Alaya_04 onlayer sloi02
        with dissA

        e "Сделав ещё глоток горьковатого напитка, Маленькая Ведьма приготовилась почивать."

##Сцена 0033
## Маленькая ведьма парит среди множества миров.
## Миры проплывают перед ней, как узоры в калейдоскопе: города, леса, океаны, чужие существа, лица, чьи-то жизни.

        scene bg0075 with fade
    
        e "Маленькой ведьме часто снились непонятные сны."
    
        pause 1.0
        scene bg0096a with dissA # bg0077 with dissA
        hide Alaya_04 onlayer sloi02  with dissA
        #$ renpy.
        #scene bg0096a #bg0079 
        #show LW_sl_01
        with dissA

        e "Жуткие или странные, загадочные и манящие, мистические и фантастические."

        scene bg0096 with dissA
        $ renpy.pause(1.0)
        scene bg0097 with dissA
        $ renpy.pause(1.0)
        scene  bg0098 with dissA
        $ renpy.pause(1.0)
        scene bg0081 
        #hide LW_sl_01
        with dissA
    
        e "В них Маленькая Ведьма оказывалась в разных, не похожих друг на друга местах, наблюдая и общаясь с обитателями этих странных миров. "
        scene bg0082 with dissA

        e "Цепи тонких снов окутывали Маленькую Ведьму,"
        e "которая боялась этих снов, и в тоже время - сны манили её, заволакивая в свои чарующие объятия..."
    
##Сцена 0033
## Ведьма встречает разных существ. Кто-то протягивает ей руку. Кто-то улыбается. Кто-то зовёт её за собой.
## Но каждый мир начинает распадаться, едва она отводит взгляд.

        scene bg0000 with teleport
        $ renpy.pause(1.0)
        scene bg0078 with dissA

        centered "{color=#d16f6a}{i}Мир податлив и мягок – он таков, каким мы его видим. {/i}{/color}"
        centered "{color=#d16f6a}{i}Измените своё восприятие мира, и он послушно изменится - это и есть основной закон магии.{/i}{/color} "
        centered "{color=#d16f6a}{i}Он недоказуем, но однажды испытавший на себе его действие - более не поставит его реальность под сомнение.{/i}{/color} "
    

        scene bg0084 with dissA
        $ renpy.pause(1.0)
        scene bg0085 with dissA
    

        e "Так думала Маленькая ведьма, путешествующая по серебряным и алым снам, существуя в них, словно птица в небе. "
        e "Она была в них свободна и независима, но эта свобода была словно раскаленная игла. "
        e "Она чувствовала, что постоянно теряет частичку себя в чужих снах. "
    
        scene bg0084 with dissA
        $ renpy.pause(1.0)
        scene bg0078 with dissA
        $ renpy.pause(1.5)
        scene bg0086 with dissA

        e "Она погрузилась в бездну воспоминаний и сновидений, которым трудно, а может и невозможно подобрать разумное определение."
   
        scene bg0084 with dissA
        $ renpy.pause(1.0)
        scene  bg0078 with dissA
        $ renpy.pause(1.5)
        scene bg0095 with dissA

        e "Плутая в иллюзорных лабиринтах смутных видений, созерцая проплывающие перед её взором,"
    
        scene bg0090 with dissA
        $ renpy.pause(1.0)
        scene bg0099 with dissA
        $ renpy.pause(1.0)
        scene bg0087 with dissA


        e "словно в калейдоскопе, миры, и чьи-то жизни. "
    
        scene bg0083 with dissA
        $ renpy.pause(1.0)
        scene bg0082 with dissA
        $ renpy.pause(1.0)
        scene bg0089 with dissA

        e "В своих тонких снах, чистых как горный лёд, Маленькая Ведьма часто созерцаяла причудливые картины пейзажей. "
   
        scene bg0090 with dissA
        $ renpy.pause(1.0)
        scene bg0091 with dissA
        $ renpy.pause(1.0)
        scene bg0092 with dissA

        e "Путешествуя по другим мирам, она знакомясь с разными живыми, разумными существами... "
        e "Но даже так, она оставалась одинокой. "
    
        scene bg0094 with dissA
    

        e "Она не могла назвать их друзьями, даже если они предлагали ей дружбу. "
        e "Ведьма знала, что стоит ей проснуться - всё распадется. "
        e "Сны не вечны." 
  
        scene bg0093 with dissA

        e "Они податливы, словно узор, рисуемый морозом на стекле, распадающийся лишь от лёгкого тёплого дуновения пробуждения."
    
        scene bg0075 with fade

        e "Что видит Маленькая ведьма, созерцая этот мир, что снится ей?"
    
        #stop music fadeout 1.0
        scene bg0000 with fade
    
        e "..........."
        e "....."
    
        #$ Cha_01 = renpy.random.choice([1, 2])
        #$ Cha_01 = mci
        #return
        jump Cha_001
        return

label Cha_001:

##Сцена 0034
## Яркие звёзды закручиваются в водоворот.
## Ведьма падает сквозь них, но падение похоже на полёт.

        $ mci = rgen.rgen() 
        $ Cha_01 = mci

        if Cha_01 == 1:

        
                scene bg0104 with fade
    
                centered "{i}В бесконечном числе миров, где каждая звезда есть отдельный мир, есть нечто уникальное и неповторимое...{/i} "
                centered "{i}но все эти миры находятся под влиянием единых законов природы лежащих в глубине основы мироздания. {/i}"
                centered "{i}И все это вместе называется вселенной. {/i}"
                centered "{i}Но нет, ни одного из миров, который можно было бы назвать «моим», {/i}"
    
                scene bg0101 with dissA
    
                centered "{i}потому что у каждого есть свое место в космосе и свои звезды; {w=1}я сама не существую {/i}"
                centered "{i}– но где-то там во всем этом находится мое сердце... {/i}"
    
                scene bg0109 with dissA
    
                centered "{i}Это непостижимо для человеческого ума...  {/i} "
                centered "{i}Здесь все происходит одновременно {w=1}– но по-разному для каждого.{/i} "
                centered "{i}В этой вселенной нет вечности; и никого, и никогда нельзя остановить во времени…{/i}"
    
                scene bg0103 with dissA
    
                e " Она видела Владык Света, которые держат миры невидимыми узами. "
    
                scene bg0106 with dissA
    
                e " Переходя от звезды к звезде и бросая непрестанное сияние жизни"
                e " из вечно меняющихся центров до самых последних пределов пространства."
    
                scene bg0100 with dissA
    
                e " Все это она видела в ясных образах, все космологические эпохи,"
                e " до предела времен,"
                e " которого ни один человек не может охватить разумом. "
    
                scene bg0105 with dissA
    
                e "Проникала она в глубину и высоту и прозревала за пределами всех сфер,"
                e " всех форм, всех светил, всякого источника движений."
    
                scene bg0102 with dissA
    
                e " То незыблемое и безмолвно действующее Великое,"
                e " согласно Которому тьма должна развиваться в свет, смерть - в жизнь, "
    
                scene bg0107 at Pan((0, 0), (0, 1550), 35.0) with dissA
    
                e "пустота - в полноту, бесформенность - в форму,{space=30}{image=images/SD/SG.png}{alt}SG{/alt} "
                e "добро - в нечто лучшее, лучшее - в совершеннейшее; {space=30}{image=images/SD/SG.png}{alt}SG{/alt}"
                e "это невысказываемое Великое сильнее самих богов: Оно неизменно, {space=30}{image=images/SD/SG.png}{alt}SG{/alt}"
                e "невыразимо, первоверховно.{space=30}{image=images/SD/SG.png}{alt}SG{/alt}"
                e " Это - Власть созидающая, разрушающая и воссоздающая, {space=30}{image=images/SD/SG.png}{alt}SG{/alt}"
                e "направляющая все и вся к добру, красоте и истине.{space=30}{image=images/SD/GO.png}{alt}GO{/alt}"

                pass
    
        
        elif Cha_01 == 2:

                pass

        else:

                #e "вариант 3"

                jump Cha_001


##Сцена 0035
## Перед ведьмой раскрывается бесчисленная система миров и солнц.
## Мириады светил движутся с поразительной правильностью.
## Каждое светило — отдельный мир, и одновременно часть общего целого.

        scene bg0000b with circleirisin

        e "***************************************"

        scene bg0000 with dissolve
        scene bg0078 with dissA

        call chapt_01_2_splashscr

        #centered "{color=#d16f6a}{i}Когда вечности суть я познала сама,{/i}{/color}"
        #centered "{color=#d16f6a}{i}Я тебя здесь уже найти не смогла,{/i}{/color}"
        #centered "{color=#d16f6a}{i}В тумане снов своих плывёт{/i}{/color}"
        #centered "{color=#d16f6a}{i}Ярких звёзд водоворот.{/i}{/color}"
        #centered "{color=#d16f6a}{i}Сон единый я создам, о цветах в серебряной ночи,{/i}{/color}"
        #centered "{color=#d16f6a}{i}Как тени этого яркого мира засыпают вечным сном.{/i}{/color}"

        scene bg0000 with dissolve

        centered "{color=#23a7e0}{i} Хранительница бездны миров, её наставница знает всё. Её волей мир никогда не сходит с означенного круга. Чёрная королева мира.{/i}{/color}"
    
        #play music "Sound/ghost-town2.mp3" fadein 1.5
        e "..."
    
        scene bg0108 with pixellate

        e "В сфере, не имеющие названий, в бесчисленные системы миров и солнц, двигающихся с поразительной правильностью, "
        e "мириады за мириадами... "
        e "где каждое светило является самостоятельным целым и в то же время частью целого одним из серебристых островов на сапфировом море, "
        e "вздымающемся в бесконечном стремлении к переменам…"


        scene black

        #(Вариант Saitar1337)
## Сцена 0036
## Сумерки. Темно.
## Маленькая ведьма мягкой походкой спускается с небольшого холма, покрытого высокой травой.
## На траве блестят большие капли воды после дождя. На серой земле под стеблями лежат студенистые лужицы.
## Ведьма останавливается, втягивает носом воздух.


        $ slw.body = "default"
        $ wind_01 = 1
        $ slw.eyes = "blink"
        $ slw.brov = "brov_angry_01"
        $ slw.freckles = "norm_01"
        $ slw.cry = "no"
        $ slw.mouth = "default"
        #$ slw.hat = "hat_01"
        $ slw.hat = "no"
        $ slw.panties = "no"
        #$ slw.panties = "panties_white"
        #$ slw.pantaloons = "pantaloons_short"
        $ slw.pantaloons = "pantaloons_long"
        #$ slw.pantaloons = "no"
        #$ slw.top = "top_black"
        $ slw.top = "no"
        $ slw.clothes = "no"
        $ slw.gloves_left = "gloves_left_01"
        $ slw.gloves_right = "gloves_right_01"
        $ slw.boots_left = "boots_left_01"
        $ slw.boots_right = "boots_right_01"
        #$ reset_slw_blink()
        

        #default eyes_LW_01 = True
        #default cry_LW_01 = 'no'
        #default freckles_LW_01 = 'norm_01'
        #default mouth_LW_01 = True
        #default brov_LW_01 = True
        

        show little_witch at LW_long_range, screen_center_03_long onlayer sloi02
        
        e "...."

        $ slw.mouth = "norm_surprised_03"
        $ slw.brov = "brov_angry_05"
        $ slw.eyes = "eyes_norm_horror_02"
        $ slw.freckles = "norm_hatching_01"
        #$ slw.pantaloons = "pantaloons_long"
        #$ slw.top = "top_01"
        $ slw.body = "bodu_01_left"
        e "...."
        $ slw.body = "bodu_01_left_down"
        e "...."
        $ slw.body = "bodu_01_left_slant"
        e "...."
        $ slw.body = "bodu_02_left"
        e "...."
        $ slw.body = "bodu_02_left_slant"
        e "...."
        $ slw.body = "bodu_02_default"
        e "...."
        $ slw.body = "bodu_02_left_down"
        e "...."
        $ slw.body = "bodu_03_default"
        e "...."
        $ slw.body = "bodu_03_left_down"
        e "...."
        $ slw.body = "bodu_03_left_down_slant"
        e "...."
        $ slw.body = "bodu_04_default"
        e "...."
        $ slw.body = "bodu_04_left_down"
        e "...."
        $ slw.body = "bodu_04_full_face"
        e "...."
        $ slw.body = "bodu_04_full_face_slant"
        e "...."
        $ slw.body = "bodu_05_default"
        e "...."
        $ slw.body = "bodu_05_full_face"
        e "...."
        $ slw.body = "bodu_05_full_face_slant"
        e "...."
        $ slw.body = "bodu_05_left"
        e "...."
        $ slw.body = "bodu_05_left_down"
        e "...."
        $ slw.body = "bodu_06_default"
        e "...."
        $ slw.body = "bodu_06_left"
        e "...."
        $ slw.body = "bodu_05_full_face"
        e "...."
        $ slw.body = "bodu_06_left_down"
        e "...."
        $ slw.body = "bodu_06_left_slant"
        e "...."
        $ slw.body = "bodu_07_default"
        e "...."
        $ slw.body = "bodu_08_default"
        e "...."
        $ slw.body = "bodu_08_left"
        e "...."
        $ slw.body = "bodu_08_left_down"
        e "...."
        $ slw.body = "bodu_08_left_slant"
        e "...."
        $ slw.body = "bodu_09_left"
        e "...."
        $ slw.body = "bodu_09_left_down"
        e "...."
        $ slw.body = "bodu_12_base"
        e "...."
        $ slw.body = "bodu_13_base"

       
        #$ head_LW_01 = 'left_slant'


        #$ head_LW_01 = 'default'
        #show HM s01 at right onlayer xra with dissolve
        #hide Little_witch onlayer sloi02
        # LW open ""
        # show LW -open





        e "v"

        hide little_witch onlayer sloi02




    
        e "Уже наступили сумерки, и было темно. "
        e "Недавно прошедшая гроза разлила по воздуху запах озона, а высокая трава колыхалась от дуновений бодрого ветерка, "
        e "поблёскивая крупными каплями свежей влаги." 

        e "Мягкой походкой Маленькая Ведьма спустилась с небольшого холма, "
        e "осторожно ступая между студенистыми лужицами. "

## Сцена 0037
## Ведьма замедляет бег и по инерции проходит ещё несколько шагов.
## Она оказывается у порога хижины.
## Над дверью горит фонарик. Он освещает маленький участок земли.
## Вокруг фонаря кружатся ночные бабочки. Их крылья опалены жаром, но они продолжают порхать возле огня.
## Ведьма смотрит на них лишь мельком.

        #scene bg057 with rightiss


        e "Пройдя вдоль дома на сваях, стоявшего на берегу озера с неестественно серебристо-белой водой, "
        e "она остановилась возле порога хижины. "
  
    
        #play sound "Zvuki/Nasic01.mp3"
        #scene bg058 with fade
        #show bafly_01 at splineBater_01
        #show bafly_02 at splineBater_02
        #show bafly_03 at splineBater_03
        #show bafly_04 at splineBater_04
        #show LW_NorBust_c_08 at smooth_random_move

    
    
    
        e "Над дверью горел фонарь, выхватывавший из темноты пядь земли внизу."
        e "Рядом вились ночные бабочки, порхавшие в нежном танце вокруг яркого света. "
        e "Их крылья уже были опалены жаром, но они продолжали порхать возле огня. "
        e "Огонь манил этих бабочек, действуя как наркотик. "
   
        #play sound "Zvuki/open1.ogg"
        #scene bg000 with light4iss
        #scene bg040a with circleirisout
    

        e "Маленькая ведьма, словно не заметив их, спокойно вошла в хижину своей Наставницы. "

## Сцена 0038
## Внутри хижина невозможным образом превращается в непостижимые тёмные покои вне времени.
## Звучит глухая дробь барабанов.
## К ней примешиваются тихие монотонные всхлипы флейт.
## В темноте пляшут гигантские тени неведомых существ.
## Пространство изгибается. Звёзды и материальные миры остаются позади.
## Ведьма несётся метеором сквозь кромешный хаос.
## Впереди — кипящий огненный центр Всего.
## Там стоит чёрный трон.

        e "Эта хижина казалась небольшой лишь снаружи. "
        e "Причудливо искривлённое пространство, изнутри оно было большим, даже безразмерным. "
        e "Сквозь густую тьму запредельной бездны просвечивали мириады удалённых звёзд и мерцали причудливые облака туманностей. "
        e "И лишь под ногами Маленькой Ведьмы эта пустота обращалась во что-то плотное, хрустевшее будто кафель. "
        e "Сквозь пустоту раздавались странные звуки, пугающие звуки, похожие на жуткую дробь барабанов и тихие монотонные всхлипы проклятых флейт… "

        e "Маленькая Ведьма никак не могла привыкнуть к этому ощущению – будто пело само пространство, "
        e "и в межзвёздной бездне мелькали гигантские тени неведомых и непостижимых существ."
        e " Но её шаги продолжала стучать по несуществующему полу посреди космической бездны… "
        e "Наконец, посреди этой тьмы она увидела даже не комнату – просто очерченный куб удивительно нормального бытового пространства,"

## Сцена 0039
## На престоле сидит ЖЕНЩИНА — НАСТАВНИЦА.
## Она облачена в невероятно просторный ханбок. По её чхиме плывут звёзды и галактики. На голове сверкает диадема.
## Женщина поднимает взгляд. Её глаза глубокие, древние и спокойные.

        #default head_LW_01 = "left_down"
        #default head_LW_01 = 'default'
        #$ wind_01 = 0
        #default eyes_LW_01 = True
        #default cry_LW_01 = 'no'
        #default freckles_LW_01 = 'norm_01'
        #default mouth_LW_01 = True
        #default brov_LW_01 = True

        #show Little_witch at LW_long_range, screen_center_03 onlayer sloi02
        #show LW n at left with moveinleft
        #show TR at Position(xpos = 400, ypos = 0, xanchor = 0, yanchor = 0)
        #show plate at right
        #show HM n at right onlayer xra 
        #with teleport
        #$ head_LW_01 = 'left_slant'
    
        e " посреди которого, в похожем на трон высоком кресле восседала женщина со сверкающей диадемой на голове, "
    
        #$ head_LW_01 = 'default'
        #show HM s01 at right onlayer xra with dissolve
        #hide Little_witch onlayer sloi02
        # LW open ""
        # show LW -open

        e "по причудливому длинному одеянию которой плыли звёзды и галактики."

        #show HM r01 at razgavor, right onlayer xra with dissolve
        #show V at loposR onlayer dexm
        #voice "Voise/HM/p_29148220_413.mp3"
        HM "- А... "
        e "протянула женщина."
        HM " - Это ты, Тихоня?"
        #show HM n at right onlayer xra with dissolve
        #hide V onlayer dexm
    
        e "Маленькая ведьма кивнула, проходя дальше в комнату. "
   
        #show HM s05 at right onlayer xra with dissolve
    
        e "Женщина еле заметно улыбнулась, поднимая на неё взгляд своих бездонных глаз."
    
        #show HM r01 at razgavor, right onlayer xra with dissolve
        #show S02 at loposR onlayer dexm
        #voice "Voise/HM/p_29148243_564.mp3"
        HM " - Давно ты не наведывалась."
        #show HM s02 at right onlayer xra with dissolve
    
        #show LW v03 at razgavor, left with dissolve
        #voice "Voise/LW/p_29148281_749.mp3"
        LW " - Да, пожалуй."
        #show LW v04 at left with dissolve

        e "Чуть виновато ответила Ведьма."

        #show HM r01 at razgavor, right onlayer xra with dissolve
        #hide S02 onlayer dexm
        #show B at loposR onlayer dexm
        #voice "Voise/HM/p_29148296_877.mp3"
        HM " - Что привело тебя в мои скромные чертоги?"
        #show HM s03 at right onlayer xra with dissolve
        #hide B onlayer dexm
 
        e "Полюбопытствовала она."
    
        #show LW ud at left with dissolve
        #show B at loposL onlayer demo 
    
        e "Маленькая ведьма задумалась, перебирая в уме доступные варианты. Потом ответила:"
    
        #hide B onlayer demo
        #show V at loposL onlayer demo
        #show LW v02 at razgavor, left with dissolve
        #voice "Voise/LW/p_29148328_996.mp3"
        $ renpy.pause(1.0)
        #voice "Voise/LW/p_29148347_104.mp3"
        LW "- Наверное… {w=1} Я хочу больше узнать про магию…"
        #show LW n at left with dissolve
        #hide V onlayer demo
    
        #show HM r02 at razgavor, right onlayer xra with dissolve
        #show D at loposR onlayer dexm
        #voice "Voise/HM/p_29148543_111.mp3"
        HM "- И что ты хочешь, чтобы я рассказала тебе? "
        #show HM s03 at right onlayer xra with dissolve
    
## Наставница задумчиво смотрит на маленькую ведьму.
    
        e "Добродушно произнесла Наставница." 
        e "Она пригласила Маленькую Ведьму поближе, жестом руки материализовав из ничего резной деревянный стул. "
        e "Присаживаясь, Ведьма успела разглядеть на её запястье радужные чётки, "
        e " выглядевшие как нанизанная на нить гирлянда миров с белёсыми точками галактических скоплений… "
        e " Наконец, собравшись с духом, Маленькая Ведьма спросила:"
    
        #hide D onlayer dexm
        #show LW r at razgavor, left with dissolve
        #voice "Voise/LW/p_29148571_226.mp3"
        LW "- Как стать настоящей Ведьмой?"
        #show LW n at left with dissolve
        #show HM s01 at right onlayer xra with dissolve
        #show B at loposR onlayer dexm
        #show HM r01 at razgavor, right onlayer xra with dissolve
        #voice "Voise/HM/p_29148594_348.mp3"
        HM "- Как ты знаешь, "
        #hide B onlayer dexm
        #show HM r02 at razgavor, right onlayer xra with dissolve

        e"- задумчиво произнесла Наставница,"

        #show S03 at loposR onlayer dexm
        #voice "Voise/HM/p_29148603_456.mp3"
        HM "- магию Ведьмы очень условно, можно разделить на магию внешнего круга, и магию внутреннего круга. "
        #voice "Voise/HM/p_29148612_543.mp3"
        HM "Можно сказать, что магия внешнего круга – это искусство изменения мира путем прямого воздействия на окружающее,"
        #voice "Voise/HM/p_29148622_649.mp3"
        HM "а магия внутреннего круга – посредством изменений процессов сознания. "
        #voice "Voise/HM/p_29148632_729.mp3"
        HM "Это также множество удивительных событий и явлений, с этими процессами связанных."
        #show HM n at right onlayer xra with dissolve
        #hide S03 onlayer dexm
    
        #show LW s02 at razgavor, left with dissolve
        #show B at loposL onlayer demo
        #voice "Voise/LW/p_29148665_241.mp3"
        LW "- И как мне это поможет? "
        #hide B onlayer demo
        #show LW v04 at left with dissolve

        e "Поинтересовалась Маленькая Ведьма."
    
        #show HM r01 at razgavor, right onlayer xra with dissolve
        #show C at loposR onlayer dexm
        #voice "Voise/HM/p_29148696_691.mp3"
        HM "- Скажи мне, что тебя побуждает к изучению магии?"
        #show HM n at right onlayer xra
        #hide C onlayer dexm
    
        e "Маленькая ведьма снова задумалась."

        #show LW ud at razgavor,  left with dissolve
        #show ZB at loposL onlayer demo
        #voice "Voise/LW/p_29148328_996.mp3"
        LW "- Наверное, "
        #show LW rn at razgavor, left with dissolve

        e "- начала она неуверенно,"

        #voice "Voise/LW/p_29148721_865.mp3"
        LW "- Потому что я хочу понять, реален ли окружающий меня мир? "
        #show HM s03 at right onlayer xra with dissolve
        #hide ZB onlayer demo
        #show LW n at left with dissolve

## Наставница молчит. Затем хмурится.

        #show HM r02 at razgavor, right onlayer xra with dissolve
        #show D at loposR onlayer dexm
        #voice "Voise/HM/p_29153489_142.mp3"
        HM "Любой подобный ответ, "
        #show HM r01 at razgavor, right onlayer xra with dissolve
        #hide D onlayer dexm


        e "Ответила Наставница, немного помолчав, продолжила,"

        #voice "Voise/HM/p_29153566_319.mp3"
        $ renpy.pause(1.0)
        #voice "Voise/HM/p_29153609_412.mp3"
        HM "Является, всего лишь ментальной установкой, на которой базируется искусственная вера"
        #voice "Voise/HM/p_29153667_550.mp3"
        HM "и соответствующая ей внутренняя реальность внутренней игры – игры с самой собой…"
        #show HM s04 at right onlayer xra with dissolve
    
        LW "- С самой собой?"
  
        e " – удивлённо спросила Маленькая Ведьма."

        HM "- Именно… "
    
        e "- ответила Наставница, "
    
        HM "– Грань, которая прорастает сквозь миры, словно корни древа сквозь землю… "
        HM "Она существует в теле каждого живущего существа, в каждой живой клетке как частица чего-то необъятного. "
        HM "Необъяснимого вопроса зарождения самой жизни… "
        HM "Необъяснимого вопроса осознания разумом самого себя… "
        HM "Грань - только начало всей жизни, но и начало начал магии…"



        #show LW s02 at razgavor, left with dissolve
        #show B at loposL onlayer demo
        #voice "Voise/LW/p_29153803_927.mp3"
        LW "- А какой же ответ на самом деле? "
        #show HM s02 at right onlayer xra with dissolve
    
        e "Поинтересовалась маленькая ведьма, с любопытством смотря на Наставницу."
    
        #hide B onlayer demo
        #show LW n at left with dissolve
    
        #show HM r01 at razgavor, right onlayer xra with dissolve
        #voice "Voise/HM/p_29153897_127.mp3"
        HM "- Единственный честный ответ, который может быть дан:"
        #show HM r02 at razgavor, right onlayer xra with dissolve
        #show S02 at loposR onlayer dexm
        #voice "Voise/HM/p_29153944_278.mp3"
        HM "«- Внутри меня есть нечто, что побуждает меня следовать этому пути», "


        e "– Наставница снова умолкла, собираясь с мыслями, и осторожно продолжила,"

        #voice "Voise/HM/p_29154001_420.mp3"
        HM "Прислушайся к себе и ощути в себе это «нечто». "
        #hide S02 onlayer dexm
        #show HM s03 at right onlayer xra with dissolve

        HM "Это и будет Грань."
    
  
        #show HM n at right onlayer xra with dissolve
    
        #show LW rn at razgavor, left with dissolve
        #voice "Voise/LW/p_29154110_718.mp3"
        LW "- Это «Нечто», существующее во мне - и есть то, что находится во внутреннем круге магии?"
        #show LW n at left with dissolve

        e "– Догадалась Маленькая Ведьма…"

## Маленькая ведьма смотрит на наставницу с тревожным любопытством.
        
        #show HM r01 at razgavor, right onlayer xra with dissolve
        #show SHT at loposR onlayer dexm
        #voice "Voise/HM/p_29211904_97.mp3"
        HM "— Почему же ты не можешь тогда стать ведьмой, если у тебя всё лежит на поверхности? "
        #show HM r02 at razgavor, right onlayer xra with dissolve

        e "– Задала риторический вопрос Наставница, "

        #hide SHT onlayer dexm
        #voice "Voise/HM/p_29212783_505.mp3"
        HM "- Ты путешествуешь по снам, ты летаешь по небу, варишь зелья, и прочее… "
        #voice "Voise/HM/p_29212818_603.mp3"
        HM "Но настоящей ведьмой ещё не стала..."
        #show HM n at right onlayer xra with dissolve
    
        #show LW ud at razgavor, left with dissolve
        #show B at loposL onlayer demo
        #voice "Voise/LW/p_29211978_320.mp3"
        LW "— И почему же?"
        #hide B onlayer demo
        #show LW n at left with dissolve
    
        #show HM r01 at razgavor, right onlayer xra with dissolve
    
        #voice "Voise/HM/p_29485285_729.mp3"
        HM "— Ведьма — это не та, кто просто летает по небу и варит зелья,"

        e - "объясняла Наставница, "
        #voice "Voise/HM/p_29485306_875.mp3"
        HM "- Все это ведьме абсолютно без надобности, так… "
        #voice "Voise/HM/p_29544162_871.mp3"
        HM "внешние атрибуты... Ведьму определяет место, где она живёт... "
        #show HM s03 at razgavor, right onlayer xra with dissolve
    
        #show LW rn at razgavor, left with dissolve
        #show C at loposL onlayer demo
        #voice "Voise/LW/p_29544204_120.mp3"
        LW "— Разве мой теперешний дом – неподходящее место? "
        #hide C onlayer demo
        #show LW n at left with dissolve

        e "Спросила Маленькая Ведьма. "
        e "Наставница отвечала: "
    
        #show HM r01 at razgavor, right onlayer xra with dissolve
        #show V at loposR onlayer dexm
        #voice "Voise/HM/p_29544240_282.mp3"
        HM "— Совершенно неподходящее. "
        #show HM r02 at razgavor, right onlayer xra with dissolve
        #hide V onlayer dexm
        #show S01 at loposR onlayer dexm
        #voice "Voise/HM/p_29544272_592.mp3"
        HM "Ведьма живёт не в доме, не в определенном месте, не в средневековых рассказах и легендах. "
        #show HM r01 at razgavor, right onlayer xra with dissolve
        #voice "Voise/HM/p_29544288_700.mp3"
        HM "Настоящая ведьма живёт в пограничном состоянии – на границе разума, на границах материй, на границах миров. "
        #voice "Voise/HM/p_29544302_823.mp3"
        HM "Не важно: где твое тело, и где твой разум - он всегда должен быть в позиции неопределенности. "
        #voice "Voise/HM/p_29544315_940.mp3"

## Наставница продолжает.

        HM "Чтобы достигнуть этого пограничного состояния, – применяются различные техники"
        HM "Некоторые, стремясь достичь желаемого, используют различные предметы: карты Таро, "
        HM "магические кристаллы, зеркала, свечи… "
        HM "Другие {w=1}– употребляют особые вещества, чтобы изменить своё сознание и через него найти ту дверь внутри себя, ведущую «туда»… "
        HM "Ты же используешь сны, желая достичь Грани и постичь её…"

        #hide S01 onlayer dexm
        #show HM n at right onlayer xra with dissolve
    
        #show LW v02 at razgavor, left with dissolve
        #show V at loposL onlayer demo
        #voice "Voise/LW/p_29544379_352.mp3"
        LW "— Просто это в моей природе, "
        #hide V onlayer demo

        e "— отметила маленькая ведьма, "

        #show LW rn at razgavor, left with dissolve
        #voice "Voise/LW/p_29544399_473.mp3"
        LW " - Магия снов, и путешествие по ним."
        #show LW v01 at left with dissolve
    
        #show HM r01 at razgavor, right onlayer xra with dissolve
        #voice "Voise/HM/p_29544424_624.mp3"
        HM "— И тем не менее, в последнее время ты топчешься на месте,"
        #show HM n at right onlayer xra with dissolve
    
        e "— слегка покачав головой, заметила Наставница. "

        #show LW rn at razgavor, left with dissolve
        #show V at loposL onlayer demo
        #voice "Voise/LW/p_29544454_771.mp3"
        LW "— Но я постоянно практикуюсь! "
        #hide V onlayer demo
        #show LW n at left with dissolve
    
        e "– произнесла Маленькая Ведьма."

        #show HM r01 at razgavor, right onlayer xra with dissolve
        #voice "Voise/HM/p_29544470_882.mp3"
        HM "— Это всё техническая сторона дела, ты слишком много о ней думаешь..."
        #show HM n at right onlayer xra with dissolve

        e "— сказала Наставница. "

## Маленькая ведьма садится около кресла наставницы и кладёт голову на подлокотник.
## Теперь она выглядит совсем ребёнком.
    
        #show LW r at razgavor, left with dissolve
        #show VP at loposL onlayer demo
        #voice "Voise/LW/p_29633745_782.mp3"
        LW " - Расскажите тогда какую-нибудь сказку, которую я не знаю... "
        #show LW v01 at left with dissolve
    
        e "Маленькая ведьма просяще посмотрела на свою Наставницу,"
    
        #hide VP onlayer demo
        #show LW r at razgavor, left with dissolve
        #show V at loposL onlayer demo
        #show HM s02 at right onlayer xra with dissolve
   
        #voice "Voise/LW/p_29633805_932.mp3"
        LW "- Расскажите, расскажите..."
        #hide V onlayer demo
        #show LW s at left with dissolve
    
        e "Взгляд Наставницы отразил сожаление."

        #show HM r02 at razgavor, right onlayer xra with dissolve
        #show S02 at loposR onlayer dexm
        #voice "Voise/HM/p_29633842_72.mp3"
        HM " - Ты знаешь все сказки мира, "
        #show HM r01 at razgavor, right onlayer xra with dissolve

        e "- ответила она," 

        #voice "Voise/HM/p_29633868_185.mp3"
        HM "- Ты видишь во снах все миры, которые только существуют..."
        #voice "Voise/HM/p_29633904_310.mp3"
        HM "Ты знаешь все их истории, которые были когда-либо придуманы... "
        #voice "Voise/HM/p_29634078_35.mp3"
        HM "Я не могу рассказать того, что не существует и никогда не существовало..."
        #hide S02 onlayer dexm
        #show HM n at right onlayer xra with dissolve
    
        #show LW rn at razgavor, left with dissolve
        #voice "Voise/LW/p_29634193_212.mp3"
        LW " - Тогда можете придумать свою историю?"
        #show HM s04 at right onlayer xra with dissolve
        #show D at loposR onlayer dexm

        e "- спросила Маленькая Ведьма,"

        #voice "Voise/LW/p_29634203_285.mp3"
        LW " - Так же, как вы выдумываете разные миры…"
        #hide D onlayer dexm
        #show SF at loposR onlayer dexm
    
        e "Наставница о чем-то задумалась, а затем произнесла:"
    
        #show LW n at left with dissolve
        #hide SF onlayer dexm
        #show V at loposR onlayer dexm

## Наставница долго молчит. Затем неожиданно произносит:
    
        #show HM r03 at razgavor, right onlayer xra with dissolve
        #voice "Voise/HM/p_29634224_412.mp3"
        HM " - Во всем виноваты читатели."
        #hide V onlayer dexm
        #show HM n at right onlayer xra with dissolve
    
        #show LW s02 at razgavor, left with dissolve
        #show ZB at loposL onlayer demo
        #voice "Voise/LW/p_29634393_941.mp3"
        LW " - Читатели?!! Почему именно читатели? "
        #hide ZB onlayer demo
        #show LW n at left with dissolve
    

        e "Недоумевая, спросила Маленькая Ведьма, приподняв голову."

        #show HM r02 at razgavor, right onlayer xra with dissolve
        #show S02 at loposR onlayer dexm
        #voice "Voise/HM/p_29634610_610.mp3"
        HM " - Потому, что авторам приходится выворачиваться, чтобы заинтересовать читателей."
        #voice "Voise/HM/p_29634639_686.mp3"
        HM "Придумывая сюжет, им приходится посылать персонажей в опасные приключения и рисковать ими."
        #voice "Voise/HM/p_29634660_739.mp3"
        HM "А читателям ещё попробуй угодить..."
        #hide S02 onlayer dexm
        #show HM n at right onlayer xra with dissolve
    
        #show LW rn at razgavor, left with dissolve
        #show VP at loposL onlayer demo
        #voice "Voise/LW/p_29634674_839.mp3"
        LW " - Но без читателей - не было бы и писателей, "
        #show LW v01 at left with dissolve
        #hide VP onlayer demo

        e "– робко возразила Маленькая Ведьма."
    
        #show HM r01 at razgavor, right onlayer xra with dissolve
        #show B at loposR onlayer dexm
        #voice "Voise/HM/p_29634698_0.mp3"
        HM "- Но и без авторов не было бы читателей! получается парадокс..."
        #show HM n at right onlayer xra with dissolve
        #hide B onlayer dexm

        e "– заметила Наставница и призадумалась..."
    
        #show LW r at razgavor, left with dissolve
        #show V at loposL onlayer demo
        #voice "Voise/LW/p_29634753_256.mp3"
        LW "- Тогда во всем виноваты критики!"
        #show LW n at left with dissolve
        #hide V onlayer demo
    
        e "– предложила выход из парадокса Маленькая Ведьма."

        #show HM r03 at razgavor, right onlayer xra with dissolve
        #show ZB at loposR onlayer dexm
        #voice "Voise/HM/p_29634956_168.mp3"
        HM "- Критики?"
        #show HM n at right onlayer xra with dissolve
        #hide ZB onlayer dexm

        e "– Удивилась Наставника."
    
        #show LW r at razgavor, left with dissolve
        #show V at loposL onlayer demo
        #voice "Voise/LW/p_29635018_325.mp3"
        LW "- Критики,"
        #hide V onlayer demo

        e "- подтвердила маленькая ведьма. "

        #show LW rn at razgavor, left with dissolve
        #show S02 at loposL onlayer demo
        #voice "Voise/LW/p_29635064_467.mp3"
        LW "Прочитав произведения автора, они критикуют его, заставляя автора придумывать самые немыслимые приключения"
        #voice "Voise/LW/p_29635093_565.mp3"
        LW "для своих персонажей, что бы угодить их вкусу,"
        #hide S02 onlayer demo
        #show LW n at left with dissolve

        e "– подвела итог девочка."
    
        e "Наставница с ней согласилась. Помолчав какое-то время, она сказала:"
    
## Наставница устало откидывается в кресле.
## Звёзды на её одежде медленно плывут, как галактики во сне.

        #show HM r02 at razgavor, right onlayer xra with dissolve
        #show GI at loposR onlayer dexm
        #voice "Voise/HM/p_29635190_869.mp3"
        #$ renpy.pause(4.0)
        #voice "Voise/HM/p_29635223_926.mp3"
        HM " - Я очень устала, и не смогу сегодня ничего придумать. {w=1} А вот завтра... "
        #voice "Voise/HM/p_29635238_977.mp3"
        $ renpy.pause(1.0)
        #voice "Voise/HM/p_29635271_40.mp3"
        HM " да, завтра {w=1} ты увидишь новую историю, которую ещё не знаешь." 
        #voice "Voise/HM/p_29635311_150.mp3"
        HM "И которая, возможно, поможет тебе в пути к тому, что ты ищешь…"
        #show HM n at right onlayer xra with dissolve
        #hide GI onlayer dexm
        e "..."
        #hide LW n
        #hide TR
        #hide plate
        #hide HM n onlayer xra 
        #with pixellate
        #scene bg059 
        #with dissA

## Мрачные чертоги постепенно становятся уютнее. Чёрный трон похож уже на старое кресло. Космическая бездна — на тёмную комнату, освещённую мягким светом.
## Маленькая ведьма осторожно поднимается.
## Она ещё немного стоит рядом с наставницей.
## Потом на цыпочках идёт к выходу.
## Перед дверью оборачивается.
## Наставница спит.
## Маленькая ведьма тихо улыбается и неслышно выскальзывает наружу, не потревожив её сны.
## Затемнение.


    
        e "Наставница погрузилась в дрёму. "
        e "Маленькая Ведьма не стала ее будить, кинув на наставницу умилённый взгляд."
    
        #scene bg040a with dissA
        #show LW v01 at left with dissolve
        #show N at loposL onlayer demo


        e "Оглянувшись по сторонам,"
        e " она обнаружила себя посреди абсолютно тривиального убранства обычной хижины – вещей, мебели, книжных полок у деревянных стен… "
        e "Как будто и не было безразмерного и пугающего космического пространства, раскрашенного термоядерным звёздным блеском… "
        e "Маленькая Ведьма ненадолго осталась в этом уютном домике,"
        e " а затем {w=1}- неслышно выскользнула наружу, стараясь не потревожив сон своей Наставницы…"
 
  
    
        #hide N onlayer demo
        #hide LW v01
        #show LW n at Transform(function=move_rotate_zoom)
        #stop music fadeout 1.0
        #scene bg000b with icenteriss
        e "****************************************************"

        jump chapter2 
        #with diss
    
        return