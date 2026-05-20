# Contributing to FlowPredict AI

Thank you for your interest in contributing to FlowPredict AI! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and constructive in all interactions.

## Getting Started

### 1. Fork and Clone
```bash
git clone https://github.com/FlowPredict-AI/FlowPredict.git
cd FlowPredict
```

### 2. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 3. Make Your Changes

## Development Standards

### Python (Backend)
- **Code Style**: Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- **Formatter**: Black (`black app/ tests/`)
- **Linter**: Pylint and Flake8
- **Type Hints**: Use Python type annotations
- **Testing**: Minimum 80% code coverage

```bash
# Format code
black app/ tests/

# Run linters
pylint app/
flake8 app/

# Run tests
pytest --cov=app tests/
```

### TypeScript/React (Frontend)
- **Code Style**: Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- **Formatter**: Prettier (`npx prettier --write src/`)
- **Linter**: ESLint
- **Type Checking**: TypeScript strict mode
- **Testing**: React Testing Library

```bash
# Format code
npm run format

# Run linter
npm run lint

# Run tests
npm test
```

## Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Test additions/changes
- `chore`: Build, dependencies, CI/CD

### Examples
```
feat(backend): add confidence intervals to predictions
fix(frontend): resolve form validation error on submit
docs(readme): update setup instructions
test(api): add prediction endpoint tests
```

## Pull Request Process

1. **Ensure all tests pass**
   ```bash
   # Backend
   cd backend && pytest --cov=app tests/
   
   # Frontend
   cd frontend && npm test
   ```

2. **Update documentation** if applicable
   - README.md
   - API documentation
   - Inline code comments

3. **Create a descriptive PR**
   - Use the PR template
   - Link related issues
   - Describe changes clearly
   - Include screenshots for UI changes

4. **Address code review feedback**
   - Be responsive to reviewer comments
   - Make changes in additional commits
   - Re-request review when ready

5. **Merge requirements**
   - ✅ All checks pass
   - ✅ Code review approval
   - ✅ No merge conflicts

## Testing Guidelines

### Backend Tests

```python
# tests/test_predictions.py
import pytest
from app.models.ml_model import MLModel
from app.models.schemas import PredictionRequest

@pytest.fixture
def ml_model():
    return MLModel()

def test_prediction_valid_input(ml_model):
    request = PredictionRequest(
        porosity=0.25,
        permeability=100.0,
        pressure=3000.0,
        depth=10000.0,
        temperature=200.0
    )
    result = ml_model.predict(request)
    assert result.production_rate > 0
    assert result.confidence_lower < result.production_rate
    assert result.production_rate < result.confidence_upper
```

### Frontend Tests

```typescript
// src/components/__tests__/PredictionForm.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import PredictionForm from '../PredictionForm';

test('renders form with all fields', () => {
  render(<PredictionForm />);
  expect(screen.getByLabelText(/porosity/i)).toBeInTheDocument();
  expect(screen.getByRole('button', { name: /predict/i })).toBeInTheDocument();
});
```

## Documentation

- Use clear, concise language
- Include code examples where appropriate
- Keep README.md updated
- Document breaking changes
- Update CHANGELOG.md

## Reporting Issues

When reporting bugs, include:
- Description of the issue
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python/Node version, etc.)
- Screenshots/logs if applicable

## Performance Considerations

- Optimize ML model predictions
- Cache expensive computations
- Minimize API response times
- Profile frontend rendering

## Security

- Never commit sensitive data (API keys, credentials)
- Use environment variables for configuration
- Validate all user inputs
- Follow OWASP security guidelines

## Questions?

Feel free to:
- Open a discussion issue
- Check existing documentation
- Review past pull requests for examples

Happy coding! 🚀