# GitHub Actions Workflows

Этот проект включает комплексные GitHub Actions workflows для автоматизации CI/CD процессов.

## 📋 Доступные Workflows

### 1. **CI/CD Pipeline** (`ci.yml`)
Основной pipeline для тестирования и развертывания.

**Триггеры:**
- Push в ветки: `main`, `dev`, `feature/*`, `bugfix/*`
- Pull Requests в `main` и `dev`
- Manual trigger с выбором окружения

**Jobs:**
- `test-go`: Тестирование Go приложения
- `test-node`: Тестирование Node.js приложения  
- `test-python`: Тестирование Python скриптов
- `build-docker`: Сборка Docker образов
- `security-scan`: Сканирование безопасности
- `code-quality`: Проверки качества кода
- `deploy`: Развертывание (только для main/dev)

### 2. **Docker Build** (`build.yml`)
Специализированный workflow для сборки и публикации Docker образов.

**Триггеры:**
- Push в `main` и `dev`
- Pull Requests в `main` и `dev`
- Manual trigger

**Jobs:**
- `build-go`: Сборка Go образа
- `build-node`: Сборка Node.js образа
- `test-docker-compose`: Тестирование Docker Compose

### 3. **Security Scan** (`security.yml`)
Комплексное сканирование безопасности.

**Триггеры:**
- Push в `main`, `dev`, `feature/*`
- Pull Requests в `main` и `dev`
- Еженедельное расписание (понедельник 2:00 UTC)
- Manual trigger

**Jobs:**
- `code-security`: Сканирование кода (Bandit, Gosec, ESLint)
- `container-security`: Сканирование Docker образов (Trivy)
- `dependency-check`: Проверка зависимостей
- `security-config`: Проверка конфигурации безопасности

### 4. **Pre-commit Checks** (`pre-commit.yml`)
Автоматические проверки качества кода.

**Триггеры:**
- Push в `main`, `dev`, `feature/*`, `bugfix/*`
- Pull Requests в `main` и `dev`
- Manual trigger

**Jobs:**
- `pre-commit`: Запуск pre-commit хуков
- `code-quality`: Дополнительные проверки качества

## 🔧 Конфигурация

### Environment Variables
```yaml
GO_VERSION: '1.21'
NODE_VERSION: '18'
PYTHON_VERSION: '3.9'
REGISTRY: ghcr.io
IMAGE_NAME: ${{ github.repository }}
```

### Secrets
Для полной функциональности требуются следующие secrets:
- `GITHUB_TOKEN` (автоматически доступен)
- `AWS_ACCESS_KEY_ID` (для AWS интеграции)
- `AWS_SECRET_ACCESS_KEY` (для AWS интеграции)

## 🚀 Использование

### Manual Trigger
```bash
# Запуск CI/CD pipeline
gh workflow run ci.yml

# Запуск с параметрами
gh workflow run ci.yml -f environment=production -f force_deploy=false

# Запуск security scan
gh workflow run security.yml

# Запуск Docker build
gh workflow run build.yml
```

### Branch Protection
Рекомендуется настроить branch protection rules:
- Require status checks to pass before merging
- Require branches to be up to date before merging
- Require pull request reviews before merging

## 📊 Мониторинг

### Artifacts
Workflows создают следующие артефакты:
- `go-binary`: Скомпилированный Go бинарный файл
- `security-reports`: Отчеты безопасности
- `quality-reports`: Отчеты качества кода
- `dependency-reports`: Отчеты зависимостей

### Notifications
- Уведомления о статусе в Slack/Discord
- Email уведомления для критических ошибок
- GitHub notifications для всех участников

## 🔒 Безопасность

### Security Features
- Автоматическое сканирование уязвимостей
- Проверка зависимостей на известные CVE
- Сканирование Docker образов
- Обнаружение hardcoded secrets
- Проверка конфигурации безопасности

### Compliance
- Соответствие security policy
- Автоматические проверки compliance
- Отчеты для аудита

## 🛠️ Troubleshooting

### Common Issues

1. **Tests failing**
   ```bash
   # Локальная проверка
   cd app-go && go test ./...
   cd app-node && npm test
   ```

2. **Docker build failing**
   ```bash
   # Локальная сборка
   docker build -t app-go ./app-go
   docker build -t app-node ./app-node
   ```

3. **Security scan issues**
   ```bash
   # Локальное сканирование
   bandit -r scripts/
   gosec ./app-go/...
   ```

### Debug Workflows
```bash
# Включить debug logging
echo "::debug::Debug message" >> $GITHUB_OUTPUT

# Проверить workflow runs
gh run list --workflow=ci.yml
```

## 📈 Метрики

### Performance
- Среднее время выполнения: ~15 минут
- Кэширование зависимостей для ускорения
- Параллельное выполнение jobs

### Coverage
- Go: Unit tests + Integration tests
- Node.js: Unit tests + API tests
- Python: Syntax + Security checks
- Docker: Build + Security scan

## 🔄 Обновления

### Version Updates
- Автоматические проверки обновлений зависимостей
- Dependabot для автоматических PR
- Manual review для критических обновлений

### Workflow Updates
- Регулярные обновления actions
- Тестирование новых features
- Backward compatibility проверки 