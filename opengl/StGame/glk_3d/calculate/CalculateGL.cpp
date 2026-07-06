#include <iostream>
#include <vector>
#include <array>
#include <cmath>
#include <memory>
#include <fstream>
#include <sstream>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

// Базовые OpenGL заголовки
#ifdef _WIN32
    #include <windows.h>
#endif
#include <GL/gl.h>
#include <GL/glu.h>

using namespace std;
namespace py = pybind11;

float degrees_to_radians(float deg) {
    return deg * acosf(-1.0f) / 180.0f;
}

class TextureGL {
public:
    TextureGL() : texture_id(0), width(0), height(0), channels(0) {}
    ~TextureGL() {
        if (texture_id != 0) {
            glDeleteTextures(1, &texture_id);
        }
    }

    bool load_from_data(const py::array_t<unsigned char>& image_data, 
                       int width_, int height_, int channels_ = 3) {
        py::buffer_info buf = image_data.request();
        
        if (buf.ndim != 3) {
            throw std::runtime_error("Image data must be 3D array (height, width, channels)");
        }
        
        width = width_;
        height = height_;
        channels = channels_;
        
        glGenTextures(1, &texture_id);
        glBindTexture(GL_TEXTURE_2D, texture_id);
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
        
        GLenum format;
        if (channels == 3)
            format = GL_RGB;
        else if (channels == 4)
            format = GL_RGBA;
        else if (channels == 1)
            format = GL_LUMINANCE;
        else {
            throw std::runtime_error("Unsupported number of channels");
        }
        
        const unsigned char* data = static_cast<unsigned char*>(buf.ptr);
        glTexImage2D(GL_TEXTURE_2D, 0, format, width, height, 0, format, GL_UNSIGNED_BYTE, data);
        
        glBindTexture(GL_TEXTURE_2D, 0);
        return true;
    }
    
    bool create_color_texture(int width_, int height_, const std::array<unsigned char, 3>& color) {
        width = width_;
        height = height_;
        channels = 3;
        
        std::vector<unsigned char> data(static_cast<size_t>(width) * static_cast<size_t>(height) * 3);
        for (int i = 0; i < width * height; ++i) {
            data[static_cast<size_t>(i) * 3 + 0] = color[0];
            data[static_cast<size_t>(i) * 3 + 1] = color[1];
            data[static_cast<size_t>(i) * 3 + 2] = color[2];
        }
        
        glGenTextures(1, &texture_id);
        glBindTexture(GL_TEXTURE_2D, texture_id);
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
        
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, data.data());
        
        glBindTexture(GL_TEXTURE_2D, 0);
        return true;
    }
    
    bool create_checker_texture(int size = 64) {
        width = size;
        height = size;
        channels = 3;
        
        std::vector<unsigned char> data(static_cast<size_t>(size) * static_cast<size_t>(size) * 3);
        for (int i = 0; i < size; ++i) {
            for (int j = 0; j < size; ++j) {
                int index = (i * size + j) * 3;
                if ((i / 8 + j / 8) % 2 == 0) {
                    data[index + 0] = 255;  // R
                    data[index + 1] = 0;    // G
                    data[index + 2] = 0;    // B
                } else {
                    data[index + 0] = 255;  // R
                    data[index + 1] = 255;  // G
                    data[index + 2] = 0;    // B
                }
            }
        }
        
        glGenTextures(1, &texture_id);
        glBindTexture(GL_TEXTURE_2D, texture_id);
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
        
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, size, size, 0, GL_RGB, GL_UNSIGNED_BYTE, data.data());
        
        glBindTexture(GL_TEXTURE_2D, 0);
        return true;
    }
    
    void bind() { 
        glBindTexture(GL_TEXTURE_2D, texture_id); 
    }
    
    void unbind() { 
        glBindTexture(GL_TEXTURE_2D, 0); 
    }
    
    GLuint get_texture_id() const { return texture_id; }
    int get_width() const { return width; }
    int get_height() const { return height; }

private:
    GLuint texture_id;
    int width, height, channels;
};

class OBJLoader {
public:
    struct Face {
        std::vector<int> vertex_indices;
        std::vector<int> tex_coord_indices;
        std::vector<int> normal_indices;
    };

