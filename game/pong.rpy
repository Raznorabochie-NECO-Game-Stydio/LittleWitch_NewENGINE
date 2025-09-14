label pong:

    init python:

        class PongDisplayable(renpy.Displayable):

            def __init__(self):

                renpy.Displayable.__init__(self)


                # Размер некоторых изображений.
                self.PADDLE_WIDTH = 12
                self.PADDLE_HEIGHT = 95
                self.PADDLE_X = 240
                self.BALL_WIDTH = 15
                self.BALL_HEIGHT = 15
                self.COURT_TOP = 194
                self.COURT_BOTTOM = 975


                # Используемые визуальные объекты.
                self.paddle = Solid("#ffffff", xsize=self.PADDLE_WIDTH, ysize=self.PADDLE_HEIGHT)
                self.ball = Solid("#ffffff", xsize=self.BALL_WIDTH, ysize=self.BALL_HEIGHT)

                # Прилеплен ли мячик к платформе.
                self.stuck = True

                # Позиции платформ.
                self.playery = (self.COURT_BOTTOM - self.COURT_TOP) / 2
                self.computery = self.playery

                # Скорость компьютерного игрока.
                self.computerspeed = 380.0

                # Позиция, направление и скорость мячика
                self.bx = self.PADDLE_X + self.PADDLE_WIDTH + 10
                self.by = self.playery
                self.bdx = .5
                self.bdy = .5
                self.bspeed = 350.0

                # Время с предыдущего кадра.
                self.oldst = None

                # победитель.
                self.winner = None

            def visit(self):
                return [ self.paddle, self.ball ]

            # Перечитывает позицию мячика, организует отскоки, и
            # отрисовывает экран.
            def render(self, width, height, st, at):

                # Объект Render, в котором будет вестись отрисовка.
                r = renpy.Render(width, height)

                # Сколько времени прошло с предыдущего кадра.
                if self.oldst is None:
                    self.oldst = st

                dtime = st - self.oldst
                self.oldst = st

                # Где будет мячик.
                speed = dtime * self.bspeed
                oldbx = self.bx

                if self.stuck:
                    self.by = self.playery
                else:
                    self.bx += self.bdx * speed
                    self.by += self.bdy * speed

                # Перемещает платформу компьютерного игрока. Стремится к self.by, 
                # но может быть ограничен скоростью реакции.
                cspeed = self.computerspeed * dtime
                if abs(self.by - self.computery) <= cspeed:
                    self.computery = self.by
                else:
                    self.computery += cspeed * (self.by - self.computery) / abs(self.by - self.computery)

                # Организация отскоков.

                # от верхнего края.
                ball_top = self.COURT_TOP + self.BALL_HEIGHT / 2
                if self.by < ball_top:
                    self.by = ball_top + (ball_top - self.by)
                    self.bdy = -self.bdy

                    if not self.stuck:
                        renpy.sound.play("images/pong/pong_beep.wav", channel=0)

                # От нижнего края.
                ball_bot = self.COURT_BOTTOM - self.BALL_HEIGHT / 2
                if self.by > ball_bot:
                    self.by = ball_bot - (self.by - ball_bot)
                    self.bdy = -self.bdy

                    if not self.stuck:
                        renpy.sound.play("images/pong/pong_beep.wav", channel=0)

                # Отрисовывает платформы, и организует отскоки от них.                       
                def paddle(px, py, hotside):

                    # Отрисовка изображеия платформы. мы даём ему область 800x600
                    # для отрисовки, зная, что изображения отрисуются по своему размеру.
                    # (Это истинно не для всех визуальных объектов. Solid, Frame,
                    # и Fixed расширяются, чтобы занять всё область.)
                    # Также передаём st и at.
                    pi = renpy.render(self.paddle, width, height, st, at)

                    # renpy.render возвращает объект Render, который мы можем
                    # blit к Render'y мы создаём.
                    r.blit(pi, (int(px), int(py - self.PADDLE_HEIGHT / 2)))

                    if py - self.PADDLE_HEIGHT / 2 <= self.by <= py + self.PADDLE_HEIGHT / 2:

                        hit = False

                        if oldbx >= hotside >= self.bx:
                            self.bx = hotside + (hotside - self.bx)
                            self.bdx = -self.bdx
                            hit = True

                        elif oldbx <= hotside <= self.bx:
                            self.bx = hotside - (self.bx - hotside)
                            self.bdx = -self.bdx
                            hit = True

                        if hit:
                            renpy.sound.play("images/pong/pong_boop.wav", channel=1)
                            self.bspeed *= 1.10

                # Рисует две платформы.
                paddle(self.PADDLE_X, self.playery, self.PADDLE_X + self.PADDLE_WIDTH)
                paddle(width - self.PADDLE_X - self.PADDLE_WIDTH, self.computery, width - self.PADDLE_X - self.PADDLE_WIDTH)

                # Рисует мячик.
                ball = renpy.render(self.ball, width, height, st, at)
                r.blit(ball, (int(self.bx - self.BALL_WIDTH / 2),
                              int(self.by - self.BALL_HEIGHT / 2)))

                # Выясняет победителя.
                if self.bx < -50:
                    self.winner = "eileen"

                    # Нужно для того, чтобы быть уверенным в том
                    # что событие вызвано.
                    renpy.timeout(0)

                elif self.bx > width + 50:
                    self.winner = "player"
                    renpy.timeout(0)

                # Просит перерисовать как можно скорее, дабы
                # мы могли отобразить следующий кадр.
                renpy.redraw(self, 0)

                # Возвращает объект Render.
                return r

            # Обработка событий.
            def event(self, ev, x, y, st):

                import pygame

                # Нажатие кнопки мыши == начало игры, путём установки

                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    self.stuck = False

                    # Ensure the pong screen updates.
                    renpy.restart_interaction()

                # Установка платформ игроков.
                y = max(y, self.COURT_TOP)
                y = min(y, self.COURT_BOTTOM)
                self.playery = y

                # Если есть победитель, он возвращается основной игре. 
                # В противном случае текущее событие игнорируется.
                if self.winner:
                    return self.winner
                else:
                    raise renpy.IgnoreEvent()

    screen pong():

        default pong = PongDisplayable()

        add "bg pong field"

        add pong

        text _("Ты"):
            xpos 240
            xanchor 0.5
            ypos 25
            size 40

        text _("Противнег"):
            xpos (1920 - 240)
            xanchor 0.5
            ypos 25
            size 40

        if pong.stuck:
            text _("Нажми чтобы начать"):
                xalign 0.5
                ypos 50
                size 40

