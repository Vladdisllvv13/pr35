from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window

Window.size = (400, 600)

class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector( -1* vx,  vy)
            vel = bounced * 1.1
            ball.velocity = vel.y, vel.x + offset


class PongBall(Widget):
    # скорость мяча по осям x и y
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    # сокращение, как, например, w.pos для w.x и w.y (Ссылочное свойство)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    #Перемещение мяча на один шаг
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball(self, vel=(0, 4)):
        self.ball.center = self.center
        self.ball.velocity = vel

    #Отслеживание отбивания мяча и перемещения
    def update(self, dt):
        self.ball.move()

        # bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # отскакивает сверху и снизу
        if (self.ball.y < self.y):
            self.serve_ball(vel=(0, 2))
            self.player1.score += 1

        if (self.ball.top > self.top):
            self.serve_ball(vel=(0, -2))
            self.player2.score += 1

        # отскакивать влево и вправо
        if self.ball.x < self.x:
            self.ball.velocity_x *= -1
            
        if self.ball.right > self.width:
            self.ball.velocity_x *= -1

    #Реагирование виджета на ввод
    def on_touch_move(self, touch):
        if touch.y < self.width / 3:
            self.player1.center_x = touch.x
        if touch.y > self.width - self.width / 3:
            self.player2.center_x = touch.x


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        #Вызов метода перемещения мяча, регулярно
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    PongApp().run()