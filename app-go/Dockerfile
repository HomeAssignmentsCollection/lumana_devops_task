# syntax=docker/dockerfile:1

# Многоэтапная сборка для оптимизированного продакшн образа
# Этап 1: Этап сборки
FROM golang:1.21-alpine AS build

# Установить рабочую директорию
WORKDIR /app

# Установить зависимости для сборки
RUN apk add --no-cache git ca-certificates tzdata

# Скопировать файлы go mod сначала для лучшего кэширования слоев
COPY go.mod go.sum ./

# Скачать зависимости (кэшированный слой)
RUN go mod download

# Скопировать исходный код
COPY . .

# Собрать приложение с оптимизациями
# - CGO_ENABLED=0: Статическая линковка для меньшего образа
# - GOOS=linux: Целевая платформа Linux
# - -ldflags: Убрать отладочную информацию и оптимизировать размер бинарного файла
RUN CGO_ENABLED=0 GOOS=linux go build \
    -ldflags="-w -s" \
    -a -installsuffix cgo \
    -o read_products read_products.go

# Этап 2: Продакшн этап
# Использовать минимальный alpine образ для безопасности и размера
FROM alpine:latest

# Установить зависимости для выполнения
RUN apk --no-cache add ca-certificates tzdata

# Создать не-root пользователя для безопасности
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup

# Установить рабочую директорию
WORKDIR /app

# Скопировать бинарный файл из этапа сборки
COPY --from=build /app/read_products .

# Изменить владельца на не-root пользователя
RUN chown -R appuser:appgroup /app

# Переключиться на не-root пользователя
USER appuser

# Открыть порт (если нужен для проверок здоровья)
EXPOSE 8080

# Проверка здоровья для обеспечения работы приложения
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD ps aux | grep read_products || exit 1

# Установить переменные окружения
ENV GIN_MODE=release

# Запустить приложение
CMD ["./read_products"]
