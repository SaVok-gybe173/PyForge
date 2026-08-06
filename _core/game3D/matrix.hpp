#include <vector>
#include <stdexcept>
#include <cmath>
#include <iostream>
#include <random>
#include <algorithm>
#include <string>

class Matrix {
    private:
    std::vector<float> data;
    size_t rows;
    size_t cols;
    public:
    void fillRandom(float scale = 1.0f) {
        static std::random_device rd;
        static std::mt19937 gen(rd());
        std::uniform_real_distribution<float> dist(-scale, scale);
        for(float& val : data) {
            val = dist(gen);
        }
    }
    void fillZeros() {
        std::fill(data.begin(), data.end(), 0.0f);
    }
    void fillOnes() {
        std::fill(data.begin(), data.end(), 1.0f);
    }
    //Конструкторы
    Matrix() : rows(0), cols(0) {}
    Matrix(size_t r, size_t c, bool initRandom = true) : rows(r), cols(c), data(r * c) {
        if(initRandom) {
            fillRandom(1.0f);
        } else {
            fillZeros();
        }
    }
    Matrix(size_t r, size_t c, float v) : rows(r), cols(c), data(r * c, v) {}
    Matrix(const Matrix& other) : rows(other.rows), cols(other.cols), data(other.data) {}
    Matrix(Matrix&& other) noexcept : data(std::move(other.data)), rows(other.rows), cols(other.cols) { other.rows = 0; other.cols = 0; }
    //Функция перемещения
    friend void swap(Matrix& a, Matrix& b) {
        std::swap(a.data, b.data);
        std::swap(a.rows, b.rows);
        std::swap(a.cols, b.cols);
    }
    //Присваивание (Copy-and-Swap)
    Matrix& operator=(Matrix other) noexcept {
        swap(*this, other);
        return *this;
    }
    float& operator()(size_t i, size_t j) {
        if(i >= rows || j >= cols) {
            throw std::out_of_range("Matrix index out of range");
        }
        return data[i * cols + j];
    }
    const float& operator()(size_t i, size_t j) const {
        if(i >= rows || j >= cols) {
            throw std::out_of_range("Matrix index out of range");
        }
        return data[i * cols + j];
    }
    float& at(size_t i, size_t j) {
        return (*this)(i, j);
    }
    const float& at(size_t i, size_t j) const {
        return (*this)(i, j);
    }
    //Умножение мартиц
    Matrix operator*(const Matrix& other) const {
        if(cols != other.rows) {
            throw std::invalid_argument("Matrix dimensions mismatch: " + std::to_string(rows) + "x" + std::to_string(cols) + " * " + std::to_string(other.rows) + "x" + std::to_string(other.cols));
        }
        Matrix result(rows, other.cols, false);
        const float* a = data.data();
        const float* b = other.data.data();
        float* c = result.data.data();
        size_t colsA = cols;
        size_t colsB = other.cols;
        for(size_t i = 0; i < rows; i++) {
            for(size_t k = 0; k < colsA; k++) {
                float aVal = a[i * colsA + k];
                for(size_t j = 0; j < colsB; j++) {
                    c[i * colsB + j] += aVal * b[k * colsB + j];
                }
            }
        }
        return result;
    }
    //Поэлементное умножение матриц (Hadamard product) для LSTM
    Matrix hadamard(const Matrix& other) const {
        if(rows != other.rows || cols != other.cols) {
            throw std::invalid_argument("Matrix dimensions must match for hadamard product");
        }
        Matrix result(rows, cols, false);
        for(size_t i = 0; i < data.size(); i++) {
            result.data[i] = data[i] * other.data[i];
        }
        return result;
    }
    //Транспонирование
    Matrix transpose() const {
        Matrix result(cols, rows, false);
        for(size_t i = 0; i < rows; i++) {
            for(size_t j = 0; j < cols; j++) {
                result(j, i) = (*this)(i, j);
            }
        }
        return result;
    }
    //Сигмоида: 1 / (1 + exp(-x))
    void applySigmoid() {
        for(float& val : data) {
            val = 1.0f / (1.0f + std::exp(-val));
        }
    }
    //Tanh: (exp(x) - exp(-x)) / (exp(x) + exp(-x))
    void applyTanh() {
        for(float& val : data) {
            val = std::tanh(val);
        }
    }
    //ReLU: max(0, x)
    void applyReLU() {
        for(float& val : data) {
            if(val < 0.0f) val = 0.0f;
        }
    }
    //Softmax: только для векторов (rows == 1)
    void applySoftmax() {
        if(rows != 1 || cols == 0) {
            throw std::runtime_error("Softmax only for row vectors (rows == 1) and cols > 0");
        }
        float maxVal = data[0];
        float minVal = data[0];
        for(size_t i = 1; i < cols; i++) {
            if(data[i] > maxVal) maxVal = data[i];
            if(data[i] < minVal) minVal = data[i];
        }
        const float SAFE_RANGE = 50.0f;
        if(maxVal - minVal > SAFE_RANGE) {
            float shift = (maxVal + minVal) / 2.0f;
            for(size_t i = 0; i < cols; i++) {
                data[i] = std::clamp(data[i], shift - SAFE_RANGE/2, shift + SAFE_RANGE/2);
            }
            maxVal = data[0];
            for(size_t i = 1; i < cols; i++) {
                if(data[i] > maxVal) maxVal = data[i];
            }
        }
        float sum = 0.0f;
        for(size_t i = 0; i < cols; i++) {
            data[i] = std::exp(data[i] - maxVal);
            sum += data[i];
        }
        for(size_t i = 0; i < cols; i++) {
            data[i] /= sum;
        }
    }
    //Сложение с другой матрицей (поэлементно)
    Matrix& operator+=(const Matrix& other) {
        if(rows != other.rows || cols != other.cols) {
            throw std::invalid_argument("Dimensions must match for +=");
        }
        for(size_t i = 0; i < data.size(); i++) {
            data[i] += other.data[i];
        }
        return *this;
    }
    Matrix operator+(const Matrix& other) const {
        if(rows != other.rows || cols != other.cols) {
            throw std::invalid_argument("Matrix dimensions must match for addition");
        }
        Matrix result = *this;
        result += other;
        return result;
    }
    //Вычитание матриц
    Matrix operator-(const Matrix& other) const {
        if(rows != other.rows || cols != other.cols) {
            throw std::invalid_argument("Dimensions must match for subtraction");
        }
        Matrix result(rows, cols, false);
        for(size_t i = 0; i < data.size(); i++) {
            result.data[i] = data[i] - other.data[i];
        }
        return result;
    }
    Matrix& operator-=(const Matrix& other) {
        if(rows != other.rows || cols != other.cols) {
            throw std::invalid_argument("Dimensions must match for -=");
        }
        for(size_t i = 0; i < data.size(); i++) {
            data[i] -= other.data[i];
        }
        return *this;
    }
    //Унарный минус
    Matrix operator-() const {
        Matrix result(rows, cols, false);
        for(size_t i = 0; i < data.size(); i++) {
            result.data[i] = -data[i];
        }
        return result;
    }
    //Умножение на скаляр
    Matrix operator*(float scalar) const {
        Matrix result(rows, cols, false);
        for(size_t i = 0; i < data.size(); i++) {
            result.data[i] = data[i] * scalar;
        }
        return result;
    }
    friend Matrix operator*(float scalar, const Matrix& m) {
        return m * scalar;
    }
    //Сумма всех элеементов
    float sum() const noexcept {
        float s = 0.0f;
        for(float v : data) s += v;
        return s;
    }
    //Клиппинг крадиентов
    void clip(float minVal, float maxVal) {
        for(float& val : data) {
            if(val < minVal) val = minVal;
            if(val > maxVal) val = maxVal;
        }
    }
    //Геттеры
    size_t getRows() const noexcept { return rows; }
    size_t getCols() const noexcept { return cols; }
    size_t size() const noexcept { return data.size(); }
    const float* getData() const noexcept { return data.data(); }
    float* getData() noexcept { return data.data(); }
    //Вывод
    void print() const {
        for(size_t i = 0; i < rows; i++) {
            for(size_t j = 0; j < cols; j++) {
                std::cout << (*this)(i, j) << " ";
            }
            std::cout << "\n";
        }
    }
};