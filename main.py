from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

Window.clearcolor = (0.1, 0.1, 0.1, 1)
Window.size = (360, 640)

class CalculatorWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 5
        self.padding = 10
        
        # 显示区域
        self.display = Label(
            text='0',
            font_size='40sp',
            size_hint=(1, 0.3),
            halign='right',
            valign='center',
            color=(1, 1, 1, 1)
        )
        self.display.bind(size=self.display.setter('text_size'))
        self.add_widget(self.display)
        
        # 按钮区域
        buttons = [
            ['C', '±', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '⌫', '=']
        ]
        
        grid = GridLayout(cols=4, spacing=5, size_hint=(1, 0.7))
        
        for row in buttons:
            for btn_text in row:
                btn = Button(
                    text=btn_text,
                    font_size='24sp',
                    background_normal='',
                    background_color=self._get_btn_color(btn_text)
                )
                btn.bind(on_press=self.on_button_press)
                grid.add_widget(btn)
        
        self.add_widget(grid)
        
        self.current_input = '0'
        self.last_result = None
        self.operator = None
        self.new_input = True
    
    def _get_btn_color(self, text):
        if text in ['C', '±', '%']:
            return (0.6, 0.6, 0.6, 1)
        elif text in ['÷', '×', '-', '+', '=']:
            return (1, 0.6, 0, 1)
        elif text == '⌫':
            return (0.3, 0.3, 0.3, 1)
        else:
            return (0.2, 0.2, 0.2, 1)
    
    def on_button_press(self, instance):
        text = instance.text
        
        if text == 'C':
            self.current_input = '0'
            self.operator = None
            self.last_result = None
            self.new_input = True
        
        elif text == '±':
            if self.current_input.startswith('-'):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
        
        elif text == '%':
            try:
                value = float(self.current_input)
                self.current_input = str(value / 100)
            except:
                self.current_input = 'Error'
        
        elif text == '⌫':
            if len(self.current_input) > 1:
                self.current_input = self.current_input[:-1]
            else:
                self.current_input = '0'
        
        elif text in ['÷', '×', '-', '+']:
            try:
                current = float(self.current_input)
                if self.operator and self.last_result is not None and not self.new_input:
                    result = self._calculate(self.last_result, current, self.operator)
                    self.last_result = result
                else:
                    self.last_result = current
                self.operator = text
                self.new_input = True
            except:
                self.current_input = 'Error'
        
        elif text == '=':
            try:
                current = float(self.current_input)
                if self.operator and self.last_result is not None:
                    result = self._calculate(self.last_result, current, self.operator)
                    self.current_input = str(result)
                    self.last_result = None
                    self.operator = None
                    self.new_input = True
            except:
                self.current_input = 'Error'
        
        else:  # 数字和小数点
            if self.new_input:
                self.current_input = text if text != '.' else '0.'
                self.new_input = False
            else:
                if text == '.' and '.' in self.current_input:
                    pass
                else:
                    if self.current_input == '0' and text != '.':
                        self.current_input = text
                    else:
                        self.current_input += text
        
        # 更新显示
        display_text = self.current_input
        if len(display_text) > 12:
            try:
                display_text = f"{float(display_text):.8g}"
            except:
                pass
        self.display.text = display_text
    
    def _calculate(self, a, b, op):
        if op == '+':
            return a + b
        elif op == '-':
            return a - b
        elif op == '×':
            return a * b
        elif op == '÷':
            if b == 0:
                return 'Error'
            return a / b
        return b

class CalculatorApp(App):
    def build(self):
        return CalculatorWidget()

if __name__ == '__main__':
    CalculatorApp().run()
