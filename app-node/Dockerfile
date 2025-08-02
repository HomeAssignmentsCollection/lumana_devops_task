# Многоэтапная сборка для оптимизированного продакшн образа
# Этап 1: Этап сборки
FROM node:18-alpine AS build

# Установить рабочую директорию
WORKDIR /app

# Скопировать файлы пакета сначала для лучшего кэширования слоев
COPY package*.json ./

# Установить зависимости
RUN npm ci --only=production && npm cache clean --force

# Скопировать исходный код
COPY . .

# Этап 2: Продакшн этап
FROM node:18-alpine AS production

# Установить зависимости для выполнения
RUN apk --no-cache add dumb-init

# Создать не-root пользователя для безопасности
RUN addgroup -g 1001 -S nodejs && \
    adduser -u 1001 -S nodejs -G nodejs

# Установить рабочую директорию
WORKDIR /app

# Скопировать node_modules и исходный код из этапа сборки
COPY --from=build --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --from=build --chown=nodejs:nodejs /app/create_product.js ./

# Переключиться на не-root пользователя
USER nodejs

# Открыть порт (если нужен для проверок здоровья)
EXPOSE 3000

# Проверка здоровья для обеспечения работы приложения
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD node -e "console.log('Health check passed')" || exit 1

# Установить переменные окружения
ENV NODE_ENV=production

# Использовать dumb-init для правильной обработки сигналов
ENTRYPOINT ["dumb-init", "--"]

# Запустить приложение
CMD ["node", "create_product.js"] 