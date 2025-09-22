# Publishing Guide

This document describes the automated publishing process for PyConsole using GitHub Actions, semantic-release, and PyPI Trusted Publishers.

## Overview

The publishing workflow automatically:
- Runs tests across multiple Python versions and platforms
- Determines the next version based on commit messages
- Creates Git tags and releases
- Publishes to PyPI using Trusted Publishers
- Builds portable executables
- Uploads artifacts to GitHub releases

## Setup Instructions

### 1. Configure PyPI Trusted Publishers

1. Go to your project on [PyPI](https://pypi.org/)
2. Navigate to **Publishing** in your project settings
3. Click **Add a pending publisher**
4. Fill in the details:
   - **Publisher name**: `github`
   - **Publisher ID**: Your GitHub repository URL (e.g., `https://github.com/username/pyconsole`)
   - **Owner**: Your GitHub username or organization
   - **Repository name**: `pyconsole`
   - **Environment**: `pypi`
   - **Workflow filename**: `publish.yml`

### 2. Configure GitHub Secrets

Add the following secrets to your GitHub repository:

```bash
# Required for Trusted Publishers (no API token needed)
# UV_PUBLISH_TOKEN is NOT required when using Trusted Publishers

# Optional for GitHub releases
GITHUB_TOKEN: automatically provided by GitHub Actions
```

### 3. Create GitHub Environment

1. Go to your repository **Settings** → **Environments**
2. Click **New environment**
3. Name it `pypi`
4. Configure protection rules as needed (recommended: require reviewers)

## Commit Convention

The workflow uses [semantic-release](https://python-semantic-release.readthedocs.io/) with conventional commits:

### Format
```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types
- `feat`: New feature (triggers minor version bump)
- `fix`: Bug fix (triggers patch version bump)
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Test changes
- `build`: Build system changes
- `ci`: CI configuration changes
- `chore`: Maintenance tasks

### Examples
```bash
feat: add new API endpoint for publishing
fix: resolve authentication issue with PyPI
docs: update installation instructions
build: upgrade to PyInstaller 6.0
```

## Workflow Triggers

### On Push to Main/Master
1. **Test Matrix**: Runs tests on all supported Python versions and platforms
2. **Semantic Release**:
   - Analyzes commit messages since last tag
   - Determines next version
   - Updates version in pyproject.toml
   - Creates Git tag and commit
   - Generates changelog
3. **Publish to PyPI**:
   - Builds package distributions
   - Publishes to PyPI using Trusted Publishers
   - Creates GitHub release with artifacts
4. **Build Executables**:
   - Creates portable executables for all platforms
   - Uploads as artifacts

### On Pull Request
- Runs full test suite
- Validates configuration
- Checks code quality

## Manual Publishing

If you need to publish manually:

### Using uv publish
```bash
# Set up your UV_PUBLISH_TOKEN
export UV_PUBLISH_TOKEN=your-token-here

# Test with dry run
python app.py --dry-run

# Publish for real
python app.py --publish
```

### Using GitHub CLI
```bash
# Create a release
gh release create v1.0.0 dist/* --title "Version 1.0.0" --notes "Release notes here"

# Or trigger the workflow manually
gh workflow run publish.yml
```

## Troubleshooting

### Common Issues

1. **Trusted Publisher not configured**
   - Ensure you've set up the publisher in PyPI project settings
   - Verify the workflow filename and repository details are correct

2. **Missing permissions**
   - Check that your workflow has `id-token: write` permissions
   - Ensure the `pypi` environment exists

3. **Version conflicts**
   - Check that semantic-release can access the full git history
   - Verify your commit messages follow the conventional format

4. **Build failures**
   - Ensure all dependencies are properly specified in pyproject.toml
   - Check that the build command works locally

### Debug Commands

```bash
# Test semantic-release locally
uv run semantic-release --version
uv run semantic-release --noop

# Check what version would be released
uv run semantic-release --version --print

# Validate configuration
uv run python -c "import tomllib; print('Config valid')" < pyproject.toml
```

## Security Considerations

- **Trusted Publishers**: No API tokens needed in GitHub secrets
- **Environment Protection**: Use GitHub environments for deployment control
- **Minimal Permissions**: Workflows only request necessary permissions
- **Audit Trail**: All releases and deployments are tracked in GitHub

## Best Practices

1. **Review Commits**: Ensure commit messages follow the conventional format
2. **Test Locally**: Run the full test suite before pushing to main
3. **Monitor Releases**: Watch for failed builds or publishing issues
4. **Keep Dependencies Updated**: Regularly update dependencies for security
5. **Document Changes**: Use clear commit messages and update documentation

## Support

For issues with:
- **PyPI Trusted Publishers**: [PyPI Documentation](https://docs.pypi.org/trusted-publishers/)
- **semantic-release**: [Python Semantic Release Docs](https://python-semantic-release.readthedocs.io/)
- **GitHub Actions**: [GitHub Actions Documentation](https://docs.github.com/en/actions)