    static bool load_obj(const std::string& filename, 
                        std::vector<std::array<float, 3>>& vertices,
                        std::vector<std::array<float, 2>>& tex_coords,
                        std::vector<std::array<float, 3>>& normals,
                        std::vector<Face>& faces) {
        
        std::ifstream file(filename);
        if (!file.is_open()) {
            std::cerr << "Cannot open OBJ file: " << filename << std::endl;
            return false;
        }

        vertices.clear();
        tex_coords.clear();
        normals.clear();
        faces.clear();

        std::string line;
        while (std::getline(file, line)) {
            std::istringstream iss(line);
            std::string type;
            iss >> type;

            if (type == "v") {  // Vertex
                float x, y, z;
                iss >> x >> y >> z;
                vertices.push_back({x, y, z});
            }
            else if (type == "vt") {  // Texture coordinate
                float u, v;
                iss >> u >> v;
                tex_coords.push_back({u, v});
            }
            else if (type == "vn") {  // Normal
                float x, y, z;
                iss >> x >> y >> z;
                normals.push_back({x, y, z});
            }
            else if (type == "f") {  // Face
                Face face;
                std::string vertex_str;
                
                while (iss >> vertex_str) {
                    std::replace(vertex_str.begin(), vertex_str.end(), '/', ' ');
                    std::istringstream vss(vertex_str);
                    
                    int v_idx, t_idx, n_idx;
                    vss >> v_idx;
                    
                    if (vss >> t_idx) {
                        // Has texture coordinate
                    } else {
                        t_idx = 0;
                    }
                    
                    if (vss >> n_idx) {
                        // Has normal
                    } else {
                        n_idx = 0;
                    }
                    
                    // OBJ indices are 1-based, convert to 0-based
                    face.vertex_indices.push_back(v_idx - 1);
                    face.tex_coord_indices.push_back(t_idx - 1);
                    face.normal_indices.push_back(n_idx - 1);
                }
                
                faces.push_back(face);
            }
        }

        file.close();
        return true;
    }

    static void convert_faces_to_quads(const std::vector<Face>& faces,
                                      std::vector<std::array<short, 4>>& quad_faces) {
        quad_faces.clear();
        
        for (const auto& face : faces) {
            if (face.vertex_indices.size() == 4) {
                // Already a quad
                quad_faces.push_back({
                    static_cast<short>(face.vertex_indices[0]),
                    static_cast<short>(face.vertex_indices[1]),
                    static_cast<short>(face.vertex_indices[2]),
                    static_cast<short>(face.vertex_indices[3])
                });
            }
            else if (face.vertex_indices.size() == 3) {
                // Convert triangle to quad by duplicating last vertex
                quad_faces.push_back({
                    static_cast<short>(face.vertex_indices[0]),
                    static_cast<short>(face.vertex_indices[1]),
                    static_cast<short>(face.vertex_indices[2]),
                    static_cast<short>(face.vertex_indices[2])
                });
            }
            // For polygons with more than 4 vertices, we'd need triangulation
        }
    }

    static void generate_edges_from_faces(const std::vector<Face>& faces,
                                         std::vector<std::array<short, 2>>& edges) {
        edges.clear();
        std::set<std::pair<short, short>> edge_set;  // To avoid duplicates
        
        for (const auto& face : faces) {
            int vertex_count = face.vertex_indices.size();
            for (int i = 0; i < vertex_count; ++i) {
                int next_i = (i + 1) % vertex_count;
                short v1 = static_cast<short>(face.vertex_indices[i]);
                short v2 = static_cast<short>(face.vertex_indices[next_i]);
                
                // Add edge in sorted order to avoid duplicates
                if (v1 < v2) {
                    edge_set.insert({v1, v2});
                } else {
                    edge_set.insert({v2, v1});
                }
            }
        }
        
        // Convert set to vector
        for (const auto& edge : edge_set) {
            edges.push_back({edge.first, edge.second});
        }
    }
};

class _FigurGL {
public:
    _FigurGL(short width_, short height_, const std::array<float, 3>& position_ = {0.0f, 0.0f, 0.0f}) 
        : width(width_), height(height_), position(position_) {
        
        line_color = {1.0f, 1.0f, 1.0f, 1.0f};
        point_color = {1.0f, 0.0f, 0.0f, 1.0f};
        line_width = 2.0f;
        point_size = 5.0f;
        use_texture = false;
    }

