# Python Forge (графический движок)

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12%20%7C%203.13%20%7C%203.14%20%7C%203.15-blue?style=flat&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Linux%20x86-supported-success?style=flat&colorA=2d2d2d&colorB=4a4a4a" alt="Linux x86" />
  <img src="https://img.shields.io/badge/Linux%20x86__64-supported-success?style=flat&colorA=2d2d2d&colorB=4a4a4a" alt=" Linux x86_64" />
  <img src="https://img.shields.io/badge/Windows%20x86-supported-success?style=flat&colorA=2d2d2d&colorB=4a4a4a" alt="Windows x86" />
  <img src="https://img.shields.io/badge/Windows%20x86__64-supported-success?style=flat&colorA=2d2d2d&colorB=4a4a4a" alt="Windows x86_64" />
  <img src="https://img.shields.io/badge/macOS%20x86__64-supported-success?style=flat&colorA=2d2d2d&colorB=4a4a4a" alt="macOS x86_64" />
  <img src="https://img.shields.io/badge/macOS%20arm64-supported-success?style=flat&colorA=2d2d2d&colorB=4a4a4a" alt="macOS arm64" />
  <img src="https://img.shields.io/badge/Android%20ARM32-supported-success?style=flat&colorA=2d2d2d&colorB=4a4a4a" alt="Android ARM32" />
  <img src="https://img.shields.io/badge/Android%20ARM64-supported-success?style=flat&colorA=2d2d2d&colorB=4a4a4a" alt="Android ARM64" />
  <img src="https://img.shields.io/badge/iOS%20ARM64-supported-success?style=flat&colorA=2d2d2d&colorB=4a4a4a" alt="iOS ARM64" />
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/SaVok-gybe173/PyForge?style=flat&logo=github&color=005571" alt="GitHub Stars" />
  <img src="https://img.shields.io/github/license/SaVok-gybe173/PyForge" alt="License MIT" />
  <img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/SaVok-gybe173/PyForge">
</p>


```Графический движок``` (иногда его называют "рендер" или "визуализатор") - это программный инструмент, главная задача которого - ```рендеринг```, то есть преобразование данных (моделей, текстур, освещения) в видимое на экране изображение. Он может существовать как самостоятельный продукт или быть частью более крупного инструмента, например, игрового движка. 

PyForge - это кроссплатформенный графический фреймворк на python и cython, он создан для высокоуровневого и низкоуровневого разработки приложений/игр. Поддерживающего OpenGl и Vulkan на sdl2.

## Поддерживаемые архитектуры (на которых проводились тесты)
| архитектура               | есть ли поддержка  | версии python                                                                |
| --------------------------| ------------------ | --------------------------------------------------------------------------- |
| Linux x86                 | ✅                | python3.12, python3.13, python3.14, остальное собирать самому
| Linux x86_64              | ✅                | python3.12, python3.13, python3.14, остальное собирать самому
| Windows x86               | ✅                | python3.12, python3.13, python3.14, остальное собирать самому
| Windows x86_64            | ✅                | python3.12, python3.13, python3.14, остальное собирать самому
| macOS x86_64              | ✅                | python3.12, python3.13, python3.14, остальное собирать самому
| macOS arm64               | ✅                | сборка модулей самому
| Android ARM32             | ✅                | сборка модулей самому
| Android ARM64             | ✅                | python3.13, остальное собирать самому
| iOS ARM64                 | ✅                | сборка модулей самому