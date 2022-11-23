import sys
import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import pyrr
import math

def framebuffer_callback(window, width, height):
  glViewport(0, 0, width, height)
  
def process_input(window):
  if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
    glfw.set_window_should_close(window, True)
  if glfw.get_key(window, glfw.KEY_G) == glfw.PRESS:
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
  if glfw.get_key(window, glfw.KEY_F) == glfw.PRESS:
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
 
 
def main():
  if not glfw.init():
    return
    
  glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
  glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
  glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

  window = glfw.create_window(800, 600, "Pietro", None, None)
  glfw.make_context_current(window)
  glfw.set_framebuffer_size_callback(window, framebuffer_callback)
  
  vertices = np.array([
    0.5, 0.5, 0.0, 
    0.5, -0.5, 0.0, 
    -0.5,  -0.5, 0.0,
    -0.5, 0.5, 0.0
  ], dtype=np.float32)
  
  indices = np.array([
    0, 1, 3,
    1, 2, 3
  ], dtype=np.uint32)
  
  
  VERTEX_SHADER = """
      #version 330

      in vec4 position;
      void main() {
        gl_Position = vec4(position.x, position.y, position.z, 1.0);

      }
  """


  FRAGMENT_SHADER = """
      #version 330

      void main() {

      gl_FragColor = 

        vec4(1.0f, 0.5f, 0.2f, 1.0f);

      }
  """
  
  vs_compiled = OpenGL.GL.shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER)
  fs_compiled = OpenGL.GL.shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
  
  shader = OpenGL.GL.shaders.compileProgram(vs_compiled, fs_compiled)
  
  glDeleteShader(vs_compiled)
  glDeleteShader(fs_compiled)
  
  glUseProgram(shader)
  
  #Create Buffer object in gpu
  VBO = glGenBuffers(1)
  VAO = glGenVertexArrays(1)
  EBO = glGenBuffers(1)
  
  glBindVertexArray(VAO)

  #Bind the buffer
  glBindBuffer(GL_ARRAY_BUFFER, VBO)
  glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

  glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
  glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)


  #get the position from vertex shader
  position = glGetAttribLocation(shader, 'position')
  glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
  glEnableVertexAttribArray(position)
  
  glBindBuffer(GL_ARRAY_BUFFER, 0)
  
  glBindVertexArray(0)  
  
  while not glfw.window_should_close(window):
    
    glfw.poll_events()
    process_input(window)
    
    glClearColor(0.2, 0.3, 0.3, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    
    glUseProgram(shader)
    glBindVertexArray(VAO)
    
    #glDrawArrays(GL_TRIANGLES, 0, 3)
    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
    #glBindVertexArray(0)
    
    glfw.swap_buffers(window)
    
  glDeleteVertexArrays(1, np.array(VAO).tolist())
  glDeleteBuffers(1, np.array(VBO).tolist())
  glDeleteProgram(shader)
  glfw.terminate()
 
if __name__ == "__main__":
    main()