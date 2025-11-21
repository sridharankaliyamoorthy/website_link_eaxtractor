# Contributing to Link Extractor

First off, thank you for considering contributing to Link Extractor! It's people like you that make this project better.

## Code of Conduct

This project adheres to a code of conduct that all contributors are expected to follow. Please be respectful and constructive in all interactions.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed after following the steps**
- **Explain which behavior you expected to see instead and why**
- **Include screenshots if applicable**
- **Specify the name and version of the OS you're using**
- **Specify the Python version you're using**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Describe the current behavior and explain which behavior you expected to see instead**
- **Explain why this enhancement would be useful**

### Pull Requests

- Fill in the required template
- Do not include issue numbers in the PR title
- Include screenshots and animated GIFs in your pull request whenever possible
- Follow the Python style guide (PEP 8)
- Include thoughtfully-worded, well-structured tests
- Document new code based on the Documentation Styleguide
- End all files with a newline

## Development Setup

1. **Fork the repository**

2. **Clone your fork**
   ```bash
   git clone https://github.com/your-username/website_link_eaxtractor.git
   cd website_link_eaxtractor
   ```

3. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If available
   ```

5. **Create a branch for your changes**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and small
- Use type hints where appropriate

### Code Formatting

- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Use black or autopep8 for formatting (if configured)

### Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

Example:
```
Add browser automation timeout handling

- Increase default timeout to 60 seconds
- Add progressive waiting for content stabilization
- Handle partial page loads gracefully

Fixes #123
```

## Testing

Before submitting your pull request, please make sure:

1. **All tests pass**
   ```bash
   python -m pytest test/
   ```

2. **Code is properly formatted**
   ```bash
   black src/  # If using black
   ```

3. **No linting errors**
   ```bash
   flake8 src/  # If using flake8
   ```

## Documentation

- Update the README.md if you add new features or change existing ones
- Add docstrings to new functions and classes
- Update API documentation if you modify the API
- Include examples in your documentation

## Submitting Changes

1. **Push your changes to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill out the PR template
   - Submit the PR

3. **Respond to feedback**
   - Be open to feedback and suggestions
   - Make requested changes promptly
   - Keep the discussion focused and constructive

## Project Structure

```
website_link_eaxtractor/
├── src/              # Source code
├── test/             # Tests
├── docs/             # Documentation
└── .github/          # GitHub templates and workflows
```

## Areas for Contribution

- **Bug fixes**: Fix any issues you find
- **New features**: Add functionality that would be useful
- **Documentation**: Improve or add documentation
- **Tests**: Add test coverage
- **Performance**: Optimize code for better performance
- **UI/UX**: Improve the user interface and experience
- **Accessibility**: Make the tool more accessible

## Questions?

If you have any questions, feel free to:
- Open an issue with the "question" label
- Contact the maintainer

Thank you for contributing! 🎉

