import pygame as pg, numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram # для работы с шейдарами

# язык шейдеров на языке С
vertax_src = """
#version 440

in vec3 vertax_position; // координаты вершин
in vec3 in_color;
out vec3 out_color;

void main(){
    /* передаём координаты на следующие
     * этапы графического конвейера
     * без преобразований.
    */
    gl_Position = vec4(vertax_position, 1.0); // ИСПРАВЛЕНО: Теперь gl_Position получает vec4

    // передаём цвета в формате шейдера
    out_color = in_color;
}


"""


if __name__ == "__main__":
    # обьяснение для начала работы с OpenGL

    pg.init()
    s = pg.display.set_mode((500,500), pg.DOUBLEBUF | pg.OPENGL)
    r = 1
    glClearColor(200/255,154/255,255/255, 1) #// задаём цве GL

    t = np.array([
    #//  x    y    z      r       g      b
        0.0, 0.5, 0.0, 52/255, 52/255, 52/255,
        -0.5, -0.5, 0.0, 52/255, 52/255, 52/255,
        0.5, -0.5, 0.0, 52/255, 52/255, 52/255,
    ], dtype=np.float32)

    # создаём буфер
    t_buffer = glGenBuffers(1) # glGenBuffers(количество даных)

    # привязываем буфер что бы загрузить даные
    glBindBuffer(GL_ARRAY_BUFFER, t_buffer)
    # в дальнейшим все команды будут действовать на этот буфер
    # GL_ARRAY_BUFFER - цель привязки

    # передаём данные из масива в буфер
    glBufferData(GL_ARRAY_BUFFER, t.nbytes, t, GL_STATIC_DRAW) # glBufferData(GL_ARRAY_BUFFER, байты, масив, команда)
    # GL_STATIC_DRAW - STATIC: загружает даные 1 раз, DRAW - даные для рисования

    # Считаем даные из буфера
    buffer_data = glGetBufferSubData(GL_ARRAY_BUFFER, 0, t.nbytes) # glGetBufferSubData(GL_ARRAY_BUFFER, смещение в байтах, количество байтив)

    # вывод двные в консоль
    print(buffer_data.view(dtype=np.float32))
    '''
    [ 0.          0.5         0.          0.20392157  0.20392157  0.20392157
    -0.5        -0.5         0.          0.20392157  0.20392157  0.20392157
     0.5        -0.5         0.          0.20392157  0.20392157  0.20392157]
    '''

    # КОМПИЛЯЦИЯ ШЕЙДЕРА    
    v_shader = compileShader(vertax_src, GL_VERTEX_SHADER) #// compileShader( шейдер на С, тип шейдера)

    while r:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                r = 0
        glClear(GL_COLOR_BUFFER_BIT) #// очистка экрана GL
        pg.display.flip()

    pg.quit()