    // Загрузка OBJ файла
    bool load_obj(const std::string& filename) {
        std::vector<std::array<float, 3>> vertices;
        std::vector<std::array<float, 2>> tex_coords;
        std::vector<std::array<float, 3>> normals;
        std::vector<OBJLoader::Face> faces;
        
        if (!OBJLoader::load_obj(filename, vertices, tex_coords, normals, faces)) {
            return false;
        }
        
        // Преобразуем faces в формат четырехугольников
        std::vector<std::array<short, 4>> quad_faces;
        OBJLoader::convert_faces_to_quads(faces, quad_faces);
        
        // Генерируем edges из faces
        std::vector<std::array<short, 2>> edges;
        OBJLoader::generate_edges_from_faces(faces, edges);
        
        // Устанавливаем данные
        set_vertices_array(vertices);
        set_faces(quad_faces);
        set_edges(edges);
        
        // Если есть текстурные координаты, устанавливаем их
        if (!tex_coords.empty()) {
            set_texture_coords_array(tex_coords);
        } else {
            // Автоматически генерируем текстурные координаты
            generate_auto_tex_coords();
        }
        
        return true;
    }

    void set_vertices(const py::array_t<float>& vertices) {
        py::buffer_info buf = vertices.request();
        if (buf.ndim != 2 || buf.shape[1] != 3) {
            throw std::runtime_error("Vertices array must be 2D with shape (N, 3)");
        }

        size_t vertex_count = static_cast<size_t>(buf.shape[0]);
        _vertices.resize(vertex_count);
        rot_vertices.resize(vertex_count);
        float* ptr = static_cast<float*>(buf.ptr);

        for (size_t i = 0; i < vertex_count; ++i) {
            for (int j = 0; j < 3; ++j) {
                _vertices[i][j] = ptr[i * 3 + j];
                rot_vertices[i][j] = ptr[i * 3 + j];
            }
        }
    }

    // Внутренний метод для установки вершин из C++ вектора
    void set_vertices_array(const std::vector<std::array<float, 3>>& vertices) {
        _vertices = vertices;
        rot_vertices = vertices;
    }

    void set_edges(const std::vector<std::array<short, 2>>& new_edges) {
        edges = new_edges;
    }

    void set_faces(const std::vector<std::array<short, 4>>& new_faces) {
        faces = new_faces;
    }

    void set_texture_coords(const py::array_t<float>& coords) {
        py::buffer_info buf = coords.request();
        if (buf.ndim != 2 || buf.shape[1] != 2) {
            throw std::runtime_error("TextureGL coordinates array must be 2D with shape (N, 2)");
        }

        size_t coord_count = static_cast<size_t>(buf.shape[0]);
        tex_coords.resize(coord_count);
        float* ptr = static_cast<float*>(buf.ptr);
        for (size_t i = 0; i < coord_count; ++i) {
            for (int j = 0; j < 2; ++j) {
                tex_coords[i][j] = ptr[i * 2 + j];
            }
        }
    }

    // Внутренний метод для установки текстурных координат из C++ вектора
    void set_texture_coords_array(const std::vector<std::array<float, 2>>& coords) {
        tex_coords = coords;
    }

    void generate_auto_tex_coords() {
        tex_coords.resize(_vertices.size());
        for (size_t i = 0; i < _vertices.size(); ++i) {
            // Простая проекция: используем X и Z координаты для UV
            // Это работает хорошо для большинства моделей
            tex_coords[i][0] = (_vertices[i][0] + 1.0f) / 2.0f;
            tex_coords[i][1] = (_vertices[i][2] + 1.0f) / 2.0f;
        }
    }

    void set_texture(const std::shared_ptr<TextureGL>& texture_ptr) {
        texture = texture_ptr;
        use_texture = (texture != nullptr);
    }

    void enable_texture(bool enable) {
        use_texture = enable && (texture != nullptr);
    }

