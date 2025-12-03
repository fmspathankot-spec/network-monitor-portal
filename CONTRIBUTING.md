# 🤝 Contributing to Network Monitor Portal

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Testing](#testing)

## 📜 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Respect differing viewpoints

## 🚀 Getting Started

### 1. Fork the Repository

Click the "Fork" button at the top right of the repository page.

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/network-monitor-portal.git
cd network-monitor-portal
```

### 3. Add Upstream Remote

```bash
git remote add upstream https://github.com/fmspathankot-spec/network-monitor-portal.git
```

### 4. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

## 💻 Development Workflow

### Backend Development

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt

# Make your changes
# Test your changes
python -m pytest tests/

# Run linter
flake8 .
black .
```

### Frontend Development

```bash
cd frontend
npm install

# Make your changes
# Test your changes
npm test

# Run linter
npm run lint
```

## 📝 Coding Standards

### Python (Backend)

- Follow [PEP 8](https://pep8.org/)
- Use type hints
- Write docstrings for all functions
- Maximum line length: 100 characters

**Example:**
```python
def get_router_status(router_id: int, db: Session) -> RouterStatus:
    """
    Get current status of a router.
    
    Args:
        router_id: ID of the router
        db: Database session
        
    Returns:
        RouterStatus object with current status
        
    Raises:
        HTTPException: If router not found
    """
    router = db.query(Router).filter(Router.id == router_id).first()
    if not router:
        raise HTTPException(status_code=404, detail="Router not found")
    return router
```

### TypeScript (Frontend)

- Use TypeScript for all new code
- Follow [Airbnb Style Guide](https://github.com/airbnb/javascript)
- Use functional components with hooks
- Maximum line length: 100 characters

**Example:**
```typescript
interface RouterFormProps {
  onSubmit: (data: RouterData) => void;
  isLoading?: boolean;
}

export function RouterForm({ onSubmit, isLoading }: RouterFormProps) {
  // Component implementation
}
```

## 📦 Commit Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/).

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```bash
feat(auth): add JWT token refresh endpoint

Implement automatic token refresh to improve user experience.
Users will no longer need to re-login when token expires.

Closes #123
```

```bash
fix(ssh): handle connection timeout gracefully

Add proper error handling for SSH connection timeouts.
Display user-friendly error message instead of crashing.

Fixes #456
```

## 🔄 Pull Request Process

### 1. Update Your Branch

```bash
git fetch upstream
git rebase upstream/main
```

### 2. Push Your Changes

```bash
git push origin feature/your-feature-name
```

### 3. Create Pull Request

1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Select your branch
4. Fill in the PR template:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added new tests
- [ ] Manual testing completed

## Screenshots (if applicable)
Add screenshots here

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
```

### 4. Code Review

- Address review comments
- Push updates to your branch
- Request re-review when ready

### 5. Merge

Once approved, maintainers will merge your PR.

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v
pytest tests/ --cov=. --cov-report=html
```

### Frontend Tests

```bash
cd frontend
npm test
npm run test:coverage
```

### Integration Tests

```bash
# Start all services
docker-compose up -d

# Run integration tests
npm run test:integration
```

## 🐛 Reporting Bugs

### Before Submitting

1. Check existing issues
2. Try latest version
3. Collect debug information

### Bug Report Template

```markdown
**Describe the bug**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen

**Screenshots**
If applicable

**Environment:**
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.11]
- Node version: [e.g., 18.17]
- Browser: [e.g., Chrome 120]

**Additional context**
Any other relevant information
```

## 💡 Feature Requests

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
Clear description of the problem

**Describe the solution you'd like**
Clear description of desired solution

**Describe alternatives you've considered**
Alternative solutions or features

**Additional context**
Mockups, examples, etc.
```

## 📚 Documentation

- Update README.md for user-facing changes
- Update API documentation for endpoint changes
- Add inline comments for complex logic
- Update CHANGELOG.md

## 🎯 Areas for Contribution

### High Priority

- [ ] Multi-vendor support (Juniper, Arista)
- [ ] Email/SMS alert notifications
- [ ] Network topology visualization
- [ ] Configuration backup/restore

### Medium Priority

- [ ] Custom dashboard widgets
- [ ] API rate limiting
- [ ] Audit logging
- [ ] Performance optimizations

### Good First Issues

- [ ] Improve error messages
- [ ] Add more unit tests
- [ ] Fix typos in documentation
- [ ] Improve UI/UX

## 🏆 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Given credit in documentation

## 📞 Getting Help

- **Discord:** [Join our server](#)
- **Email:** fmspathankot@gmail.com
- **Issues:** [GitHub Issues](https://github.com/fmspathankot-spec/network-monitor-portal/issues)

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing! 🎉**
