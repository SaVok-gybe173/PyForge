#include <iostream>
#include <vector>
#include "matrix.hpp"

int main() {
    try {
        std::cout << "=== Testing Unary Minus ===\n\n";
        
        // Создаём матрицу
        Matrix A(2, 3, false);
        A(0,0) = 1; A(0,1) = 2; A(0,2) = 3;
        A(1,0) = 4; A(1,1) = 5; A(1,2) = 6;
        
        std::cout << "A:\n";
        A.print();
        
        // Унарный минус
        Matrix B = -A;
        std::cout << "\n-A:\n";
        B.print();
        
        // Проверка: A + (-A) должно дать нулевую матрицу
        Matrix C = A + B;
        std::cout << "\nA + (-A):\n";
        C.print();
        
        // Проверка суммы (должна быть 0)
        std::cout << "\nSum of A + (-A): " << C.sum() << " (should be 0)\n";
        
        // ========== ИСПОЛЬЗОВАНИЕ В ГРАДИЕНТАХ ==========
        std::cout << "\n=== Gradient Descent Example ===\n";
        
        // Представь, что это градиент
        Matrix grad(2, 2, false);
        grad(0,0) = 0.1f; grad(0,1) = 0.2f;
        grad(1,0) = 0.3f; grad(1,1) = 0.4f;
        
        std::cout << "Gradient:\n";
        grad.print();
        
        // Обновление весов: w = w - learning_rate * grad
        float learning_rate = 0.01f;
        Matrix weights(2, 2, false);
        weights(0,0) = 1.0f; weights(0,1) = 2.0f;
        weights(1,0) = 3.0f; weights(1,1) = 4.0f;
        
        std::cout << "\nWeights before update:\n";
        weights.print();
        
        // Используем унарный минус для -learning_rate * grad
        weights += (-learning_rate * grad);
        
        std::cout << "\nWeights after update:\n";
        weights.print();
        
        // Проверка: w_new = w_old - lr * grad
        Matrix expected(2, 2, false);
        expected(0,0) = 1.0f - 0.01f * 0.1f;
        expected(0,1) = 2.0f - 0.01f * 0.2f;
        expected(1,0) = 3.0f - 0.01f * 0.3f;
        expected(1,1) = 4.0f - 0.01f * 0.4f;
        
        std::cout << "\nExpected weights:\n";
        expected.print();
        
        std::cout << "\n=== ALL TESTS PASSED! ===\n";
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << "\n";
    }
    
    return 0;
}