#include <iostream>
#include <string>
#include <vector>
#include <array>
#include <cmath>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

using namespace std;
namespace py = pybind11;

double degrees_to_radians(float deg) {
    return deg * acos(-1) / 180.0;
}

class _Figur {
public:
    _Figur(short width_, short height_, const std::array<float, 3>& position_ = { 0.0f, 0.0f, 0.0f }) :
        width(width_), height(height_), position(position_)
    {}

    int fov = 5;
    short height, width;
    std::array<float, 3> position = { 0.0f, 0.0f, 0.0f };

    std::vector<std::array<float, 3>> _vertices;
    std::vector<std::array<float, 3>> rot_vertices;

    std::vector<std::array<short, 2>> edges;
    std::vector<std::array<int, 2>> projected_vertices;

    void set_height_width(short width_, short height_){
        short height = height_;
        short width = width_;
    }

    void set_fov(int _fov = 5){
        int fov = _fov;
    }

    void set_position(std::array<float,3> positions = {0.0f, 0.0f, 0.0f}){
        for (size_t i = 0; i < rot_vertices.size(); ++i) {
            rot_vertices[i][0] = rot_vertices[i][0] +  positions[0];
            rot_vertices[i][1] = rot_vertices[i][1] +  positions[1];
            rot_vertices[i][2] = rot_vertices[i][2] +  positions[2];
        }
    }
    void update(float distans = 0.0f, std::array<float,3> positions = {0.0f, 0.0f, 0.0f}) {
    //void update(float distans = 0.0f, std::array<float, 3>& positions = { 0.0f, 0.0f, 0.0f }) {
        projected_vertices.clear();

        for (size_t i = 0; i < rot_vertices.size(); ++i) {
            float x = (float)(rot_vertices[i][0] + positions[0]);
            float y = (float)(rot_vertices[i][1] + positions[1]);
            float z = (float)(rot_vertices[i][2] + positions[2]);

            z -= distans;

            float z_factor = fov / (fov + z);
            float x_proj = x * -z_factor;
            float y_proj = y * z_factor;

            std::array<int, 2> projected_vertex;
            if (z + fov < 0) {
                projected_vertex[0] = (int)((x_proj + 1) * width / 2);
                projected_vertex[1] = (int)((1 - y_proj) * height / 2);
            }
            else {
                projected_vertex[0] = 0;
                projected_vertex[1] = 0;
            }
            projected_vertices.push_back(projected_vertex);
        }
    }

    void _draw(const int* start, const int* end) {
        // TODO: Реализовать отрисовку в Python
    }

    void set_vertices(const py::array_t<float>& vertices) {
        py::buffer_info buf = vertices.request();
        if (buf.ndim != 2 || buf.shape[1] != 3) {
            throw std::runtime_error("Vertices array must be 2D with shape (N, 3)");
        }

        _vertices.resize(buf.shape[0]);
        rot_vertices.resize(buf.shape[0]);
        float* ptr = (float*)buf.ptr;

        for (size_t i = 0; i < buf.shape[0]; ++i) {
            for (int j = 0; j < 3; ++j) {
                _vertices[i][j] = ptr[i * 3 + j];
                rot_vertices[i][j] = ptr[i * 3 + j];
            }
        }
    }
    const std::vector<std::array<int, 2>>& get_projected_vertices() const { return projected_vertices; }


    void set_edges(const std::vector<std::array<short, 2>>& new_edges) {
        edges = new_edges;
    }

    void draw() {
        for (const auto& edge : edges) {
            if (edge[0] >= 0 && edge[0] < projected_vertices.size() &&
                edge[1] >= 0 && edge[1] < projected_vertices.size()) {
                std::array<int, 2> start = projected_vertices[edge[0]];
                std::array<int, 2> end = projected_vertices[edge[1]];
                _draw(start.data(), end.data());
            }
        }
    }

    void turn_y(float rads) {
        float angle = (float)(degrees_to_radians(rads));
        for (size_t i = 0; i < rot_vertices.size(); ++i) {
            float x = rot_vertices[i][0];
            float y = rot_vertices[i][1];
            float z = rot_vertices[i][2];
            rot_vertices[i][1] = y * cos(angle) - z * sin(angle);
            rot_vertices[i][2] = y * sin(angle) + z * cos(angle);
        }
    }

    void turn_x(float rads) {
        float angle = (float)(degrees_to_radians(rads));
        for (size_t i = 0; i < rot_vertices.size(); ++i) {
            float x = rot_vertices[i][0];
            float y = rot_vertices[i][1];
            float z = rot_vertices[i][2];
            rot_vertices[i][0] = x * cos(angle) + z * sin(angle);
            rot_vertices[i][2] = -x * sin(angle) + z * cos(angle);
        }
    }
void turn_z(float rads) {
        float angle = (float)(degrees_to_radians(rads));
        for (size_t i = 0; i < rot_vertices.size(); ++i) {
            float x = rot_vertices[i][0];
            float y = rot_vertices[i][1];
            float z = rot_vertices[i][2];
            rot_vertices[i][0] = x * cos(angle) - y * sin(angle);
            rot_vertices[i][1] = x * sin(angle) + y * cos(angle);
        }
    }

    std::vector<std::array<short, 2>> get_edges() const {
        return edges;
    }
};

PYBIND11_MODULE(Calculate, m) {
    m.doc() = "вычисления для скорости на с++";

    py::class_<_Figur>(m, "_Figur")
        .def(py::init<short, short, const std::array<float, 3>&>())
        .def("class_draw", &_Figur::_draw)
        .def("draw", &_Figur::draw)
        .def("update", &_Figur::update)
        .def("set_vertices", &_Figur::set_vertices)
        .def("set_edges", &_Figur::set_edges)
        .def("get_edges", &_Figur::get_edges)
        .def("turn_y", &_Figur::turn_y)
        .def("turn_x", &_Figur::turn_x)
        .def("turn_z", &_Figur::turn_z)
        .def("set_position", &_Figur::set_position)
        .def("set_height_width", &_Figur::set_height_width) 
        .def("set_fov", &_Figur::set_fov) 
        .def("get_projected_vertices", &_Figur::get_projected_vertices);
}