    void update(float distans = 0.0f) {
        projected_vertices.clear();
        for (size_t i = 0; i < rot_vertices.size(); ++i) {
            float x = rot_vertices[i][0];
            float y = rot_vertices[i][1];
            float z = rot_vertices[i][2];
            z -= distans;

            float z_factor = (z + static_cast<float>(fov) > 0.1f) ? 
                static_cast<float>(fov) / (static_cast<float>(fov) + z) : 0.0f;
            float x_proj = x * -z_factor;
            float y_proj = y * z_factor;

            std::array<int, 2> projected_vertex;
            if (z_factor > 0.0f) {
                projected_vertex[0] = static_cast<int>((x_proj + 1) * static_cast<float>(width) / 2.0f);
                projected_vertex[1] = static_cast<int>((1 - y_proj) * static_cast<float>(height) / 2.0f);
            } else {
                projected_vertex[0] = -1000;
                projected_vertex[1] = -1000;
            }
            projected_vertices.push_back(projected_vertex);
        }
    }

    void turn_x(float rads) {
        float angle = degrees_to_radians(rads);
        float cos_angle = cosf(angle);
        float sin_angle = sinf(angle);
        for (size_t i = 0; i < rot_vertices.size(); ++i) {
            float x = rot_vertices[i][0];
            float z = rot_vertices[i][2];
            rot_vertices[i][0] = x * cos_angle + z * sin_angle;
            rot_vertices[i][2] = -x * sin_angle + z * cos_angle;
        }
    }

    void turn_y(float rads) {
        float angle = degrees_to_radians(rads);
        float cos_angle = cosf(angle);
        float sin_angle = sinf(angle);
        for (size_t i = 0; i < rot_vertices.size(); ++i) {
            float y = rot_vertices[i][1];
            float z = rot_vertices[i][2];
            rot_vertices[i][1] = y * cos_angle - z * sin_angle;
            rot_vertices[i][2] = y * sin_angle + z * cos_angle;
        }
    }

    void turn_z(float rads) {
        float angle = degrees_to_radians(rads);
        float cos_angle = cosf(angle);
        float sin_angle = sinf(angle);
        for (size_t i = 0; i < rot_vertices.size(); ++i) {
            float x = rot_vertices[i][0];
            float y = rot_vertices[i][1];
            rot_vertices[i][0] = x * cos_angle - y * sin_angle;
            rot_vertices[i][1] = x * sin_angle + y * cos_angle;
        }
    }


    void render_3d_scene() {
    // НАСТРОЙКА OpenGL - ОСТАВЛЯЕМ
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho(0, width, height, 0, -1, 1);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    
    // УБИРАЕМ ОЧИСТКУ ЭКРАНА ЗДЕСЬ!
    // glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
    // glClear(GL_COLOR_BUFFER_BIT);
    
    // Отрисовка текстурированных граней
    if (use_texture && texture && !faces.empty() && tex_coords.size() >= _vertices.size()) {
        glEnable(GL_TEXTURE_2D);
        texture->bind();
        glColor4f(1.0f, 1.0f, 1.0f, 1.0f);
        
        for (const auto& face : faces) {
            glBegin(GL_QUADS);
            for (int i = 0; i < 4; ++i) {
                short vertex_index = face[i];
                if (vertex_index >= 0 && static_cast<size_t>(vertex_index) < projected_vertices.size() &&
                    static_cast<size_t>(vertex_index) < tex_coords.size()) {
                    const auto& vertex = projected_vertices[static_cast<size_t>(vertex_index)];
                    const auto& tex_coord = tex_coords[static_cast<size_t>(vertex_index)];
                    if (vertex[0] >= 0 && vertex[1] >= 0) {
                        glTexCoord2f(tex_coord[0], tex_coord[1]);
                        glVertex2i(vertex[0], vertex[1]);
                    }
                }
            }
            glEnd();
        }
        
        glDisable(GL_TEXTURE_2D);
    }
    
    // Отрисовка линий (каркас)
    if (draw_lines) {  // Добавляем проверку на включение линий
        glLineWidth(line_width);
        glColor4f(line_color[0], line_color[1], line_color[2], line_color[3]);
        
        glBegin(GL_LINES);
        for (const auto& edge : edges) {
            if (edge[0] >= 0 && static_cast<size_t>(edge[0]) < projected_vertices.size() &&
                edge[1] >= 0 && static_cast<size_t>(edge[1]) < projected_vertices.size()) {
                
                const auto& start = projected_vertices[static_cast<size_t>(edge[0])];
                const auto& end = projected_vertices[static_cast<size_t>(edge[1])];
                
                if (start[0] >= 0 && start[1] >= 0 && end[0] >= 0 && end[1] >= 0) {
                    glVertex2i(start[0], start[1]);
                    glVertex2i(end[0], end[1]);
                }
            }
        }
        glEnd();
    }
    
    // Отрисовка точек
    if (draw_point) {  // Добавляем проверку на включение точек
        glPointSize(point_size);
        glColor4f(point_color[0], point_color[1], point_color[2], point_color[3]);
        
        glBegin(GL_POINTS);
        for (const auto& vertex : projected_vertices) {
            if (vertex[0] >= 0 && vertex[1] >= 0) {
                glVertex2i(vertex[0], vertex[1]);
            }
        }
        glEnd();
    }
}

    
    

    // Геттеры
    const std::vector<std::array<int, 2>>& get_projected_vertices() const { 
        return projected_vertices; 
    }
    
    std::vector<std::array<short, 2>> get_edges() const {
        return edges;
    }

    // Сеттеры
    void set_line_color(const std::array<float, 4>& color) { line_color = color; }
    void set_point_color(const std::array<float, 4>& color) { point_color = color; }
    void set_line_width(float width) { line_width = width; }
    void set_point_size(float size) { point_size = size; }
    
    void enable_lines(bool draw) {draw_lines = draw; }
    void enable_point(bool draw) {draw_point = draw; }
private:

    int fov = 5;
    short height, width;
    std::array<float, 3> position = {0.0f, 0.0f, 0.0f};
    
    std::array<float, 4> line_color;
    std::array<float, 4> point_color;
    float line_width;
    float point_size;
    bool use_texture;
    bool draw_lines = false;
    bool draw_point = false;


    std::shared_ptr<TextureGL> texture;
    std::vector<std::array<float, 2>> tex_coords;
    std::vector<std::array<short, 4>> faces;

    std::vector<std::array<float, 3>> _vertices;
    std::vector<std::array<float, 3>> rot_vertices;
    std::vector<std::array<short, 2>> edges;
    std::vector<std::array<int, 2>> projected_vertices;
};

PYBIND11_MODULE(CalculateGL, m) {
    m.doc() = "OpenGL рендеринг на C++ с поддержкой OBJ файлов";

    py::class_<TextureGL, std::shared_ptr<TextureGL>>(m, "TextureGL")
        .def(py::init<>())
        .def("load_from_data", &TextureGL::load_from_data)
        .def("create_color_texture", &TextureGL::create_color_texture)
        .def("create_checker_texture", &TextureGL::create_checker_texture)
        .def("get_width", &TextureGL::get_width)
        .def("get_height", &TextureGL::get_height);

    py::class_<_FigurGL>(m, "_FigurGL")
        .def(py::init<short, short, const std::array<float, 3>&>(),
             py::arg("width_"), py::arg("height_"), 
             py::arg("position_") = std::array<float, 3>{0.0f, 0.0f, 0.0f})
        .def("load_obj", &_FigurGL::load_obj)  // Новый метод для загрузки OBJ
        .def("set_vertices", &_FigurGL::set_vertices)
        .def("set_edges", &_FigurGL::set_edges)
        .def("set_faces", &_FigurGL::set_faces)
        .def("set_texture_coords", &_FigurGL::set_texture_coords)
        .def("set_texture", &_FigurGL::set_texture)
        .def("enable_texture", &_FigurGL::enable_texture)
        .def("update", &_FigurGL::update)
        .def("turn_x", &_FigurGL::turn_x)
        .def("turn_y", &_FigurGL::turn_y)
        .def("turn_z", &_FigurGL::turn_z)
        .def("render_3d_scene", &_FigurGL::render_3d_scene)
        .def("get_projected_vertices", &_FigurGL::get_projected_vertices)
        .def("get_edges", &_FigurGL::get_edges)
        .def("set_line_color", &_FigurGL::set_line_color)
        .def("set_point_color", &_FigurGL::set_point_color)
        .def("set_line_width", &_FigurGL::set_line_width)
        .def("set_point_size", &_FigurGL::set_point_size)
        .def("enable_point", &_FigurGL::enable_point)
        .def("enable_lines", &_FigurGL::enable_lines); 
}